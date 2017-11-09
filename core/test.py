services = [['FastEthernet0/1', 'Input 0.0 % Output 0.0 %', '0'], ['FastEthernet0/2', 'Interface not found', '1'],
            ['Fan 1', 'Normal', '0'], ['Fan 2', 'Normal', '0'], ['Fan 3', 'Normal', '0'], ['RTT', '1.173', '0'],
            ['Uptime', '1:55:46', '0'], ['chassis_temperature', '20 °C', '0']]
# print("oryginal:")
# print(services)
# for item in services:
#     print("item:")
#     print(item)
#     if item[2] == '0':
#         print(item[2])
#         services.remove(item)
# print("po usunieciu:")
# print(services)


result = [item for item in services if item[2] != '0']
print(result)