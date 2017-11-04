from core.import_file import ImportFile


class ImportHost(ImportFile):
    def is_valid(self):
        max_col = self.ws.max_column
        first_row = []
        pattern = ['name', 'description', 'address', 'snmp_version', 'community', 'security_name',
                   'security_level', 'auth_protocol', 'priv_key', 'priv_protocol', 'auth_key', 'uptime',
                   'interface', 'chassis_temperature', 'fan_status', 'is_on']
        for i in range(max_col):
            first_row.append(self.file_data[i][0])
        if first_row != pattern:  # If wrong return 1
            return 1

    def is_empty(self):
        errors = []
        self.errors = errors  # Field errors with errors list after checked if all is in file.
        v_2c = []
        v_3 = []

        for i in [0, 2, 3]:
            if None in self.file_data[i]:
                row_number = self.file_data[i].index(None) + 1
                col_name = self.file_data[i][0]
                errors.append(col_name + " is empty in " + str(row_number) + ". row.")

        for i in range(self.ws.max_row):
            if "2c" in [self.file_data[3][i]]:
                v_2c.append(i)
            elif 3 in [self.file_data[3][i]]:
                v_3.append(i)

        for i in v_2c:
            if None in [self.file_data[4][i]]:
                col_name2 = self.file_data[4][0]
                row_number2 = i + 1
                errors.append(col_name2 + " is empty in " + str(row_number2) + ". row.")

        for i in v_3:
            for j in range(5, 11):
                if None in [self.file_data[j][i]]:
                    col_name3 = self.file_data[j][0]
                    row_number3 = i + 1
                    errors.append(col_name3 + " is empty in " + str(row_number3) + ". row.")
        if errors:
            return 1  # If wrong return 1
