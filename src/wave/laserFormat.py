# -*- coding:utf-8 -*-
import logging
'''
根据协议获得各字段数据
'''
# 如果子类定义了构造函数，而没有调用父类构造函数
# 将不具备父类的所有属性（包括使用到父类属性的父类方法）

def str2list(s, width):
    '''将字符串按照指定宽度截取成列表，且列表数据转换为10进制'''
    if len(s) % width == 0:
        return [int(s[x:x+width], 16) for x in range(0, len(s), width)]
    else:
        print('hello world')

def find_all(string, sub_str):
    return [i for i in range(len(string)) if s[i:].startswith(sub_str)]

class LaserFormat (object):
    def __init__(self):  #构造方法
        self.data = ''
        self.trg = 0
        self.ch1_has = 0
        self.head = u'01234567'
        # offset 20:23
        # self.gps_week = 0
        # # offset 24:31
        # self.gps_second = 0
        # # offset 32:39
        # self.gps_sub_time = 0
        # # offset 40:47
        # self.gps_azimuth_angle = 0  # 方位角
        # # offset 48:55
        # self.gps_pitch_angle = 0    # 俯仰角
        # # offset 56:63
        # self.gps_roll_angle = 0     # 翻滚角
        # # offset 64:71
        # self.gps_llatitudina = 0    # 纬度
        # # offset 72:79
        # self.gps_longitude = 0      # 经度
        # # offset 80:87
        # self.gps_height = 0         # 高度
        # # offset 88:95
        # self.motor_bit = 0
        # # offset 96:103
        # self.motor_cnt = 0
        # # offset 104:111
        # self.jane_num = 0
        # # offset 112:119
        # self.wave_len = 0

        self.motor_cnt = []

        self.ch0_first_start_pos = []
        self.ch0_first_pick_len = []
        self.ch0_second_start_pos = []
        self.ch0_second_pick_len = []
        self.ch0_second_data_x = []
        self.ch0_second_data_y = []

        self.ch1_first_start_pos = []
        self.ch1_first_pick_len = []
        self.ch1_second_start_pos = []
        self.ch1_second_pick_len = []

        self.ch2_first_start_pos = []
        self.ch2_first_pick_len = []
        self.ch2_second_start_pos = []
        self.ch2_second_pick_len = []

        self.ch3_first_start_pos = []
        self.ch3_first_pick_len = []
        self.ch3_second_start_pos = []
        self.ch3_second_pick_len = []

        self.ch0_first_start_pos_error = []
        self.ch0_first_pick_len_error = []
        self.ch0_second_start_pos_error = []
        self.ch0_second_pick_len_error = []

        self.ch1_first_start_pos_error = []
        self.ch1_first_pick_len_error = []
        self.ch1_second_start_pos_error = []
        self.ch1_second_pick_len_error = []

        self.ch2_first_start_pos_error = []
        self.ch2_first_pick_len_error = []
        self.ch2_second_start_pos_error = []
        self.ch2_second_pick_len_error = []

        self.ch3_first_start_pos_error = []
        self.ch3_first_pick_len_error = []
        self.ch3_second_start_pos_error = []
        self.ch3_second_pick_len_error = []

        # offset 120:123
        # offset 124:127

        # 错误标志
        self.total_error = []
        self.len_error = []

    def setData(self, data, trg):
        '''
        :param data: 一次采集的全部数据
        :param trg:
        :return:
        '''
        if data:
            self.data = data
        self.trg = trg

    def getGPSWeek(self):
        tmp = self.data[20:24]
        tmp = tmp[2:4] + tmp[0:2]
        self.gps_week = str((int(tmp, 16)))

    def getGPSSecond(self):
        tmp = self.data[24:32]
        tmp = tmp[6:8] + tmp[4:6] + tmp[2:4] + tmp[0:2]
        self.gps_second = str((int(tmp, 16)))

    def getGPSSubTime(self):
        self.gps_sub_time = str((int(self.data[32:40], 16)))

    def getGPSAzimutuAngle(self):
        self.gps_azimuth_angle = str((int(self.data[40:48], 16)))

    def get_gps_pitch_angle(self):
        self.gps_pitch_angle = str((int(self.data[48:56], 16)))

    def get_gps_roll_angle(self):
        self.gps_roll_angle = str((int(self.data[56:64], 16)))

    def get_gps_llatitudina(self):
        self.gps_llatitudina = str((int(self.data[64:72], 16)))

    def get_gps_longitude(self):
        self.gps_longitude = str((int(self.data[72:80], 16)))

    def get_gps_height(self):
        self.gps_height = str((int(self.data[80:88], 16)))

    def get_motor_bit(self):
        self.motor_bit = str((int(self.data[88:96], 16)))

    def get_motor_cnt(self):
        data = int(self.data[96:104], 16)
        self.motor_cnt.append(data)
        # self.motor_cnt = str((int(self.data[96:104], 16)))

    def get_jane_num(self):
        self.jane_num = str((int(self.data[104:112], 16)))

    def get_wave_len(self):
        self.wave_len = str((int(self.data[112:120], 16)))

    def getChData(self, type='land'):
        if type == 'land':
            return self.getLandData()
        else:
            return self.getOeacnData()
    def getLandData(self):
        pass

    def getOeacnData(self):
        l = []
        Xdata, Ydata = self.getOeacnChData('eb90a55a0000')
        l.append(Xdata)
        l.append(Ydata)
        Xdata, Ydata = self.getOeacnChData('eb90a55a0f0f')
        l.append(Xdata)
        l.append(Ydata)
        Xdata, Ydata = self.getOeacnChData('eb90a55af0f0')
        l.append(Xdata)
        l.append(Ydata)
        Xdata, Ydata = self.getOeacnChData('eb90a55affff')
        l.append(Xdata)
        l.append(Ydata)
        return l

    def getOeacnChData(self, flag='eb90a55a0000'):
        '''
        1. 找到第一段数据的起始位置，和数据长度

        2. 根据长度和起始位置，获得第一段数据的x轴坐标
        3a. 得到第一段数据的字符串格式
        3b. 获得第一段数据的y轴数据

        4. 找到第二段数据的起始位置，和数据长度
        5. 根据长度和起始位置，获得第一段数据的x轴坐标
        6a. 得到第二段数据的字符串格式
        6b. 获得第二段数据的y轴数据
        '''
        index = self.data.find(flag)
        if index != -1:
            # 1.找到第一段数据的起始位置，和数据长度
            pos = index + 12
            first_start_pos = int(self.data[pos:pos+4], 16)
            first_pick_len = int(self.data[pos+4:pos+8], 16)

            # 2. 根据长度和起始位置，获得第一段数据的x轴坐标
            Xdata = [ i+first_start_pos for i in range(first_pick_len)]

            # 3a. 得到第一段数据的字符串格式
            pos = index + 20
            first_data_string = self.data[pos:pos + first_pick_len*4]
            #first_data_string = self.data[pos:pos + 2400]
            # 3b. 获得第一段数据的y轴数据
            Ydata = str2list(first_data_string, 4)

            # # 4. 找到第二段数据的起始位置，和数据长度
            pos = index + (10+first_pick_len*2)*2
            second_start_pos = int(self.data[pos:pos+4], 16)
            second_pick_len = int(self.data[pos+4:pos+8], 16)
            Xdata = Xdata + [ i+second_start_pos for i in range(second_pick_len)]

            pos = pos+8
            second_data_string = self.data[pos : pos+second_pick_len*4]
            Ydata = Ydata + str2list(second_data_string, 4)
            return Xdata, Ydata
        else:
            return [], []


    def analyze(self):
        self.getGPSWeek()
        self.getGPSSecond()
        self.getGPSSubTime()
        self.getGPSAzimutuAngle()
        self.get_gps_pitch_angle()
        self.get_gps_roll_angle()
        self.get_gps_llatitudina()
        self.get_gps_longitude()
        self.get_gps_height()
        self.get_motor_bit()
        self.get_motor_cnt()
        self.get_jane_num()
        self.get_wave_len()
