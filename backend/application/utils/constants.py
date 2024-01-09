from enum import Enum


class Group(Enum):
    """権限"""

    MANAGER = 1
    """管理者"""
    GENERAL = 2
    """一般"""
