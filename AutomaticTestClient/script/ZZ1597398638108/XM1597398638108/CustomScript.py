# -*- coding: utf-8 -*-
"""
@Time ： 2020/9/1 11:05
@Auth ： 邓锐坤
@File ：CustomScript.py
@IDE ：PyCharm

"""


def run(methodName, paramDict):
    result = globals().get(methodName)(paramDict)
    return result


def a(paramDict):
    return paramDict
