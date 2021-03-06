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

"""
This contains all the unit tests necessary for
submit_to_bv.submit_to_bv.SubmitToBv
"""

import os
import json
import sys
import logging
from io import StringIO, BytesIO
from unittest import TestCase
try:
    from unittest.mock import Mock, patch, mock_open
except ImportError:
    from mock import Mock, patch, mock_open

from submit_to_bv.submit_to_bv import SubmitToBV


def mock_response(
        status=200,
        message="TEST",
        malicious=False,
        json_data=None,
        raise_for_status=None,
        reason="error occured",
        text="test"):
    mock_resp = Mock()
    mock_resp.raise_for_status.side_effect = raise_for_status
    mock_resp.status_code = status
    mock_resp.content = json.dumps({ "message": message, "malicious": malicious })
    mock_resp.headers = {"x-feapi-token": "test"}
    mock_resp.text = text
    mock_resp.ok = status < 400
    mock_resp.reason = reason

    if json_data:
        mock_resp.json.return_value = json_data

    return mock_resp

    
class TestSubmitToBV(TestCase):
    
    def setUp(self):
        self.test_file = "./mock_file.txt"
        with open("mock_file.txt", "w+") as f:
            f.write("Testing testing 1,2,3")
        # Determine location of builtin open method based on version of Python
        self.open_at = "__builtin__.open"
        if sys.version_info >= (3, 0):
            self.open_at = "builtins.open"
            
    def tearDown(self):
        os.remove(self.test_file)
    
    def test__invalid_input_path(self):
        stbv = SubmitToBV("user", "pass", "log")
        self.assertRaises(ValueError, stbv.submit, "fake_folder")
        
    @patch("sys.stdout", new_callable=StringIO if sys.version_info >= (3, 0) else BytesIO)
    @patch("requests.post")
    def test__invalid_credentials(self, mock_post, mock_print):
        mock_resp = mock_response(
            status=400, message=json.dumps("ERROR"), reason="Bad Request")
        mock_post.return_value = mock_resp
        with patch(self.open_at, mock_open(read_data="data")) as mock_file:
            assert open(self.test_file).read() == "data"
            mock_file.assert_called_with(self.test_file)
            stbv = SubmitToBV("fake_user", "fake_pass", "log")
            with patch.object(logging.Logger, "error") as log:
                stbv.submit(self.test_file)
                self.assertIn("400 -- Bad Request", "{0}".format(log.call_args[0][0]))
            stbv.submit(self.test_file, log=False)
            assert "400 -- Bad Request" in mock_print.getvalue()
                        
    @patch("sys.stdout", new_callable=StringIO if sys.version_info >= (3, 0) else BytesIO)
    @patch("requests.post")
    def test__successful_analysis_benign(self, mock_post, mock_print):
        mock_resp = mock_response(message="MOCK BENIGN")
        mock_post.return_value = mock_resp
        with patch(self.open_at, mock_open(read_data="data")) as mock_file:
            assert open(self.test_file).read() == "data"
            mock_file.assert_called_with(self.test_file)
            stbv = SubmitToBV("fake_user", "fake_pass", "log")
            with patch.object(logging.Logger, "info") as log:
                stbv.submit(self.test_file)
                self.assertIn("MOCK BENIGN", log.call_args[0][0])
            stbv.submit(self.test_file, log=False)
            assert "MOCK BENIGN" in mock_print.getvalue()
            
    @patch("requests.post")
    def test__successful_analysis_malicious(self, mock_post):
        mock_resp = mock_response(message="MOCK MALICIOUS", malicious=True)
        mock_post.return_value = mock_resp
        with patch(self.open_at, mock_open(read_data="data")) as mock_file:
            assert open(self.test_file).read() == "data"
            mock_file.assert_called_with(self.test_file)
            stbv = SubmitToBV("fake_user", "fake_pass", "log")
            with patch.object(logging.Logger, "warning") as log:
                stbv.submit(self.test_file)
                self.assertIn("MOCK MALICIOUS", log.call_args[0][0])