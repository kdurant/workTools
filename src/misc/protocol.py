#-*- coding:utf-8 -*-

from src import str2list

class EncodeProtocol():
    def __init__(self):
        self.pck_num = 8*'0'

        self.table = {
            '系统复位'      : '50000001',
            '读取设备参数'  : '50000002',
            '透传激光参数'  : '50000003',
            '激光重频'      : '50000004',
            '激光器开关'    : '50000005',
            'AD起始位置'    : '50000006',
            'AD采样长度'    : '50000007',
            'AD采集状态'    : '50000008'
        }

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
    def __init__(self):
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
        self.table = {
            'AD采样长度'    : 'a0000007',
            'AD采集状态'    : 'a0000008'
        }
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
        data_len = self.getDataLen()
        pck_num = self.getPckNum()
        data_s = ''
        if self.getCommand() == 'a0000008':
            if self.getPckNum() == 0 :
                if len(self.ch_all_data) != 0:   # 需要处理已经接受到一次采集数据
                    ch_len = len(self.ch_all_data)
                    self.ch0_xdata = list(range(0, ch_len//16))
                    data_s = self.ch_all_data[0:ch_len//4]
                    self.ch0_ydata = str2list(data_s, 4)

                    self.ch1_xdata = self.ch0_xdata
                    data_s = self.ch_all_data[ch_len // 4:ch_len // 2]
                    self.ch1_ydata = str2list(data_s, 4)

                    self.ch2_xdata = self.ch0_xdata
                    data_s = self.ch_all_data[ch_len // 2:ch_len // 2+ch_len // 4]
                    self.ch2_ydata = str2list(data_s, 4)

                    self.ch3_xdata = self.ch0_xdata
                    data_s = self.ch_all_data[ch_len // 2 + ch_len // 4:]
                    self.ch3_ydata = str2list(data_s, 4)
                    self.ch_all_data = ''

                    self.ch_all_data += self.frame[48:560]
                    return True
                else:           # 第一次收到上传数据
                    self.ch_all_data += self.frame[48:560]
            else:
                if data_len == 256:
                    self.ch_all_data += self.frame[48:560]
                else:
                    self.ch_all_data += self.frame[48:48+data_len*2]

        else:   # 如果一直上传
            self.cnt = 0
            if self.cnt > 2 and pck_num == 0:
                return True
            else:
                return False

