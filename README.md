# BluVector File Submission Python Wrapper
submit_to_bv is a Python wrapper for the BluVector Malware Analysis Portal. It can be used to submit either individual files or a directory of files. Results of the BluVector analysis will be stored in a log. 

## Develop
This software is built using Python 3.7. The package should be built and tested in a Python 3.7 virtual environment.
```sh
$ python3 -m venv submit-files
$ source submit-files/bin/activate
```

To deactivate the virtual environment:
```sh
$ deactivate
```

### Build
To build the python package:
```sh
$ pip install -r requirements.txt
$ python setup.py build
```

### Install
To install the python package:
```sh
$ python setup.py install
```

### Test
Run the unit tests from the top level of the repository.

```sh
$ tox
```

## Register for BluVector Malware Analysis Portal Access
To use the BluVector Malware Analysis Portal you must register with BluVector and receive a Username and Password. You can register for free access at https://www.bluvector.io/trial. Users are limited to 25 file submissions per day. To request a higher limit please contact info@bluvector.io. 

## Use
After installing the package a command line interface is available. 

```sh
$ submit-to-bv -h
usage: submit-to-bv [-h] [-l LOG_FILENAME] username password input_path

Gathering files wished to be sent to BluVector

positional arguments:
  username              BluVector Portal Username
  password              BluVector Portal Password
  input_path            Path to file or directory wish to submit

optional arguments:
  -h, --help            show this help message and exit
  -l LOG_FILENAME, --log-filename LOG_FILENAME
                        Path to output log file (default:
                        './submit_to_bv.log')
```

Suspicious files will be logged as WARNING messages while benign files will be logged as INFO messages.

## License
This software is released under under the Apache License, Version 2.0. You may not use this software except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0. A copy is also provided with this software.
