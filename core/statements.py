from core.file import *
import os
import sys


class Statements:

    def __init__(self):
        settings = File("../data/manager.json")
        self.lang = settings.get_record("lang")
        self.debug = settings.get_record("debug")
        self.statements_data = File("../data/statements.json").read_file()

    def get_statement(self, err, own=""):
        if self.debug == 1:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

            statement = "Error in " + file_name + ":" + str(exc_tb.tb_lineno) + ": \n"\
                        + str(err.__class__.__name__) + ": " + str(err) + "\n" \
                        + "Error doc: " + err.__doc__ + " " + "\n" + own
            return statement
        else:
            if err.__class__.__name__ in self.statements_data[self.lang]:
                return self.statements_data[self.lang][err.__class__.__name__] + "\n" + own
            else:
                return str(err.__class__.__name__) + ": " + str(err) + "\n" + own
