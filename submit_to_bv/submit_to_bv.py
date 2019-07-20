""" submit_to_bv.submit_to_by -- ##########
"""

# Base Libraries
import argparse
import logging
import os
import os.path
import sys

# Third Party Libraries
import requests


class SubmitToBV(object):
    """
        Description
    """

    def __init__(self, api_key, log):
        logging.basicConfig(
            filename=log,
            filemode='a',
            level=logging.INFO)
        self.api_key = api_key
        self.log = log
        self.logger = logging.getLogger(__name__)

    def submit(self, input_path, log=True):
        if os.path.exists(input_path) is not True:
            raise ValueError("Invalid input path to file or directory provided for upload")
        else:
            files = []
            base_url = 'http://api-dev.bluvector.io'
            if os.path.isfile(input_path) is True:
                files.append(os.path.abspath(input_path))
            else:
                for dirpath, dirnames, filenames in os.walk(input_path):
                    files.extend([os.path.abspath(os.path.join(dirpath, name))
                                  for name in filenames if not name.startswith(".")])
            for fname in files:
                f = {
                    'file': open(fname, 'rb')
                }
                response = requests.post(
                    url='{}/hector/v1/results'.format(base_url),
                    files=f,
                    auth=(
                        'bluvector-dev',
                        '5cfdd6c280dc4534bc844cbfb6c8c0e1'))
                if response.status_code > 299:
                    self.logger.error("File: %s, Status Code: %s -- %s", fname, response.status_code, response.reason)
                else:
                    self.logger.info("File: %s, Status Code: %s -- %s", fname, response.status_code, response.reason)


def my_arg_parser(args):
    parser = argparse.ArgumentParser(
        description=(
            "Gathering files wished to be sent to BluVector"))
    parser.add_argument(
        "api_key",
        help=(
            "BluVector Portal Customer Key"))
    parser.add_argument(
        "input_path",
        help=(
            "Path to file or directory wish to submit"))
    parser.add_argument(
        "-l",
        "--log-filename",
        default="./submit_to_bv.log",
        help=(
            "Path to output log file (default: './submit_to_bv.log')"))
    args = parser.parse_args(args)
    return args


def cli(args):
    client = SubmitToBV(api_key=args.api_key, log=args.log_filename)
    client.submit(args.input_path)
    print "Done"


def main():
    args = my_arg_parser(sys.argv[1:])
    cli(args)


if __name__ == "__main__":
    main()
