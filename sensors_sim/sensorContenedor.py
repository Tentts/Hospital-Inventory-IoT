import random
import sys
import time
import subprocess
import os

username = "cliente2"
passwd = "scopass2"
apikey = "4jggokgpepnvsb2uv4s40d59ov"


def args_handler():
    if(len(sys.argv) == 3):
        sensorName = sys.argv[1]
        refreshTime = sys.argv[2]
    else:
        print("ERROR WORNG ARGUMENTS. USAGE: python3 sensorPublish.py <sensor name> <refresh time in seconds for publisher>")
        sys.exit(0)
    return sensorName, int(refreshTime)


def getMessage():
    message = ""
    return message


def main():

    sensorName, refreshTime = args_handler()

    command = "mosquitto_pub"

    while True:
        tValue = random.randint(-30, 5)
        hValue = random.randint(5, 30)
        tim = time.localtime()
        current_time = time.strftime("%H:%M:%S", tim)

        print(f"[{current_time}] Updating ({sensorName}): t {tValue} / h {hValue}")
        # Execute command
		# sudo mosquitto_pub -u cliente2 -P scopass2 --cafile ca.crt --cert client2.crt 
		# --key client2.key -d -h localhost -p 8883 -t /4jggokgpepnvsb2uv4s40d59ov/Contenedor001/attrs -m "t|-3|h|23"
        exec = [command, "-u", username, "-P", passwd, "--cafile", "ca.crt", "--cert", "client2.crt", "--key", "client2.key",
                "-h", "localhost", "-p", "8883", "-t", f"/{apikey}/{sensorName}/attrs", "-m", f"t|{tValue}|h|{hValue}", "-d"]

        subprocess.run(exec, stdout=open(os.devnull, 'wb'))
        print(f"[{current_time}] Updated ({sensorName}).")
        time.sleep(refreshTime)


if __name__ == '__main__':
    main()

sys.exit(0)
