import json


class Settings:
    def __init__(self, file_name, mode='r'):
        self.file_name = file_name
        self.mode = mode
        self.data = self.read_file()

    def read_file(self):
        try:
            with open(self.file_name, self.mode) as (settings_data):
                self.data = json.load(settings_data)
                return self.data
        except Exception as err:
            return err

    def set_setting(self, current_settings, new_settings):
        if new_settings[1]:
            current_settings[new_settings[0]]['warning'] = new_settings[1]
        if new_settings[2]:
            current_settings[new_settings[0]]['critical'] = new_settings[2]
        return current_settings

    def write_file(self, path, data):
        with open(path, 'w') as f:
            json.dump(data, f)
        success = "Change settings successfully"
        return success

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
