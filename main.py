import argparse

from config import get_config, Config
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


if __name__ == '__main__':
    main()
