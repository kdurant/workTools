#-*- coding:utf-8 -*-

from .misc import str2list
class EncodeProtocol():
    def __init__(self, table = {}):
        self.pck_num = 8*'0'
        self.table = table
    def config(self, head='AA555AA5AA555AA5', cmd_num='00000000', command='00000000', pck_num='11223344', data_len=4, data='0000'):
        self.head = ''.join(head.split())
        self.cmd_num = ''.join(cmd_num.split()).zfill(8)
        self.command = command
        self.pck_num = ''.join(pck_num.split()).zfill(8)
        self.data_len = ''.join(data_len.split()).zfill(8)
        self.data = ''.join(data.split()).zfill(int(data_len)*2)+(512-int(data_len)*2)*'0'
        pass

    def getCmdNum(self):
        return self.cmd_num

    def getPckNum(self):
        return self.pck_num

    def getCmd(self):
        return  self.command
        # value = ''
        # for key in self.table:
        #     if key == self.command:
        #         value = self.table[key]
        #
        # if not value:
        #     return '88888888'
        # else:
        #     return value

    def getCheckSum(self):
        checksum = int(self.getCmdNum(), 16) + int(self.getCmd(), 16) + \
                   int(self.getPckNum(), 16) + int(self.data_len, 16)

        l = str2list(self.data, 8)
        for i in l:
            checksum += i

        return str(hex(checksum))[-8:]

    def getFrame(self):
        frame_data = self.head + self.getCmdNum() + self.getCmd() + str(self.pck_num) + \
                     self.data_len + self.data + self.getCheckSum()
        return frame_data

class DecodeProtocol():
    def __init__(self, table = {}):
        self.pck_num = 0
        self.cnt = 0
        self.ch_all_data = ''
        self.ch0_xdata = []
        self.ch0_ydata = []
        self.ch1_xdata = []
        self.ch1_ydata = []
        self.ch2_xdata = []
        self.ch2_ydata = []
        self.ch3_xdata = []
        self.ch3_ydata = []
        self.table = table

    def config(self, frame):
        self.frame = frame

    def getPckNum(self):
        self.pck_num = int(self.frame[32:40], 16)
        return  self.pck_num

    def getDataLen(self):
        self.data_len = int(self.frame[40:48], 16)
        return  self.data_len

    def getCommand(self):
        self.command = self.frame[24:32]
        return  self.command

    def analyzeFrame(self):
        '''
        先收集到一次完整触发上传的数据
        :return:
        '''
        data_len = self.getDataLen()
        pck_num = self.getPckNum()
        data_s = ''
        if self.getCommand() == '80000006':
            # if self.getPckNum() == 0 :
            if self.getDataLen() != 256 : # 这是一次触发数据的最后一帧
                self.ch_all_data += self.frame[48:48+data_len*2]

                if self.ch_all_data.count('eb90a55a0000') == 1:
                    self.ch0_xdata, self.ch0_ydata, self.ch1_xdata, self.ch1_ydata, self.ch2_xdata, self.ch2_ydata, self.ch3_xdata, self.ch3_ydata = self.getChData(self.ch_all_data)
                    self.ch_all_data = ''
                    return True
                else:
                    self.ch_all_data = ''
                    return False
            else:
                if self.getPckNum() == 0:
                    self.ch_all_data += self.frame[48 + 176:560]
                else:
                    self.ch_all_data += self.frame[48:560]

        else:   # 如果一直上传
            self.cnt = 0
            if self.cnt > 2 and pck_num == 0:
                return True
            else:
                return False

    def getChData(self, data):
        pos = data.find('eb90a55a0000')
        laserStartPos = int(data[pos + 12:pos + 16], 16)
        laserLen = int(data[pos + 16:pos + 20], 16)

        ch0_xdata = list(range(laserStartPos, laserStartPos + laserLen))
        data_s = data[pos + 20:pos + 20 + laserLen * 4]
        ch0_ydata = str2list(data_s, 4)

        ch1_xdata = ch0_xdata
        pos = data.find('eb90a55a0f0f')
        data_s = data[pos + 20:pos + 20 + laserLen * 4]
        ch1_ydata = str2list(data_s, 4)

        ch2_xdata = ch0_xdata
        pos = data.find('eb90a55af0f0')
        data_s = data[pos + 20:pos + 20 + laserLen * 4]
        ch2_ydata = str2list(data_s, 4)

        ch3_xdata = ch0_xdata
        pos = data.find('eb90a55affff')
        data_s = data[pos + 20:pos + 20 + laserLen * 4]
        ch3_ydata = str2list(data_s, 4)

        return [ch0_xdata, ch0_ydata, ch1_xdata, ch1_ydata, ch2_xdata, ch2_ydata, ch3_xdata, ch3_ydata]