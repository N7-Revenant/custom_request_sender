import os
import sys
import logging


class __Vars:
    """Класс-хранилище для глобальных приватных переменных модуля"""
    __slots__ = []
    logger = None
    """Переменная, хранящая последний созданный функцией create_logger логгер"""


def get_log_levels() -> list:
    """Получить список имен уровней логирования

    Возвращает список допустимых имен уровней логирования

    :return: Список, содержащий допустимые названия уровней логирования
    """
    return [logging.getLevelName(x) for x in range(0, 51, 10)]


def configure_logging(log_path: str, log_level: str, name: str='') -> None:
    """Конфигурация логгера, находящегося во внутреннем хранилище.

    Настроенный логгер хранится внутри модуля. Единовременно возможно хранение только одного набора настроек
    логирования. Каждый новый вызов данной функции будет заменять хранимые настройки.

    :param log_path: Строка, содержащая путь к файлу, в который будут записываться логи сервиса
    :param log_level: Строка, содержащая имя уровня логирования
    :param name: Строка, содержащая имя логгера
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    if log_path:
        if os.path.dirname(log_path) != '':
            os.makedirs(os.path.dirname(log_path), exist_ok=True)

        handler = logging.FileHandler(log_path)
    else:
        handler = logging.StreamHandler(sys.stdout)

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    __Vars.logger = logger


def log(s: str, lvl: int=logging.INFO) -> None:
    """Запись информации в лог

    Логгирование информации осуществляется с помощью логгера, содержащегося во внутреннем хранилище модуля. Если
    логгер в хранилище отсутствует, сообщение будет отправлено на stdout с помощью стандартной функции print()

    :param s: Строка, содержащая логируемое сообщение
    :param lvl: Целое число, содержащее уровень логирования (DEBUG, INFO, WARNING и т.д. из модуля logging)
    """
    logger = __Vars.logger
    if logger is not None:
        logger.log(lvl, s)
    else:
        print(s)
