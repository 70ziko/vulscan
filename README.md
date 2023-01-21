# vulscan - Vulnerablity Scanner for the
 This program compares installed software with a vulnerability database and alerts the user of any known vulnerabilities. It works on Linux. Functionality on Windows and MacOS is under development

## Features
- Scans installed software on your system
- Compares the results with a vulnerability database of your choosing, currently the https://nvd.nist.gov.pl website
- Alerts the user of any known vulnerabilities
- Support for different package managers depending on the OS
- Easy to use command line interface

## Requirements
- Python 3.x
- `pip` package manager
- requests
- bs4

## Usage
    Type in ./vulscan -h or python3 vulscan.py -h to see available options of running the program

## Contributing
If you're interested in contributing to the project, please feel free to open a pull request or an issue.

## In development
 - (under testing) OS detection and automatic selection
 - Package version comparison
 - more package managers!!
 - various APIs for working with different databases and making searches ⚡blazingly fast⚡
