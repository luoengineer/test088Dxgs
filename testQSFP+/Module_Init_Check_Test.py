import ctypes
from ctypes import *
import time
import random
import operator
from cmdServ import cmdservdll,Sfp_Factory_Pwd_Entry
from classTestEvb import *
import sys
import math
import os

#Test times
#wr_and_rd_times  = 5
run_time_second = 3600 * 2  # unit : s
# user type for password
is_088_Module = 0
is_other_Module = 1
user_password_type = is_other_Module

#Product list
ComboSfpI2cAddr = [0xA0,0xA2,0xB0,0xB2,0xA4]
SfpI2cAddr = [0xA0,0xA2,0xA4]
XfpI2dAddr = [0xA0,0xA4]

devUsbIndex = 0
devSffChannel = 1
devSfpChannel = 2

#########################################################
#               create object
#########################################################
testEvb = cTestEvb(devUsbIndex)

#########################################################
#               Inner Funtion
#########################################################
def random_int_list(start, stop, length):
  start, stop = (int(start), int(stop)) if start <= stop else (int(stop), int(start))
  length = int(abs(length)) if length else 0
  for i in range(length):
    yield random.randint(start, stop)

def read_A2_92():
    A2RawDataBuff = ctypes.c_ubyte * 1
    A2RawReadByte = A2RawDataBuff()
    print("Read A2 92: ")
    f.write("\nRead A2 92: \n")
    Res = 0xFF
    Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 92, 1, A2RawReadByte)
    if 0 == Res:
        if 1 == A2RawReadByte[0]:
            print('A2[{}]=0x{:0>2X},{}'.format(92, A2RawReadByte[0], 'OK'))
            f.write('A2[{}]=0x{:0>2X},{}\n'.format(92, A2RawReadByte[0], 'OK'))
        else:
            print('A2[{}]=0x{:0>2X},{}'.format(92, A2RawReadByte[0], 'Fail'))
            f.write('A2[{}]=0x{:0>2X},{}\n'.format(92, A2RawReadByte[0], 'Fail'))
    else:
        print('Read A2 92 fail.')
        f.write('Read A2 92 fail.')
        return 'fail'
        #f.close()
        #sys.exit()

def read_rxpower():
    A2RawDataBuff = ctypes.c_ubyte * 2
    A2RawReadByte = A2RawDataBuff()
    print("Read A2 104-105(Rxpower), 099 must be 0x0000  ")
    f.write("Read A2 104-105(Rxpower), 099 must be 0x0000 \n")
    Res = 0xFF
    Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 104, 2, A2RawReadByte)
    if 0 == Res:
        if (0 == A2RawReadByte[0]) and (0 == A2RawReadByte[1]):
            print(
                'A2[{}-{}](Rxpower)=0x{:0>2X},0x{:0>2X}, {}'.format(104, 105, A2RawReadByte[0], A2RawReadByte[1], 'OK'))
            f.write(
                'A2[{}-{}](Rxpower)=0x{:0>2X},0x{:0>2X}, {}'.format(104, 105, A2RawReadByte[0], A2RawReadByte[1], 'OK'))
        else:
            print('A2[{}-{}](Rxpower)=0x{:0>2X},0x{:0>2X}, {}'.format(104, 105, A2RawReadByte[0], A2RawReadByte[1],
                                                                      'Error'))
            f.write('A2[{}-{}](Rxpower)=0x{:0>2X},0x{:0>2X}, {}'.format(104, 105, A2RawReadByte[0], A2RawReadByte[1],
                                                                        'Error'))
    else:
        print('Read A2 104-105 fail.')
        f.write('Read A2 104-105 fail.')
        return 'fail'
        #f.close()
        #sys.exit()

def read_ddmi_case_temperature():
    A2RawDataBuff = ctypes.c_ubyte * 2
    A2RawReadByte = A2RawDataBuff()
    Res = 0xFF
    Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 96, 2, A2RawReadByte)
    if 0 == Res:
        print("Read A2 96-97(case temperature) = 0x{:0>2X},0x{:0>2X} ".format(A2RawReadByte[0], A2RawReadByte[1]))
        f.write("\nRead A2 96-97(case temperature) = 0x{:0>2X},0x{:0>2X} ".format(A2RawReadByte[0], A2RawReadByte[1]))
        caseTemp = A2RawReadByte[0] + A2RawReadByte[1] / 256
        print("Module DDMI case temperature : {} °C".format(caseTemp))
        f.write("\nModule DDMI case temperature : {} °C".format(caseTemp))
    else:
        print("Read DDMI case temperature fail. ")
        f.write("\nRead DDMI case temperature fail. ")
        return 'fail'

