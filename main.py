import sys
import json
import logging
import argparse
import traceback
import http.client

from config import get_config
from logger import log, get_log_levels, configure_logging


def main():
    parser = argparse.ArgumentParser(description="Peeper")
    parser.add_argument("-c", "--config", default='conf.yaml', help="path to the configuration file")
    parser.add_argument("-l", "--log", help="path to the log file")
    parser.add_argument("--log-level", choices=get_log_levels(), default='INFO', help="logging level")
    args = parser.parse_args()

    configure_logging(args.log, args.log_level, 'sender')

    log("Loading configuration...")
    conf = get_config(args.config)

    requests = conf.get_requests()
    input_help = ['Select command:', "0: exit application"] + ['%s: %s' % (key, requests[key].title) for key in requests]

    command_id = ''
    while command_id != '0':
        log(*input_help)
        try:
            command_id = input('Input command code: ')
        except:
            log("Stopping app because of: ")
            traceback.print_exc(file=sys.stdout)
            break
        if command_id in requests:
            try:
                connection = http.client.HTTPConnection(host=conf.get_host(), port=conf.get_port())
                req_settings = requests[command_id]
                connection.request(req_settings.type, req_settings.path,
                                   json.dumps(req_settings.body), req_settings.headers)
                response = connection.getresponse()
                log("Status: {} and reason: {}".format(response.status, response.reason))
                log("Response body:", response.read().decode(), '\n')
                connection.close()
            except Exception as exc:
                log('Unable to send request', lvl=logging.WARNING)
                log(str(exc), lvl=logging.WARNING)
        else:
            if command_id != '0':
                log("Unknown command code!", '\n')
    else:
        log("'0' selected, exiting application...")


if __name__ == '__main__':
    main()
