import paho.mqtt.client as mqtt 
from random import randrange, uniform
import time

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
        #show_data

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
                    receive_data_ctrl[0] = True
                if msg.topic == topics_sub_list[1][0]:
                    receive_data_ctrl[1] = True

        self.client_pc.loop_stop()

if __name__ == "__main__":
    sonar_client_pc = EspMqttComm(client_name)
    sonar_client_pc.connect()
    sonar_client_pc.send_command_to_esp(1, [0xff,0xff,0xff])
    sonar_client_pc.disconnect()
