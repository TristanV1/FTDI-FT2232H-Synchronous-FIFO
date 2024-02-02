
import time
import random

import ftd2xx

BLOCK_LEN = 2048 * 32

def init():
    dev = ftd2xx.openEx(b'FT73YTN0A')
    time.sleep(0.1)
    dev.setTimeouts(5000, 5000)
    time.sleep(0.1)
    dev.setBitMode(0xff, 0x00)
    time.sleep(0.1)
    dev.setBitMode(0xff, 0x40)
    time.sleep(0.1)
    dev.setUSBParameters(0x10000, 0x10000)
    time.sleep(0.1)
    dev.setLatencyTimer(2)
    time.sleep(0.1)
    dev.setFlowControl(ftd2xx.defines.FLOW_RTS_CTS, 0, 0)
    time.sleep(0.1)
    dev.purge(ftd2xx.defines.PURGE_RX)
    time.sleep(0.1)
    dev.purge(ftd2xx.defines.PURGE_TX)
    time.sleep(0.1)
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

    print("\n \n \n \n")
    dev.purge(ftd2xx.defines.PURGE_RX)
    time.sleep(0.1)
    #print(dev.getQueueStatus())

    rx_data = dev.read(numBytes,True) 
    #print(dev.getQueueStatus())
    chunks = []
    while numBytes > 0:
        chunk = dev.read(numBytes,False)
        #print(chunk)
        #print(dev.getQueueStatus())
        chunks.append(chunk)
        numBytes -= len(chunk)

    combine_chunks = [b for chunk in chunks for b in chunk]

    #print(f"Reading {numBytes} Bytes")
    #print(rx_data)

    dev.close()
    print("\nWrite Test Finished Successfully\n")

    return(combine_chunks)

def parseHex(hexDump):
    return([ord(c) for c in hexDump] if type(hexDump) is str else list(hexDump))




if __name__ == "__main__":
    testReturn = run_write_test(65532)
    testReturnParsed = parseHex(testReturn)

    for i,num in enumerate(testReturnParsed):
        print(f"{i+1}: {num}")