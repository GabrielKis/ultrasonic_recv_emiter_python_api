# Python mqtt-esp_sonar
## Finalidade

A finalidade do repositório é de se comunicar com um firmware que envia e recebe dados de transdutores ultrassonicos. Mais informações para o firmware e placa utilizados estão em:
```
github.com/GabrielKis/ultrasonic_transmiter_receiver
```

## Requisistos

Para utilização é necessário que seja instalado Python3 em um sistema Linux(Ubuntu), de preferência com o gerenciador de pacotes Anaconda/Miniconda. Informações para sua instalação podem ser encontrados em:
```
https://docs.conda.io/en/latest/miniconda.html#linux-installers
```
Após a instalação do Python é necessário obter a aplicação que executa o Broker MQTT (Eclipse-Mosquitto):

```
sudo apt-get install mosquitto
```

Com istto feito basta instalar os pacotes de python necessários ao projeto. Estes pacotes estão em `requirements.txt` e o comando para instalá-los é:

```
pip install -r requirements.txt
```

OBS: Vale lembrar que o arquivo que configura a criação do broker já está existente no projeto (`mosquitto.conf`).
## Utilização

O primeiro passo para realizar a comunicação com a placa é se conectar à rede Wifi que ela gera, de nome `myssid` e senha `mypassword`. Feito este passo o script irá automatizar o resto da comunicação.

O script que deve ser utilizado a fim de realizar a comunicação com a placa é `esp_sonar_api.py`. Para sua controlar seu funcionamento existem os seguintes comandos adicionais:
```
  -h, --help            show this help message and exit
  -r REPEAT_PERIOD, --repeat_period REPEAT_PERIOD
                        Amount of times that the period will be repeated [0-65535]
  --waveform WAVEFORM   Waveform of signal to be sent [sine, triangular and square]
  --duty DUTY           Duty cicle of signal [0-1]
```

Um exemplo de comando a ser usado seria:

```bash
python esp_sonar_api.py -r 60 --waveform sine
```

Este comando iria enviar uma onda senoidal (40kHz) por 60 periodos, como não é controlável o duty cicle de um seno este comando é desnecessário.


