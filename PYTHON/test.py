
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
    dev.setTimeouts(500, 500)
    sleep(0.1)
    dev.setBitMode(0xff, 0x00)
    sleep(0.1)
    dev.setBitMode(0xff, 0x40)
    sleep(0.1)
    dev.setUSBParameters(0x0000FA0, 0x0000FA0)
    #dev.setUSBParameters(0x00040, 0x00040)
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

def run_write_test(bytesToRead = 0, getBitRate = False,getDetails = False):
    dev = init()
    sleep(0.1)
    
    if (getDetails):
        print("\nDevice Details :")
        print("Serial : " , dev.getDeviceInfo()['serial'])
        print("Type : " , dev.getDeviceInfo()['type'])
        print("ID : " , dev.getDeviceInfo()['id'])
        print("Description : " , dev.getDeviceInfo()['description'])
        print("TEST : " , dev.getDeviceInfo()['description'])

        numBytes = bytesToRead

        print("\n \n")
        print(f"In Buffer Before Purge: {dev.getQueueStatus()}")
        dev.purge(ftd2xx.defines.PURGE_RX)
        print(f"In Buffer After Purge: {dev.getQueueStatus()}")

        print(f"Reading {numBytes} Bytes")
        

    chunks = []
    bytesLeft = bytesToRead
    

    start_time = time_ns()
    if dev.getQueueStatus() > 0:
        while bytesLeft > 0:
            chunk = dev.read(bytesLeft,True)
            if not chunk:
                break
            chunks.append(chunk)
            bytesLeft -= len(chunk)
            #print(bytesLeft)
    else:
        print("Buffer empty, no data read.")

    combine_chunks = [b for chunk in chunks for b in chunk]
    
    end_time0 = time_ns()
    if (getBitRate):
        end_time = end_time0 - start_time

        run_time_s = end_time*float(10.0**-9)

        print(f"Run Time: {run_time_s}")

        bit_rate = float(len(combine_chunks)) / run_time_s
        print("Bit rate: (%.06f Mbps)" % (bit_rate*(10.0**-6)))
    else:
        bit_rate = 0


    dev.close()
    #print("\nWrite Test Finished Successfully\n")

    return(combine_chunks,bit_rate*(10.0**-6))

def parseHex(hexDump):
    return([ord(c) for c in hexDump] if type(hexDump) is str else list(hexDump))


def testbench(getBitRate = False,printErrors = False,writeToLog = False,getStats = True,getPlot = False):
    testReturn,bit_rate = run_write_test(0x0003200,getBitRate)
    testReturnParsed = parseHex(testReturn)
    old_num = 0
    old_num2 = 0
    statData = []
    errorCount = 0

    log = open("log.txt","a")

    for i,num in enumerate(testReturnParsed):
        if (num-1==old_num or num-2 == old_num2 or num == 0 or i == 0):
            if (printErrors):
                print(f"{i+1}: {num}")
            if (writeToLog):
                log.write(f"{i+1}: {num}\n")
            statData.append(0)
        else:
            if (printErrors):
                print(f"{i+1}: {num} ----------------ERROR------")
            if (writeToLog):
                log.write(f"{i+1}: {num} ----------------ERROR------\n")
            statData.append(1)
            errorCount += 1
        
        old_num2 = old_num
        old_num = num

    log.close()

    if (getStats):
        print(f"Test finished with {errorCount} errors")
    if (getBitRate):
        print(f"Achieved {round(bit_rate,2)} Mbps")
        print(f"         {round(bit_rate/8,2)} MBps")


    if (getPlot):
        x = list(range(0,len(statData)))

        plt.plot(x, statData)
        plt.xlabel("Data Address")
        plt.ylabel("Error?")
        plt.show()

    return(errorCount)

if __name__ == "__main__":
    
    isError = False
    run = 0
    Errors = 0

    while(not isError):
        run += 1
        Errors = testbench(getStats = True, printErrors=False) >= 1
        isError = Errors >= 1
        print(run)

    print(f"{run} runs until error. \nTotal Errors: {Errors}")
    

#USB Param = 64bytes, 7549 errors
#USB Param = 64Kbytes, 7629 errors    