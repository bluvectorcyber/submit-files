"""
This contains all the unit tests necessary for
submit_to_bv.submit_to_bv.SubmitToBv
"""
from submit_to_bv.submit_to_bv import SubmitToBV
import os
import pytest

def test__invalid_input_path():
    with pytest.raises(ValueError) as excinfo:
        stbv = SubmitToBV("api_key", "log", "username")
        s = stbv.submit("fake_folder")
    assert 'Invalid input path to file or directory provided for upload' in str(excinfo.value)

def test__invalid_credentials(caplog):
    f=open("file.txt", "w+")
    f.write("Testing testing 1,2,3")
    f.close() 
    stbv = SubmitToBV("fake_api_key", "log", "fake_username")
    s = stbv.submit("./file.txt")
    os.remove("./file.txt")
    assert "Status Code: 400 -- Bad Request" in caplog.text