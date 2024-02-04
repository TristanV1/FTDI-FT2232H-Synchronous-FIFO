
from time import sleep
from time import time_ns
import random
import ftd2xx
import matplotlib.pyplot as plt
import numpy as np


BLOCK_LEN = 2048 * 32

def init():
    dev = ftd2xx.openEx(b'FT73YTN0A')
    sleep(0.1)
    dev.setTimeouts(5000, 5000)
    sleep(0.1)
    dev.setBitMode(0xff, 0x00)
    sleep(0.1)
    dev.setBitMode(0xff, 0x40)
    sleep(0.1)
    dev.setUSBParameters(0x10000, 0x10000)
    sleep(0.1)
    dev.setLatencyTimer(2)
    sleep(0.1)
    dev.setFlowControl(ftd2xx.defines.FLOW_RTS_CTS, 0, 0)
    sleep(0.1)
    dev.purge(ftd2xx.defines.PURGE_RX)
    sleep(0.1)
    dev.purge(ftd2xx.defines.PURGE_TX)
    sleep(0.1)
    return dev

def run_write_test(bytesToRead):
    dev = init()
    print("\nDevice Details :")
    print("Serial : " , dev.getDeviceInfo()['serial'])
    print("Type : " , dev.getDeviceInfo()['type'])
    print("ID : " , dev.getDeviceInfo()['id'])
    print("Description : " , dev.getDeviceInfo()['description'])
    print("TEST : " , dev.getDeviceInfo()['description'])

    i = 0
    numBytes = bytesToRead
    
    data = [i % 256 for i in range(numBytes)]

    print("\n \n")
    dev.purge(ftd2xx.defines.PURGE_RX)
    sleep(0.1)
    #print(dev.getQueueStatus())

    #rx_data = dev.read(numBytes,True) 
    #print(dev.getQueueStatus())
    
    start_time = time_ns()
    #print (start_time)

    chunks = []
    while numBytes > 0:
        chunk = dev.read(numBytes,True)
        #print(chunk)
        #print(dev.getQueueStatus())
        chunks.append(chunk)
        numBytes -= len(chunk)

    end_time = time_ns()-start_time
    #print(time_ns())

    combine_chunks = [b for chunk in chunks for b in chunk]
    run_time_s = end_time*float(10.0**-9)

    print(f"Run Time: {run_time_s}")
    
    #bit_rate = float(len(combine_chunks)) / run_time_s
    #print("Bit rate: (%.06f Mbps)" % (bit_rate*(10.0**-6)))

    #print(f"Bit rate: {float(numBytes*8)/float(end_time)}Mbps")

    #print(f"Reading {numBytes} Bytes")
    #print(rx_data)

    dev.close()
    print("\nWrite Test Finished Successfully\n")

    return(combine_chunks)

def parseHex(hexDump):
    return([ord(c) for c in hexDump] if type(hexDump) is str else list(hexDump))




if __name__ == "__main__":
    testReturn = run_write_test(65523)
    testReturnParsed = parseHex(testReturn)
    old_num = 0
    
    statData = []

    for i,num in enumerate(testReturnParsed):
        if (num-1==old_num):
            print(f"{i+1}: {num}")
            statData.append(0)
        else:
            print(f"{i+1}: {num} ----------------ERROR------")
            statData.append(10)
        
        old_num = num

    x = list(range(0,len(statData)))

    plt.plot(x, statData)
    plt.show()