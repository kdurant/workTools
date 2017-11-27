#-*- coding:utf-8 -*-
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