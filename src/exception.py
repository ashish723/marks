import sys
from src.logger import logging 
def error_message_detail(error,error_detail:sys):
    """ this function is used to print return error message"""

    _,_,exc_tb=error_detail.exc_info()
    file_name=exc_tb.tb_frame.f_code.co_filename
    line_no=exc_tb.tb_lineno

    error_message=f"Error occured at file {file_name} lineNo {line_no} error {str(error)}"

    return error_message

class MyException(Exception):
    def __init__(self,error_message,error_detail):
        super().__init__(error_message)
        self.error_message=error_message_detail(error_message,error_detail)

    def __str__(self):

        return self.error_message
    

