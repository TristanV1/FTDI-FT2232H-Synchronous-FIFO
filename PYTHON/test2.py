
import ftd2xx as ft
from time import time, sleep

KiB = 1024
MiB = KiB * 1024


class FPGA:
    def __init__(self, ftdi_serial, fifo245_mode):
        self.ftdi_serial = ftdi_serial
        self.fifo245_mode = fifo245_mode

    def __enter__(self):
        try:
            ftdev_id = ft.listDevices().index(self.ftdi_serial)
            #print(ft.listDevices().index(self.ftdi_serial))
        except ValueError:
            raise Exception("No board found!")
        self.ftdev = ft.open(ftdev_id)
        print(ftdev_id)
        self.ftdev.resetDevice()
        self.ftdev.purge()
        # AN130 for more details about commands below
        self.ftdev.setBitMode(0xff, 0x40 if self.fifo245_mode == 'sync' else 0x00)
        self.ftdev.setTimeouts(10, 10)  # in ms
        self.ftdev.setUSBParameters(0x10000)  # set rx, tx buffer size in bytes
        self.ftdev.setFlowControl(ft.defines.FLOW_RTS_CTS, 0, 0)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ftdev.close()

    def __cmd(self, code, data):
        return ((0xAA << 56) | (code << 40) | (data << 8) | 0x55).to_bytes(8, 'little')

    def test_led(self):
        self.ftdev.write(self.__cmd(0x1ED0, 1))
        sleep(2)
        self.ftdev.write(self.__cmd(0x1ED0, 0))
        sleep(2)

    def test_read(self, total_bytes):
        # Prepare data
        golden_data = [i % 256 for i in range(total_bytes)]

        # Start read test
        #self.ftdev.write(self.__cmd(0xBEEF, total_bytes - 1))

        # Receive data
        chunks = []
        start_time = time()
        while total_bytes > 0:
            print(self.ftdev.getQueueStatus())
            chunk = self.ftdev.read(total_bytes,False)
            if not chunk:
                break
            chunks.append(chunk)
            total_bytes -= len(chunk)
        

        data = [b for chunk in chunks for b in chunk]
        data2 = [ord(c) for c in data] if type(data) is str else list(data)
        #print(data2)        
        exec_time = time() - start_time
        
            #Print statistics
          # flatten all chunks
        data_len = len(data)
        data_len_mb = data_len / MiB
        print("Read %.02f MiB (%d bytes) from FPGA in %f seconds (%.02f MiB/s)" %
              (data_len_mb, data_len, exec_time, data_len_mb / exec_time))
#
        ## Verify data
        #print("Verify data: %s" % ('ok' if golden_data == data else 'error'))

with FPGA(ftdi_serial=b'FT73YTN0A', fifo245_mode='sync') as de10lite:
    print("START")
    #de10lite.test_led()
    data = de10lite.test_read(65532)
    #de10lite.test_write(100 * MiB)
    print("DONE")