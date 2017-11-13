from core.file_json import *

class Settings():
    def set_setting(self, current_settings, new_settings):
        if new_settings[1]:
            current_settings[new_settings[0]]['oid'] = new_settings[1]
        if new_settings[2]:
            current_settings[new_settings[0]]['description'] = new_settings[2]
        if new_settings[3]:
            current_settings[new_settings[0]]['warning'] = new_settings[3]
        if new_settings[4]:
            current_settings[new_settings[0]]['critical'] = new_settings[4]
        return current_settings

