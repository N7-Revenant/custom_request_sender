import http.client
import argparse

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
    input_help = ["0: exit application"] + ['%s: %s' % (key, requests[key].title) for key in requests]

    command_id = ''
    while command_id != '0':
        print('Select command:', *input_help, sep='\n')
        command_id = input('Input command code: ')
        if command_id in requests:
            connection = http.client.HTTPConnection(host=conf.get_host(), port=conf.get_port())
            req_settings = requests[command_id]
            connection.request(req_settings.type, req_settings.path)
            response = connection.getresponse()
            print("Status: {} and reason: {}".format(response.status, response.reason))
            print("Response body:", response.read().decode(), sep='\n', end='\n\n')
            connection.close()
        else:
            if command_id != '0':
                print("Unknown command code!", end='\n\n')
    else:
        print("'0' selected, exiting application...")


if __name__ == '__main__':
    main()
