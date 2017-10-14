hosts = [['Router V1', 'Opis', '192.168.1.1', '3', None, 'Admin', 'authPriv', 'MD5', 'Password', 'DES', 'Password',
          'Routers'], ['Router V2', 'Opis asdasd', '192.168.1.2', '3', None, 'Admin', 'authPriv', 'MD5', 'Password',
                       'DES', 'Password', 'Routers'], ['Switch drugi', 'Opis 2', '192.168.1.5', '3', None, 'Admin',
                                                       'authPriv', 'MD5', 'Password', 'DES', 'ok', 'Switches'],
         ['Switch glowny4', 'Opisdwa', '192.168.1.6', '2c', 'Password', None, None, None, None, None, None, 'Switches']]


category = [['Routers', True, True, 'fa0/1', None, None, None], ['Switches', True, True, 'fa0/3', '1', True, True]]


for i in range(1, len(hosts)):
    print(hosts[i][11])

