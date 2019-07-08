import yaml
import logging
import cerberus

from pathlib import Path
from typing import Any, Callable

from logger import log


class Request:
    def __init__(self, req_title, req_type, req_path, req_body, req_headers):
        self.title = req_title
        self.type = req_type
        self.path = req_path
        self.body = req_body
        self.headers = req_headers


class Config:
    """Класс, содержащий словарь с конфигурацией и методы доступа к ее элементам

    :param conf_dict: Словарь с конфигурацией
    """
    __slots__ = ['__host', '__port', '__requests']

    def __init__(self, conf_dict: dict):
        self.__host = conf_dict['general']['host']
        self.__port = conf_dict['general']['port']
        self.__requests = {}
        for count, item in enumerate(conf_dict['requests'], start=1):
            self.__requests.update({str(count): Request(req_title=item.get('title'),
                                                        req_type=item.get('type'),
                                                        req_path=item.get('path'),
                                                        req_body=item.get('body', {}),
                                                        req_headers=item.get('headers', {}))})

    def get_host(self) -> str:
        return self.__host

    def get_port(self) -> str:
        return self.__port

    def get_requests(self) -> dict:
        return self.__requests


class ConfigurationSettings:
    """Класс, содержащий схему валидации конфигурации и значения по умолчанию"""
    __slots__ = ['default', 'schema']

    def __init__(self):
        self.default = {
            'general': {
                'host': '127.0.0.1',
                'port': 8080
            },
            'requests': []
        }
        """Стандартные значения конфигурационных параметров"""

        self.schema = {
            'general': {
                'type': 'dict',
                'nullable': True,
                'schema': {
                    'host': {'type': 'string'},
                    'port': {'type': 'integer',
                             'min': 1024,
                             'max': 65535}
                }
            },
            'requests': {
                'type': 'list',
                'nullable': True,
                'schema': {
                    'type': 'dict',
                    'schema': {
                        'title': {'type': 'string'},
                        'type': {'type': 'string', 'allowed': ['GET', 'POST', 'PUT', 'DELETE']},
                        'path': {'type': 'string'},
                        'body': {'type': 'dict',
                                 'nullable': True},
                        'headers': {'type': 'dict',
                                    'nullable': True}
                    }
                }
            }
        }
        """Cerberus-схема для валидации конфигурации"""

    @staticmethod
    def __check_file_existence(field: str, value: Any, error: Callable) -> None:
        """Метод, используемый для проверки того, что в конфигурации указан реально существующий файл

        :param field: Поле схемы, в котором выполняется проверка
        :param value: Путь к файлу
        :param error: Метод Cerberus, используемый для фиксации ошибки
        """
        if value and not Path(value).is_file():
            error(field, 'File "' + str(value) + '''" doesn't exist''')

    @staticmethod
    def __check_folder_existence(field: str, value: Any, error: Callable) -> None:
        """Метод, используемый для проверки того, что в конфигурации указан реально существующий файл

        :param field: Поле схемы, в котором выполняется проверка
        :param value: Путь к каталогу
        :param error: Метод Cerberus, используемый для фиксации ошибки
        """
        if value and not Path(value).is_dir():
            error(field, 'Folder "' + str(value) + '''" doesn't exist''')


def __merge_conf_dicts(base_dict: dict, update_dict: dict) -> dict:
    """Метод, выполняющий рекурсивное слияние 2-х словарей конфигураций

    По каждому ключу из базового словаря выполняется поиск во втором словаре и, если там такой ключ найден,
    его значение заменяет собой значение из базового словаря.

    :param base_dict: Базовый словарь, используемый в качестве основы
    :param update_dict: Словарь-заменитель, значения которого должны заменить собой аналогичные из базового
    :return: Словарь, построенный на основе базового, значения которого обновлены с помощью словаря-заменителя
    """
    res = dict()
    for key in base_dict:
        if key in update_dict and update_dict[key] is not None:
            if isinstance(base_dict[key], dict):
                res.update({key: __merge_conf_dicts(base_dict[key], update_dict[key])})
            else:
                res.update({key: update_dict[key]})
        else:
            res.update({key: base_dict[key]})
    return res


def get_config(config_file_path: str=None) -> Config:
    """Метод получения конфигурации приложения

    Возвращает объект класса Config, хранящий настройки конфигурации и предоставляющий методы доступа к ним

    :param config_file_path: Путь к YAML-файлу, содержащему конфигурацию приложения
    :return: Объект класса Config, содержащий конфигурацию приложения
    """
    result = dict()
    settings = ConfigurationSettings()
    if config_file_path:
        try:
            with open(config_file_path, 'r') as conf:
                config = yaml.safe_load(conf.read())
                v = cerberus.Validator(settings.schema)
                v.allow_unknown = True
                if v.validate(config):
                    log('Configuration validation passed!')
                    result.update(__merge_conf_dicts(settings.default, config))
                    log('Working with configuration:')
                else:
                    log('Configuration validation failed!', logging.WARNING)
                    log(v.errors, logging.WARNING)
                    result.update(settings.default)
                    log('Using default configuration:', logging.WARNING)
        except Exception as exc:
            log('Configuration file reading failed with following exception:', logging.WARNING)
            log(str(exc), logging.WARNING)
            log('Using default configuration:', logging.WARNING)
            result.update(settings.default)
    else:
        log('Configuration file not specified, using default configuration:', logging.WARNING)
        result.update(settings.default)
    log(str(result))
    return Config(result)
