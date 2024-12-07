#This file contains the code for handling errors/exception and giving us the details of the same, this file is common for all the project
import sys
from .logger import logging

class CustomException(Exception):
    """ 
    Class to handle the custom exception.
    
    Args:
        Exception (class): The base class for all exceptions.
    """
    
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message=error_message_detail(error_message,error_detail=error_detail)
    
    def __str__(self):
        return self.error_message
    

def error_message_detail(error,error_detail:sys):
    """ 
    Function to get the details of the error message in desired format.
    
    Args:
        error (str): The error message.
        error_detail (sys): The error details.
    """
    _,_,exc_tb=error_detail.exc_info()
    file_name=exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occurred in python script named: [{0}], line number: [{1}], error message: [{2}]".format()
    logging.info(error_message)
    file_name,exc_tb.tb_lineno,str(error)
    return error_message


    
