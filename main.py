import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from serial import SerialException

import GUI  # файл окна
import COM_PORT  # инициализация ком порта
import time
#from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import log_file
#import pyqtgraph.examples
#pyqtgraph.examples.run()
from random import randint


# класс для доступа к методам класса виджетов


class DEP_AD_Window(QtWidgets.QMainWindow, GUI.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.GraphWidget = pg.PlotWidget(title="Field")
        self.GraphWidget.setBackground('w')
        # self.GraphWidget.setForeground('b')
        # self.GraphWidget.setConfigOption('background','w')
        # self.GraphWidget.setConfigOption('foreground', 'b')

        self.frame_layout = QtWidgets.QVBoxLayout()  # создаем контейнер куда потом вставим виджет
        self.frame.setLayout(self.frame_layout)  # вставляем наш контейнер (layout) в рамку которую создали в
        #  QtDesigner
        self.frame_layout.addWidget(self.GraphWidget)  # а теперь можно вставить наш виджет

        self.com_port = COM_PORT.OaiSerial()
        self.port_flag = self.com_port.open_id()
        self.com_port.baudrate = 28800


        if (self.port_flag):
            self.com_port.error_string = "Подключение к COM порту успешно, измерения не производятся"
            #print(self.port_flag)
            try:
                self.com_port.open()
            except  SerialException:
                self.com_port.error_string = "COM порт используется другой программой"
        else:
            self.com_port.error_string = "Ошибка подключения к COM порту, проверьте кабель"
            self.Cycle_mesurement_status = 0

        self.connection_string.setText(self.com_port.error_string)

        self.Connection_Button.clicked.connect(self.connect_to_com_port)
        self.Cycle_measurement_button.clicked.connect(self.start_mesure)
        #self.Cycle_measurement_button.setStyleSheet('QPushButton {background-color: gray;}')
        self.Cycle_mesurement_status = 0
        self.time = [1]  # 100 time points
        self.DEP_1_Field = [0]  # 100 data points
        self.DEP_2_Field = [0]  # 100 data points
        self.DEP1_Freq = 0
        self.DEP2_Freq = 0
        self.Freq_read_flag = 0
        DEP_1_data = pg.mkPen(color='r')
        DEP_2_data = pg.mkPen(color='b')
        self.graph_data_1 = self.GraphWidget.plot(self.time, self.DEP_1_Field, pen=DEP_1_data)
        self.graph_data_2 = self.GraphWidget.plot(self.time, self.DEP_2_Field, pen=DEP_2_data)


        self.timer_data = QtCore.QTimer()
        self.timer_data.setInterval(2000)
        self.timer_data.timeout.connect(self.update_plot_data)

        self.timer_plot = QtCore.QTimer()
        self.timer_plot.setInterval(50)
        self.timer_plot.timeout.connect(self.update_plot)
        self.timer_plot.start()

        self.row_data = b''
        # commands
        self.synchro_1 = bytearray([0x01, 0x31, 0x30, 0x36, 0x30, 0x30, 0x30, 0x03])  # ДЭП-АД 1
        self.res_1 = bytearray([0x01, 0x31, 0x30, 0x36, 0x37, 0x30, 0x30, 0x03])  # ДЭП-АД 1
        self.synhro_continious = bytearray([0x01, 0x31, 0x30, 0x36, 0x30, 0x30, 0x31, 0x03])
        self.synhro_continious_stop = bytearray([0x01, 0x31, 0x30, 0x36, 0x30, 0x30, 0x30, 0x03])
        self.answer_synhro_continious = bytearray([0x01, 0x30, 0x31, 0x36, 0x30, 0x30, 0x31, 0x03])
        self.read_data = bytearray([0x01, 0x31, 0x30, 0x36, 0x41, 0x30, 0x30, 0x03])
        self.data_answer_mask = bytearray([0x02, 0x30, 0x31, 0x36, 0x41, 0x30, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                           0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03])
        self.data_answer_mask_simple_read_data = bytearray(
            [0x02, 0x30, 0xFF, 0x36, 0x41, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x30, 0x30, 0x30, 0x30, 0x30,
             0x30, 0x30, 0x30, 0x03])
        # ascii словарь
        self.ascii_to_num = {0x30: 0x0, 0x31: 0x1, 0x32: 0x2, 0x33: 0x3, 0x34: 0x4, 0x35: 0x5, 0x36: 0x6, 0x37: 0x7, 0x38: 0x8, 0x39: 0x9,
                             0x41: 0xA, 0x42: 0xB, 0x43: 0xC, 0x44: 0xD, 0x45: 0xE, 0x46: 0xF}
    def read_field_DEP_AD(self, command):

        try:
            # DEP_AD7_result = [0x01, 0x37, 0x30, 0x36, 0x37, 0x30, 0x30, 0x03]
            self.com_port.reset_input_buffer()
            self.com_port.write(command)
            time.sleep(0.01)
            dummy_read = self.com_port.read(8)
            row_data = self.com_port.read(22)
            if (row_data[0:2] == self.data_answer_mask_simple_read_data[0:2]) and (row_data[2:3] == command[1:2]) and (row_data[-1:] == self.data_answer_mask_simple_read_data[-1:]):
                print("ок")
                F1_dep_ad = int(row_data[7:9], 16)
                E1_dep_ad_row = int(row_data[5:7], 16)
                F2_dep_ad = int(row_data[11:13], 16)
                E2_dep_ad_row = int(row_data[9:11], 16)
                #E1_dep_ad = self.pars_filed(E1_dep_ad_row)
                #E2_dep_ad = self.pars_filed(E2_dep_ad_row)
                self.DEP1_Freq = F1_dep_ad
                self.DEP2_Freq = F2_dep_ad
                #return F1_dep_ad, E1_dep_ad, F2_dep_ad, E2_dep_ad
            else:
                print(" не ок")
                self.com_port.reset_input_buffer()
                return 0, 0, 0, 0
                pass
        except Exception as error:
            print(error)
        pass



    def update_plot_data(self):
        try:
            self.com_port.reset_input_buffer()
            self.com_port.write(self.read_data)
            dummy_read = self.com_port.read(len(self.read_data))
            #print(dummy_read)
            self.row_data = self.com_port.read(len(self.data_answer_mask))
            #a = self.com_port.bytes_to_list(self.row_data)
            if (self.row_data[0:5] != self.data_answer_mask[0:5]) and (self.row_data[-1] != self.data_answer_mask[-1]) or (self.row_data == None):
                self.com_port.error_string = "Ошибка подключения к ДЭП-АД, устройство не отвечает, проверьте устройство и " \
                                             "подключите заново "
                self.connection_string.setText(self.com_port.error_string)
                self.Cycle_mesurement_status = 0

            else:
                if self.row_data[5:21] == b'FAFAFAFAFAFAFAFA':
                    pass
                else:
                    #print(self.row_data[5:21])
                    '''
                    row_1 = self.ascii_to_num[self.row_data[7]] << 8 | self.ascii_to_num[self.row_data[5]] << 4 | self.ascii_to_num[self.row_data[6]]
                    row_2 = self.ascii_to_num[self.row_data[8]] << 8 | self.ascii_to_num[self.row_data[9]] << 4 | self.ascii_to_num[self.row_data[10]]
                    '''
                    row_1 = int((self.row_data[7:8] + self.row_data[5:7]), base=16)
                    #row_1 = int(self.row_data[7:8], base=16) << 8 | int(self.row_data[5:7], base=16)
                    row_2 = int(self.row_data[8:11], base=16)
                    row_3 = int(self.row_data[15:16], base=16) << 8 | int(self.row_data[13:15], base=16)
                    row_4 = int(self.row_data[16:19], base=16)
                    if(row_1 & 0x800):
                        sign_1 = -1
                    else:
                        sign_1 = 1
                    if (row_2 & 0x800):
                        sign_2 = -1
                    else:
                        sign_2 = 1
                    if (row_3 & 0x800):
                        sign_3 = -1
                    else:
                        sign_3 = 1
                    if (row_4 & 0x800):
                        sign_4 = -1
                    else:
                        sign_4 = 1
                    row_1 = sign_1 * (row_1 & 0x7FF)
                    row_2 = sign_2 * (row_2 & 0x7FF)
                    row_3 = sign_3 * (row_3 & 0x7FF)
                    row_4 = sign_4 * (row_4 & 0x7FF)

                    if(len(self.time)<100):
                        self.time.append(self.time[-1] + 1)  # Add a new value 1 higher than the last.
                        self.time.append(self.time[-1] + 1)  # Add a new value 1 higher than the last.
                        self.DEP_1_Field.append(row_1)  # Add a new random value.
                        self.DEP_1_Field.append(row_3)  # Add a new random value.
                        self.DEP_2_Field.append(row_2)  # Add a new random value.
                        self.DEP_2_Field.append(row_4)  # Add a new random value.
                    else:
                        self.time = self.time[2:]  # Remove the first y element.
                        self.time.append(self.time[-1] + 1)  # Add a new value 1 higher than the last.
                        self.time.append(self.time[-1] + 1)  # Add a new value 1 higher than the last.
                        self.DEP_1_Field = self.DEP_1_Field[1:]  # Remove the first
                        self.DEP_1_Field.append(row_1)  # Add a new random value.
                        self.DEP_1_Field = self.DEP_1_Field[1:]  # Remove the first
                        self.DEP_1_Field.append(row_3)  # Add a new random value.
                        self.DEP_2_Field = self.DEP_2_Field[1:]  # Remove the first
                        self.DEP_2_Field.append(row_2)  # Add a new random value.
                        self.DEP_2_Field = self.DEP_2_Field[1:]  # Remove the first
                        self.DEP_2_Field.append(row_4)  # Add a new random value.
                    if self.Freq_read_flag == 0:
                        self.read_field_DEP_AD(self.res_1)
                        if(self.DEP1_Freq == 0 or self.DEP2_Freq == 0 ):
                            self.Freq_read_flag = 0
                        else:
                            self.Freq_read_flag = 1
                        #print('nen')
                        pass
                    else:
                        pass
                    self.mode_string.setText('ДЭП 1' + '\t' + str(self.DEP1_Freq) + '\t'+ str(row_1) +'|'+ str(row_3) + '\t' + 'ДЭП 2' + '\t' + str(self.DEP2_Freq) + '\t'+ str(row_2) +'|'+ str(row_4))
                    file_dep_1 = log_file.open_log_file(self.file_handle_1)
                    time_moment_1 = time.localtime()
                    time_moment_2 = time.localtime(time.mktime(time_moment_1)-1)
                    file_dep_1.write(time.strftime("%H-%M-%S ", time_moment_2) + '\t' + str(row_1) + '\n')
                    file_dep_1.write(time.strftime("%H-%M-%S ", time_moment_1) + '\t' + str(row_3) + '\n')
                    log_file.close_log_file(self.file_handle_1)
                    file_dep_2 = log_file.open_log_file(self.file_handle_2)
                    file_dep_2.write(time.strftime("%H-%M-%S ", time_moment_2) + '\t' + str(row_2) + '\n')
                    file_dep_2.write(time.strftime("%H-%M-%S ", time_moment_1) + '\t' + str(row_4) + '\n')
                    log_file.close_log_file(self.file_handle_2)
                    print(row_1, row_2, row_3, row_4)
                    pass


        except IndexError:
            self.com_port.error_string = "Ошибка подключения к ДЭП-АД, устройство не отвечает, проверьте устройство и подключите заново"
            self.connection_string.setText(self.com_port.error_string)
            self.Cycle_mesurement_status = 0
        except Exception as error:
            print(error, "update_plot_data")

    def update_plot(self):
        self.graph_data_1.setData(self.time, self.DEP_1_Field)  # Update the data.
        self.graph_data_2.setData(self.time, self.DEP_2_Field)  # Update the data.

    def start_mesure(self):
        try:
            self.com_port.reset_input_buffer()
            if self.Cycle_mesurement_status == 0:

                self.com_port.write(self.synhro_continious)
                dummy_read = self.com_port.read(len(self.synhro_continious))
                answer = self.com_port.read(len(self.answer_synhro_continious))
                if (answer != self.answer_synhro_continious):
                    self.com_port.error_string = "Ошибка подключения к ДЭП-АД, устройство не отвечает, проверьте устройство и подключите заново"
                    self.Cycle_mesurement_status = 0
                    self.connection_string.setText(self.com_port.error_string)

                else:
                    #self.Cycle_measurement_button.setStyleSheet('QPushButton {background-color: green;}')
                    self.Cycle_mesurement_status = 1
                    self.com_port.error_string = "Подключение в порядке, непрерывный режим запущен"
                    self.Cycle_measurement_button.setText("Остановить измерения")
                    self.connection_string.setText(self.com_port.error_string)
                    self.file_handle_1, self.log_dir_1 = log_file.create_log_file(prefix="DEP_1_Data", extension=".txt")
                    self.file_handle_2, self.log_dir_2 = log_file.create_log_file(prefix="DEP_2_Data", extension=".txt")
                    self.timer_data.start()
            elif self.Cycle_mesurement_status == 1:

                self.com_port.write(self.synchro_1)
                dummy_read = self.com_port.read(len(self.synchro_1))
                answer = self.com_port.read(len(self.answer_synhro_continious))
                self.Cycle_mesurement_status = 0
                self.Freq_read_flag = 0
                self.timer_data.stop()
                self.com_port.error_string = "Подключение в порядке, непрерывный режим остановлен, дождитесь окончания измерений"
                self.Cycle_measurement_button.setText("Запустить измерения")
                self.connection_string.setText(self.com_port.error_string)
                #self.Cycle_measurement_button.setStyleSheet('QPushButton {background-color: gray;}')
                pass


        except Exception as error:
            print(error, "start_mesure")

    def reconnect(self):
        self.disconnect()
        self.serial.open_id()
        pass

    def disconnect(self):
        self.serial._close_event.set()
        time.sleep(0.1)
        del self.serial
        pass

    def connect_to_com_port(self):
        try:
            self.com_port.close()
            self.DEP_COM = self.com_port.open_id()
            if (self.DEP_COM):
                self.com_port.error_string = "Подключение к COM порту успешно, измерения не производятся"
                self.com_port.baudrate = 28800
                self.com_port.open()
            else:
                self.com_port.error_string = "Ошибка подключения к COM порту, проверьте кабель"
                self.Cycle_mesurement_status = 0
            self.connection_string.setText(self.com_port.error_string)
            pass
        except Exception as error:
            print(error)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = DEP_AD_Window()
    window.show()
    app.exec_()


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
