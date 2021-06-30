import sys
import subprocess
import numpy as np
from scipy import signal as sg

import argparse
from client_pc_mqtt import EspMqttComm

SAMPLES_PER_PERIOD = 25
MULTIPLIER = 127.5
client_name = 'Client_PC'

def send_data_to_esp():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--repeat_period", required=False, default='10',
                        help="Amount of times that the period will be repeated [0-65535]")
    parser.add_argument("--waveform", required=False, default='sine',
                        help="Waveform of signal to be sent [sine, triangular and square]")
    parser.add_argument("--duty", required=False, default='0.5',
                        help="Duty cicle of signal [0-1]")
    args = parser.parse_args()

    # Inicia broker
    broker_process = subprocess.Popen(['mosquitto', '-c', 'mosquitto.conf'],\
                                        stderr=subprocess.STDOUT)

    try:
        x = np.arange(0,SAMPLES_PER_PERIOD)
        duty_cicle = float(args.duty)
        if args.waveform == 'sine':
            signal_np = (MULTIPLIER * np.sin(2*np.pi*x/SAMPLES_PER_PERIOD)) + MULTIPLIER
            signal_list = signal_np.tolist()
            signal = [round(signal_list) for signal_list in signal_list]
        elif args.waveform == 'triangular':
            signal_np = (MULTIPLIER * sg.sawtooth(2*np.pi*x/SAMPLES_PER_PERIOD, width=duty_cicle)) + MULTIPLIER
            signal_list = signal_np.tolist()
            signal = [round(signal_list) for signal_list in signal_list]
        elif args.waveform == 'square':
            signal_np = (MULTIPLIER * sg.square(2*np.pi*x/SAMPLES_PER_PERIOD, duty=duty_cicle)) + MULTIPLIER
            signal_list = signal_np.tolist()
            signal = [round(signal_list) for signal_list in signal_list]

        sonar_client_pc = EspMqttComm(client_name)
        sonar_client_pc.connect()
        sonar_client_pc.send_command_to_esp(args.repeat_period, signal)
        sonar_client_pc.disconnect()
    except Exception as e:
        print('ERROR:', e)
        return

    # terminar broker
    broker_process.kill()

    # mostra os dados e salva em arquivo CSV
    sonar_client_pc.print_data()

if __name__ == "__main__":
    send_data_to_esp()