def read_ddmi_voltage():
    A2RawDataBuff = ctypes.c_ubyte * 2
    A2RawReadByte = A2RawDataBuff()
    Res = 0xFF
    Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 98, 2, A2RawReadByte)
    if 0 == Res:
        print("Read A2 98-99(supply voltage) = 0x{:0>2X},0x{:0>2X} ".format(A2RawReadByte[0], A2RawReadByte[1]))
        f.write("\nRead A2 98-99(supply voltage) = 0x{:0>2X},0x{:0>2X} ".format(A2RawReadByte[0], A2RawReadByte[1]))
        voltage = (A2RawReadByte[0] * 256 + A2RawReadByte[1]) / 10000
        print("Module DDMI supply voltage : {} V".format(voltage))
        f.write("\nModule DDMI supply voltage : {} V".format(voltage))
        if (voltage <= 0) or ((0 == A2RawReadByte[0]) and (0 == A2RawReadByte[1])):
            return 'Less than 0'
        else:
            return 'OK'
    else:
        print("Read DDMI supply voltage fail. ")
        f.write("\nRead DDMI supply voltage fail. ")
        return 'fail'


def read_ddmi_Txbias():
    A2RawDataBuff = ctypes.c_ubyte * 2
    A2RawReadByte = A2RawDataBuff()
    Res = 0xFF
    Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 100, 2, A2RawReadByte)
    if 0 == Res:
        print("Read A2 100-101(TxBias) = 0x{:0>2X},0x{:0>2X} ".format(A2RawReadByte[0], A2RawReadByte[1]))
        f.write("\nRead A2 A2 100-101(TxBias) = 0x{:0>2X},0x{:0>2X} ".format(A2RawReadByte[0], A2RawReadByte[1]))
        if (0x09 ==  A2RawReadByte[0]) and (0xC4 == A2RawReadByte[1]):
            return 'Default bias'
        bias = (A2RawReadByte[0] * 256 + A2RawReadByte[1]) * 2 / 1000
        print("Module DDMI TX bias : {} mA".format(bias))
        f.write("\nModule DDMI TX bias : {} mA".format(bias))
        #if 0 == bias:
        #    return 'ERROR'
        #else:
        #    return 'OK'
    else:
        print("Read DDMI TX bias fail. ")
        f.write("\nRead DDMI TX bias fail. ")
        return 'fail'


def read_ddmi_TxPower():
    A2RawDataBuff = ctypes.c_ubyte * 2
    A2RawReadByte = A2RawDataBuff()
    Res = 0xFF
    Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 102, 2, A2RawReadByte)
    if 0 == Res:
        print("Read A2 102-103(TxPower) = 0x{:0>2X},0x{:0>2X} ".format(A2RawReadByte[0], A2RawReadByte[1]))
        f.write("\nRead A2 102-103(TxPower) = 0x{:0>2X},0x{:0>2X} ".format(A2RawReadByte[0], A2RawReadByte[1]))
        bias = math.log10((A2RawReadByte[0] * 256 + A2RawReadByte[1]) / 10000) * 10
        print("Module DDMI TX Power : {} dBm".format(bias))
        f.write("\nModule DDMI TX Power : {} dBm".format(bias))
    else:
        print("Read DDMI TX Power fail. ")
        f.write("\nRead DDMI TX Power fail. ")
        return 'fail'

def read_A2_Status():
    A2RawDataBuff = ctypes.c_ubyte * 1
    A2RawReadByte = A2RawDataBuff()
    print("Read A2 110: ")
    f.write("\nRead A2 110: \n")
    Res = 0xFF
    Res = testEvb.objdll.AteIicRandomRead(devUsbIndex, devSffChannel, SfpI2cAddr[1], 110, 1, A2RawReadByte)
    if 0 == Res:
        print('A2[{}]=0x{:0>2X}'.format(110, A2RawReadByte[0]))
        f.write('A2[{}]=0x{:0>2X}\n'.format(110, A2RawReadByte[0]))
    else:
        print('Read A2 110 fail.')
        f.write('Read A2 110 fail.')
        return 'fail'

#########################################################
#               Open USB Device
#########################################################
testEvb.openUsbDevice()

#########################################################
#               Slot Power On
#########################################################
testEvb.AteAllPowerOn()
time.sleep(2)
#########################################################
#               Entry Password
#########################################################
Sfp_Factory_Pwd_Entry(user_password_type)
time.sleep(1)
#########################################################
#               Command Sevices
#########################################################
# Read firmware version
strCmdIn = create_string_buffer(b'MCU_GET_VERSION()')
strCmdOutBuff = ctypes.c_ubyte*64
strCmdOut = strCmdOutBuff()
strFwVer = []
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    strFwVer = [chr(strCmdOut[item]) for item in range(len(strCmdOut)) if 0 != strCmdOut[item]]
else:
    print("Can't get firmware version, stop test ! ")
    sys.exit()
strFwVer = ''.join(strFwVer)

