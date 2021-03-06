import json


class FIleJson:  # change from File
    def __init__(self, file_name, mode='r'):
        self.file_name = file_name
        self.mode = mode
        self.read_file()

    def read_file(self):
        try:
            with open(self.file_name, self.mode) as (settings_data):
                self.data = json.load(settings_data)
                return self.data
        except Exception as err:
            return err

    def get_record(self, level_1="", level_2=""):
        try:
            if level_1 == "" and level_2 == "":
                return self.data
            elif level_1 == "" and level_2 == "":
                return self.data
            elif level_1 != "" and level_2 == "":
                return self.data[level_1]
            elif level_1 == "" and level_2 != "":
                record = []
                for key, value in self.data.items():
                    record.append(value[level_2])
                return record
            else:
                return self.data[level_1][level_2]
        except Exception as err:
            return err
