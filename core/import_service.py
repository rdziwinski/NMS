from core.import_file import ImportFile


class ImportService(ImportFile):
    def is_valid(self):
        max_col = self.ws.max_column
        first_row = []
        pattern = ['category', 'uptime', 'ping', 'interface_status', 'interface_utilization', 'chassis_temperature',
                   'fan_status']
        for i in range(max_col):
            first_row.append(self.file_data[i][0])
        if first_row != pattern:  # If wrong return 1
            return 1
