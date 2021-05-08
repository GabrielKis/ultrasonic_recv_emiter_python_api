import argparse
import bluetooth

def send_data_to_esp():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--csv_file", nargs='?', required=False, default='csv_files/sine.csv',
                        help="Path to csv file corresponding to 1 period (40kHz) of signal to be sent")
    parser.add_argument("-r", "--repeat_period", nargs='?', required=False, default='10',
                        help="Amount of times that the period will be repeated")
    parser.add_argument("-p", "--ping", action='store_true',
                        help="Test bluetooth connection to esp32")
    args = parser.parse_args()
    if args.ping:
        #TODO: TESTE DE CONEXAO BLUETOOTH
        print('testar conexao com esp32')
        devices = bluetooth.discover_devices(lookup_names=True)
        print("Devices found: %s" % len(devices))
        for item in devices:
            print(item)

    elif args.csv_file:
        csv_data_string = ''
        with open(args.csv_file, 'r') as csv_input:
            for line in csv_input:
                csv_data_string += line.replace('\n','').replace(',,',',')
        csv_data = csv_data_string.split(',')
        print(csv_data)
        print(len(csv_data))
    else:
        parser.print_help()

if __name__ == "__main__":
    send_data_to_esp()
