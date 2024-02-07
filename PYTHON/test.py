
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
    dev.setTimeouts(10, 10)
    sleep(0.1)
    dev.setBitMode(0xff, 0x00)
    sleep(0.1)
    dev.setBitMode(0xff, 0x40)
    sleep(0.1)
    dev.setUSBParameters(0x10000, 0x10000)
    #dev.setUSBParameters(0x00040, 0x00040)
    sleep(0.1)
    dev.setLatencyTimer(1)
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
    print(f"In Buffer Before Purge: {dev.getQueueStatus()}")
    dev.purge(ftd2xx.defines.PURGE_RX)
    print(f"In Buffer After Purge: {dev.getQueueStatus()}")
    sleep(0.1)
    #print(dev.getQueueStatus())

    #rx_data = dev.read(numBytes,True) 
    #print(dev.getQueueStatus())
    
    start_time = time_ns()
    #print (start_time)

    chunks = []
    bytesLeft = bytesToRead
    read1 = 0
    if dev.getQueueStatus() > 0:
        while bytesLeft > 0:
            if read1%510 >= 1:
                sleep(0.0001)
                print ("Break")
                print(read1)
            chunk = dev.read(bytesLeft,True)
            if not chunk:
                break
            chunks.append(chunk)
            read = len(chunk)
            bytesLeft -= len(chunk)
            print(bytesLeft)
    else:
        print("Buffer empty, no data read.")

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
    testReturn = run_write_test(0x01000)
    testReturnParsed = parseHex(testReturn)
    old_num = 0
    old_num2 = 0
    statData = []
    errorCount = 0

    for i,num in enumerate(testReturnParsed):
        if (num-1==old_num or num-2 == old_num2 or num == 0 or i == 0):
            print(f"{i+1}: {num}")
            statData.append(0)
        else:
            print(f"{i+1}: {num} ----------------ERROR------")
            statData.append(1)
            errorCount += 1
        
        old_num2 = old_num
        old_num = num
        
    print(f"Test finished with {errorCount} errors")


    x = list(range(0,len(statData)))

    plt.plot(x, statData)
    plt.xlabel("Data Address")
    plt.ylabel("Error?")
    plt.show()
    

#USB Param = 64bytes, 7549 errors
#USB Param = 64Kbytes, 7629 errors    