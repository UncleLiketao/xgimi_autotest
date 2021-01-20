"""
@author: jack.tang  
@date: 2020/12/19 
"""


class CommonException(Exception):
    def __init__(self, *args):
        self.args = args
