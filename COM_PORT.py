import serial
import serial.tools.list_ports
import time


class OaiSerial(serial.Serial):
    def __init__(self, **kw):
        serial.Serial.__init__(self)
        self.serial_numbers = ['AH06VN4LA', 'AH06VN4MA', 'A2002IV5A']  # это лист возможных серийников!!! (не строка)
        self.baudrate = 28800
        self.timeout = 1
        self.self_id = 0x00
        self.dev_id = 0x00
        self.seq_num = 0
        self.port = "COM0"
        self.row_data = b""
        self.state = 0
        for key in sorted(kw):
            if key == "serial_numbers":
                self.serial_numbers = kw.pop(key)
            elif key == "baudrate":
                self.baudrate = kw.pop(key)
            elif key == "timeout":
                self.baudrate = kw.pop(key)
            elif key == "port":
                self.baudrate = kw.pop(key)
            elif key == "self_id":  
                self.self_id = kw.pop(key)
            elif key == "dev_id":
                self.dev_id = kw.pop(key)
            elif key == "data":
                self.data = kw.pop(key)
            else:
                pass
        self.error_string = "Нет ошибок"
        self.temperature_pars_data = {}
        self.sensors_numbers = 0

    def open_id(self):
        try:
            port_device = ''
            self.port_flag = 0
            # List ports for user to select
            com_list = serial.tools.list_ports.comports()
            print('\nDetected the following serial ports:')
            for com in com_list:
                print('Port:%s\tID#:=%s' % (com.device, com.serial_number))
                for ID in self.serial_numbers:
                    if com.serial_number is not None:
                        if (com.serial_number.__str__()[:len(ID)] == ID):  # Match ID with the correct port
                            self.port = com.device  # Store the device name to later open port with.
                            self.port_flag = 1
                            break
            if self.port_flag:
                print('\r\n%s is the correct port.' % (self.port))
                return True
            else:
                print("Port with correct ID: %s is not found!")
                return False
        except Exception as error:
            print(error)

    def serial_close(self):
        self.close()


    def bytes_to_string(self, data):
        bytes_str = ""
        for i in range(len(data)):
            bytes_str += '%02x ' % (data[i])
        return bytes_str

    def bytes_to_list(self, data):
        bytes_list = []
        for i in range(len(data)):
            bytes_list.append(data[i])
        return bytes_list