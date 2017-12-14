# import eraser

# __all__ = ['diskInfo', 'readSector', 'eraserSector']

from .misc import diskInfo, readSector, eraserSector, str2list, timethis

from .protocol import EncodeProtocol, DecodeProtocol

from .udpCore import UdpCore

from .chart import Chart

import logging


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s.%(msecs)d %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='log.log',
                    filemode='w')