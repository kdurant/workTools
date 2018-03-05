#-*- coding:utf-8 -*-
from enum import Enum
import numpy as np
import matplotlib.pyplot as plt

# @unique
class Wave(Enum):
    SIN = 1
    COS = 2
    TRIANGLE = 3
    TOOTH = 4
    RANDOM = 5

class Signal(object):
    def __init__(self):
        self.type = Wave.SIN

    """
    :param cycle : 单次周期里有多少个点
    :param type : 波形类型
    :param bias : 偏置
    :param num : 本次产生数据包含几个周期
    :param ad_bit : 根据ad_bit数，可以计算出ad量程
    """
    def config(self, cycle=1000, type = Wave.SIN, bias = 1, num = 1, ad_bit = 10):
        self.cycle = cycle
        self.type = type
        self.num = num
        self.bias = bias
        self.ad_bit = ad_bit-1

    def buildSignal(self):
        if self.type == Wave.SIN:
            r = np.linspace(0, 2*np.pi, self.cycle)
            data = (np.sin(r) + self.bias)*(2**self.ad_bit)
            data = data.astype(int)
            return data

    def oceanTestSignal(self):
        self.cycle = 6000
        for i in range(0, 6000):


        pass

if __name__ == '__main__':
    signal = Signal()
    signal.config(cycle=100, type=Wave.SIN)
    s = signal.buildSignal()
    np.savetxt('numpy.txt', s, '%u')

    plt.plot(s)
    plt.show()
    pass
