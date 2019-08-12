"""
Change the self.base_url (line 21) to https://api.bluvector.io when moving from staging to production
"""

import argparse
import logging
import os
import os.path
import sys
import requests


class SubmitToBV():

    def __init__(self, api_key, log, username):
        logging.basicConfig(
            filename=log,
            filemode='a',
            level=logging.INFO)
        self.api_key = api_key
        self.base_url = 'http://api-dev.bluvector.io'
        self.log = log
        self.logger = logging.getLogger(__name__)
        self.username = username

    def submit(self, input_path, log=True):
        if os.path.exists(input_path) is not True:
            raise ValueError("Invalid input path to file or directory provided for upload")
        files = []
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
                url='{}/hector/v1/results'.format(self.base_url),
                files=f,
                auth=(
                    self.username,
                    self.api_key))
            if response.ok is not True:
                self.logger.error("File: {}, Status Code: {} -- {}"
                                  .format(fname, response.status_code, response.reason))
            else:
                self.logger.info("File: {}, Status Code: {} -- {}"
                                 .format(fname, response.status_code, response.reason))


def my_arg_parser(args):
    parser = argparse.ArgumentParser(
        description=(
            "Gathering files wished to be sent to BluVector"))
    parser.add_argument(
        "username",
        help=(
            "BluVector Portal Username"))
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
    client = SubmitToBV(api_key=args.api_key, log=args.log_filename, username=args.username)
    client.submit(args.input_path)
    print("Done")


def main():
    args = my_arg_parser(sys.argv[1:])
    cli(args)


if __name__ == "__main__":
    main()
