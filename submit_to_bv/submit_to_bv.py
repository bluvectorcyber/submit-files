# Copyright 2019 BluVector, A Comcast Company
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

import argparse
import logging
import os
import os.path
import sys
import json
import requests


class SubmitToBV():

    def __init__(self, username, password, log="./submit_to_bv.log", server_hostname="api.bluvector.io"):
        logging.basicConfig(
            filename=log,
            filemode="a",
            format="[%(levelname)s] %(asctime)s - %(message)s",
            datefmt="%d-%b-%y %H:%M:%S",
            level=logging.INFO)
        self.password = password
        self.service_url = "https://{0}/hector/v1/results".format(server_hostname)
        self.log = log
        self.logger = logging.getLogger(__name__)
        self.username = username

    def submit(self, input_path, log=True):
        """
            Method for providing a path to a file or directory of files to submit. Results of analysis
            and any errors are stored in log or printed to stdout.

            parameters:
                input_path: [string] path to file or directory
                log: [boolean, default: True] When true, stores results in a log file otherwise prints to stdout
        """
        if not os.path.exists(input_path):
            raise ValueError("Invalid input path to file or directory provided for upload")

        # Generate file list for submission
        files = []
        if os.path.isfile(input_path):
            files.append(os.path.abspath(input_path))
        else:
            for dirpath, dirnames, filenames in os.walk(input_path):
                files.extend([os.path.abspath(os.path.join(dirpath, name))
                              for name in filenames if not name.startswith(".")])

        # Submit each file in list one at a time
        for fname in files:
            try:
                result = self.submit_file(fname)
            except RuntimeError as err:
                if log:
                    self.logger.error(err)
                else:
                    print(err)
                continue

            msg = "{0}: {1}".format(fname, result)
            if log:
                if result["malicious"]:
                    self.logger.warning(msg)
                else:
                    self.logger.info(msg)
            else:
                print(msg)

    def submit_file(self, filename):
        """
            Method for submitting a single file and receiving analysis results as a JSON object
            if analysis fails a RuntimeError will be raised

            parameters:
                filename: [string] fully qualified path to a file
        """
        with open(filename, "rb") as f:
            response = requests.post(
                url=self.service_url,
                files={
                    "file": f
                },
                auth=(self.username, self.password),
                verify=False
            )
        if not response.ok:
            raise RuntimeError("File: {0}: Status Code: {1} -- {2}"
                               .format(filename, response.status_code, response.reason))
        return json.loads(response.content)


def my_arg_parser(args):
    parser = argparse.ArgumentParser(
        description=(
            "Gathering files wished to be sent to BluVector"))
    parser.add_argument(
        "username",
        help=(
            "BluVector Portal Username"))
    parser.add_argument(
        "password",
        help=(
            "BluVector Portal Password"))
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
    parser.add_argument(
        "-s",
        "--server-hostname",
        default="api.bluvector.io",
        help=(
            "Hostname of the Submit to BluVector service (default: 'api.bluvector.io')"))
    args = parser.parse_args(args)
    return args


def cli(args):
    client = SubmitToBV(args.username, args.password, 
                        log=args.log_filename, server_hostname=args.server_hostname)
    client.submit(args.input_path)
    print("Done")


def main():
    args = my_arg_parser(sys.argv[1:])
    cli(args)


if __name__ == "__main__":
    main()
