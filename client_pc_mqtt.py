import paho.mqtt.client as mqtt 
from random import randrange, uniform
import matplotlib.pyplot as plt
import mplcursors
import time
import numpy as np
import csv

from queue import Queue

# Configured on the ESP firmware
mqttBroker ="192.168.4.2" 
client_name = "Client_PC"

topics_pub_list = [('config_to_esp', 2)]
topics_sub_list = [('ultrasound_send', 2), ('ultrasound_recv', 2)]

class EspMqttComm():
    def __init__(self, pc_client_name):
        # send and receive params to esp
        self.q = Queue()
        self.client_pc = mqtt.Client(pc_client_name, transport="websockets")
        self.sent_data_wf= []
        #client_pc = mqtt.Client("Client_PC")

    def connect(self):
        self.client_pc.connect(mqttBroker, port=5089)

    def disconnect(self):
        self.client_pc.disconnect()

    def send_command_to_esp(self, qtd_periods, waveform_data):
        #parse input
        payload = (int(qtd_periods)).to_bytes(2, byteorder='big') + bytes(waveform_data)
        #send cmd-waveform
        self._send_data(payload)
        #receive-waveforms
        self._receive_data()
        # create sent_data list
        #for i in range(0,int(qtd_periods)):
        #    self.sent_data_wf += waveform_data
        #    pass
        #fill_zeros = 10000 - len(self.sent_data_wf)
        #zeros_list = [0] * fill_zeros
        #self.sent_data_wf += zeros_list

    def _on_message(self, client, userdata, message):
        self.q.put(message)
        print("{} RECEIVED data from topic: {}".format(client_name, str(message.topic)))

    def _send_data(self, payload):
        self.client_pc.publish(topics_pub_list[0][0], payload, retain=True)
        print("{} PUBLISHED data to topic: {}".format(str(client_name), topics_pub_list[0][0]))

    def _receive_data(self):
        receive_data_ctrl = [False, False]

        self.client_pc.loop_start()

        self.client_pc.subscribe(topics_sub_list)
        self.client_pc.on_message=self._on_message

        # espera ate que os topicos de retorno sejam recebidos
        while not all(receive_data_ctrl):
            if not self.q.empty():
                msg = self.q.get()
                if msg.topic == topics_sub_list[0][0]:
                    #self.tx_waveform_array = np.array(msg.payload)
                    self.tx_waveform_array = list(msg.payload)
                    receive_data_ctrl[0] = True
                if msg.topic == topics_sub_list[1][0]:
                    #self.rx_waveform_array = np.array(msg.payload)
                    self.rx_waveform_array = list(msg.payload)
                    receive_data_ctrl[1] = True

        self.client_pc.loop_stop()

    def print_data(self):
        #print("rx array:", self.rx_waveform_array)
        #print("tx_array:", self.tx_waveform_array)
        #print("len rx:", len(self.rx_waveform_array))
        #print("len tx:", len(self.tx_waveform_array))
        x_rx = range(0,len(self.rx_waveform_array))
        #x_tx = range(0,len(self.tx_waveform_array))
        #print(type(x_rx))
        #print(type(self.sent_data_wf))
        #print(self.sent_data_wf)
        #plt.plot(lookup_table, 'bo')
        print(type(self.rx_waveform_array))
        print(type(self.rx_waveform_array[0]))
        lines = plt.plot(x_rx, self.rx_waveform_array)
        mplcursors.cursor(lines, multiple=True) # or just mplcursors.cursor()
        plt.grid()
        #plt.step(x_rx, self.sent_data_wf)
        plt.ylabel('some numbers')
        plt.show()
        with open('csv_file', 'w') as myfile:
            #wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            for i in self.rx_waveform_array:
                myfile.write(str(i))
                myfile.write(',\n')

if __name__ == "__main__":
    sonar_client_pc = EspMqttComm(client_name)
    sonar_client_pc.connect()
    sonar_client_pc.send_command_to_esp(1, [0xff,0xff,0xff])
    sonar_client_pc.disconnect()
