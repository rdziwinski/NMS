from core.file_json import *


class Settings():
    def set_setting(self, current_settings, new_settings):
        if new_settings[1]:
            current_settings[new_settings[0]]['warning'] = new_settings[1]
        if new_settings[2]:
            current_settings[new_settings[0]]['critical'] = new_settings[2]
        return current_settings