#########################################################
#                 Open File
#########################################################
startTick = time.time()
endTick = startTick + run_time_second
dateTime = time.strptime(time.asctime( time.localtime(startTick)))
dateTime = "{:4}-{:02}-{:02} {:02}:{:02}:{:02}".format(dateTime.tm_year,dateTime.tm_mon,dateTime.tm_mday,dateTime.tm_hour,dateTime.tm_min,dateTime.tm_sec)
testTitle = strFwVer
fileName = strFwVer+'.txt'
f = open(fileName, 'a+')
time.sleep(1)
print("\n****************************************************************************")
print("Module Initial test, start time : {}".format(dateTime))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\nModule Inital test, start time : {}".format(dateTime))
f.write("\n****************************************************************************")
print("Firmware Version : {}".format(testTitle))
f.write('\nFirmware Version : '+testTitle)

strCmdIn = create_string_buffer(b'MCU_GET_TABLE(base,3,4,16)')
strCmdOutBuff = ctypes.c_ubyte * 64
strCmdOut = strCmdOutBuff()
strModuleId = []
retStauts = cmdservdll.SuperCmdSer(strCmdIn, strCmdOut)
if 0 == retStauts:
    strModuleId = [chr(strCmdOut[item]) for item in range(len(strCmdOut)) if 0 != strCmdOut[item]]
    strModuleId = ''.join(strModuleId).split(',')
    print("Module ID : ", end='')
    f.write("\nModule ID : ")
    for item in range(len(strModuleId)):
        if '0xFF' == strModuleId[item]:
            print("{}".format(strModuleId[item]), end='')
            f.write("{}".format(strModuleId[item]))
        else:
            print("{}".format(chr(int(strModuleId[item], 16))), end='')
            f.write("{}".format(chr(int(strModuleId[item], 16))))
else:
    print("Can't get module ID! ")

#for times in range(wr_and_rd_times):
total_times_count = 0
error_times_count = 0
error_times_statistics = []
while time.time() < endTick:
    print("\nRound.{}, POR...".format(total_times_count))
    f.write("\n\nRound.{}, POR...".format(total_times_count))
    # clear factory password
    testEvb.AteAllPowerOff()
    time.sleep(2)
    testEvb.AteAllPowerOn()
    time.sleep(2)

    round_error_times = 0
    ret = read_A2_92()
    if 'fail'== ret:
        error_times_statistics.append(str(total_times_count))
        error_times_statistics.append('Not read A2[92], i2c fail')
        round_error_times += 1
    ret = read_A2_Status()
    if 'fail' == ret:
        error_times_statistics.append(str(total_times_count))
        error_times_statistics.append('Not read A2[110], i2c fail')
        round_error_times += 1
    ret = read_rxpower()
    if 'fail' == ret:
        error_times_statistics.append(str(total_times_count))
        error_times_statistics.append('Not read A2[104-105], i2c fail')
        round_error_times += 1
    ret = read_ddmi_case_temperature()
    if 'fail' == ret:
        error_times_statistics.append(str(total_times_count))
        error_times_statistics.append('Not read A2[96-97], i2c fail')
        round_error_times += 1
    ret = read_ddmi_voltage()
    if 'Less than 0' == ret:
        error_times_statistics.append(str(total_times_count))
        error_times_statistics.append('DDMI Vcc less than 0')
        round_error_times += 1
    elif 'fail' == ret:
        error_times_statistics.append(str(total_times_count))
        error_times_statistics.append('Not read A2[98-99], i2c fail')
        round_error_times += 1
    ret = read_ddmi_Txbias()
    if 'fail' == ret:
        error_times_statistics.append(str(total_times_count))
        error_times_statistics.append('Not read A2[100-101], i2c fail')
        round_error_times += 1
    #    os.system('.\Driver_GN25L96_Init_Test.py')
        
    #read_ddmi_TxPower()
    if round_error_times >= 1:
        error_times_count += 1
    total_times_count += 1

if len(error_times_statistics) > 0:
    #print("\n{}".format(error_times_statistics))
    for item in range(len(error_times_statistics)):
        print("\nError happen in Round {} ".format(len(error_times_statistics)))
        f.write("\n\nError happen in Round {} ".format(len(error_times_statistics)))
    print("\nTotal happen {} times error ".format(error_times_count))
    f.write("\n\nTotal happen {} times error ".format(error_times_count))
else:
    print("\nNo error, total execute Round {} OK . ".format(total_times_count))
    f.write("\n\nNo error, total execute Round {} OK . ".format(total_times_count))

dateTime = time.strptime(time.asctime())
dateTime = "{:4}-{:02}-{:02} {:02}:{:02}:{:02}".format(dateTime.tm_year,dateTime.tm_mon,dateTime.tm_mday,dateTime.tm_hour,dateTime.tm_min,dateTime.tm_sec)
print("\n****************************************************************************")
print("Module Initial test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
print("****************************************************************************")
f.write("\n****************************************************************************")
f.write("\nModule Initial test, end time : {}, elapsed time : {:2d} h {:2d} m {:.02f} s".format(dateTime, int(time.time()-startTick)//3600,int(time.time()-startTick)%3600//60,int(time.time()-startTick)%3600%60))
f.write("\n****************************************************************************")
testEvb.AteAllPowerOff()
f.close()

