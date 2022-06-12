# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 10:56:19 2022

@author: Jasmine Rimani

The code is a collection of Custom Exception for the HIST Development
"""

class NotDefinedRequirements(Exception):
    """Exception raised for modes not in the defined MIRS dictionary.

    Attributes:
        mode -- input mode which caused the error
        message -- explanation of the error
    """

    def __init__(self, message="You defined no requirements for your domain!"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.mode} -> {self.message}'