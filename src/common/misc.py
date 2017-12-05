#-*- coding:utf-8 -*-

import time
from functools import wraps

def diskInfo():
    '''
    找到系统有几块硬盘可用
    :return:
    '''
    info = ['\\\\.\\PHYSICALDRIVE2']
    # disk = open('\\\\.\\PHYSICALDRIVE0', 'rb')
    # try:
    #     disk = open('\\\\.\\PHYSICALDRIVE0', 'rb')
    # except PermissionError:
    #     info.append('\\\\.\\PHYSICALDRIVE0')
    # try:
    #     disk = open('\\\\.\\PHYSICALDRIVE1', 'rb')
    # except PermissionError:
    #     info.append('\\\\.\\PHYSICALDRIVE1')

    return info


def readSector(drive, sector, data_len=512, mode='rb'):
    '''
    :param drive: 需要读取的硬盘
    :param sector: 需要读取的扇区编号
    :param data_len: 每次读取多少数据
    :param mode: 返回数据格式
    :return: 扇区数据
    '''
    drive.seek(sector * 512)
    data = drive.read(data_len)

    if mode == 'rb':
        return data
    elif mode == 'str':
        return data.hex()
    else:
        return

def eraserSector(drive, sector, data, data_len=512):
    '''
    :param drive: 需要写入数据的硬盘
    :param sector: 需要写入的扇区编号
    :param data:
    '''
    drive.seek(sector * 512)
    drive.write(data*data_len)


def str2list(s, width):
    '''将字符串按照指定宽度截取成列表，且列表数据转换为16进制'''
    if len(s) % width == 0:
        return [int(s[x:x + width], 16) for x in range(0, len(s), width)]
    else:
        print('hello world')


def timethis(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        r = func(*args, **kwargs)
        end = time.perf_counter()
        print('{}.{} : {}'.format(func.__module__, func.__name__, end - start))
        return r
    return wrapper

# @timethis
# def countdown(n):
#     while n > 0:
#         n -= 1
#
# countdown(100000)