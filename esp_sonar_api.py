import sys
import subprocess
import numpy as np

import argparse
from client_pc_mqtt import EspMqttComm

SINE_LOOK_UP_TABLE = [
    0x80,0x86,0x8c,0x93,0x99,0x9f,0xa5,0xab,
    0xb1,0xb7,0xbd,0xc2,0xc8,0xcd,0xd2,0xd7,
    0xdb,0xe0,0xe4,0xe8,0xeb,0xee,0xf1,0xf4,
    0xf7,0xf9,0xfb,0xfc,0xfd,0xfe,0xff,0xff,
    0xff,0xff,0xfe,0xfd,0xfb,0xfa,0xf8,0xf5,
    0xf3,0xf0,0xed,0xe9,0xe6,0xe2,0xde,0xd9,
    0xd4,0xd0,0xca,0xc5,0xc0,0xba,0xb4,0xae,
    0xa8,0xa2,0x9c,0x96,0x8f,0x89,0x83,0x7c,
    0x76,0x70,0x69,0x63,0x5d,0x57,0x51,0x4b,
    0x45,0x3f,0x3a,0x35,0x2f,0x2b,0x26,0x21,
    0x1d,0x19,0x16,0x12,0x0f,0x0c,0x0a,0x07,
    0x05,0x04,0x02,0x01,0x00,0x00,0x00,0x00,
    0x01,0x02,0x03,0x04,0x06,0x08,0x0b,0x0e,
    0x11,0x14,0x17,0x1b,0x1f,0x24,0x28,0x2d,
    0x32,0x37,0x3d,0x42,0x48,0x4e,0x54,0x5a,
    0x60,0x66,0x6c,0x73,0x79,0x80
]

SAMPLES_PER_PERIOD = 125
MULTIPLIER = 127.5
client_name = 'Client_PC'

def send_data_to_esp():
    parser = argparse.ArgumentParser()
    #parser.add_argument("-f", "--csv_file", nargs='?', required=False, default='csv_files/sine.csv',
    #                    help="Path to csv file corresponding to 1 period (40kHz) of signal to be sent")
    parser.add_argument("-r", "--repeat_period", required=False, default='10',
                        help="Amount of times that the period will be repeated")
    parser.add_argument("--waveform", required=False, default='sine',
                        help="Waveform of signal to be sent (sine, triangular and square)")
    #parser.add_argument("-p", "--ping", action='store_true',
    #                    help="Test bluetooth connection to esp32")
    args = parser.parse_args()

    # iniciar broker
    broker_process = subprocess.Popen(['mosquitto', '-c', 'mosquitto.conf'],\
                                        stderr=subprocess.STDOUT)

    x = np.arange(0,SAMPLES_PER_PERIOD)
    if args.waveform == 'sine':
        # gerar look-up table do seno
        print('gerar onda senoidal')
        signal_np = (MULTIPLIER * np.sin(2*np.pi*x/SAMPLES_PER_PERIOD)) + MULTIPLIER
        signal_list = signal_np.tolist()
        signal = [round(signal_list) for signal_list in signal_list]
    elif args.waveform == 'triangular':
        # gerar look-up table do triangular - com duty
        print('gerar onda triangular')
    elif args.waveform == 'square':
        # gerar look-up table da quadrada - com duty
        print('gerar onda quadrada')

    sonar_client_pc = EspMqttComm(client_name)
    sonar_client_pc.connect()
    sonar_client_pc.send_command_to_esp(args.repeat_period, signal)
    sonar_client_pc.disconnect()

    # terminar broker - como? matando subprocess do python, ou matando o processo diretamente do linux
    broker_process.kill()

if __name__ == "__main__":
    send_data_to_esp()
