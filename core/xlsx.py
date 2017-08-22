from openpyxl import load_workbook
from database.host import *


data = load_workbook(filename='../data/hosts.xlsx', read_only=True)
host = data['Routers']

max_col = host.max_column
max_row = host.max_row

data = []
temp = []

for i in range(1, max_col+1):
    temp = []
    for j in range(1, max_row+1):
        sth1 = host.cell(row=j + 1, column=i).value
        temp.append(sth1)
    data.append(temp)

for i in range(max_row-1):
    Host(name=data[0][i], description=data[1][i], address=data[2][i], snmp_version=data[3][i], community=data[4][i],
         security_name=data[5][i], security_level=data[6][i], auth_protocol=data[7][i], priv_key=data[8][i],
         priv_protocol=data[9][i], auth_key=data[10][i]).add()
