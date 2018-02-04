# Network Monitoring System
Hello, here is my web application for monitoring network by **SNMP** and **ICMP**. This app use **Python**, **Flask**, **EasySNMP**, **SQLAlchemy**, **SQLite3**.  This is not a competition for system like Nagios because it's small app for simple use. The application can monitoring:
 - Interfaces utilization
 - Uptime
 - Chassis temperature
 - Fan status
 - CPU utilization

Import hosts database is realize by *.xlsx file. Example is in **data** folder. 
## Requirements
A Linux system is required to run. Entering the following commands as root should be sufficient:

    apt-get install python3.5 python3-pip libsnmp-dev snmp-mibs-downloader gcc python3.5-dev
    alias python=python3.5
    apt-get install snmp
    pip3 install easysnmp Flask SQLAlchemy openpyxl

To run application please type:

    python NMS.py

I think application is easy to use, but if you have any question please contact me by email: **rdziwinski@gmail.com**
