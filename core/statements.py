from core.file_json import *
import os
import sys


class Statements:

    def __init__(self):
        settings = FIleJson("../data/manager.json")
        self.lang = settings.get_record("lang")
        self.debug = settings.get_record("debug")
        self.statements_data = FIleJson("../data/statements.json").read_file()

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


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class NameIsEmpty(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
