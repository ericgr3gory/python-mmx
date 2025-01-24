import time
from datetime import date
from notify import notification
import subprocess
from dotenv import load_dotenv
import os



def last_line_of_log(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    return lines[-2].strip()

def current_log_name():
    current_date = date.today()
    log_name = f'/home/ericgr3gory/mmx-node/mainnet/logs/mmx_harvester_{current_date.year}_{current_date.month:02}_{current_date.day:02}.txt'
    return log_name

def is_node_host_up(host):
    result = subprocess.run(['ping', '-c', '1', host], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        notification(f"{host} is up")
    else:
        notification(f"{host} is down")

        
def main():
    while True:
        file = current_log_name()
        line = last_line_of_log(file)
        if 'WARN:' in line:
            print(line)
            notification(line)
            print(f"node = {os.getenv('NODE_HOST')}")
            is_node_host_up(os.getenv('NODE_HOST'))
        time.sleep(10)
    

if __name__ == "__main__":
    load_dotenv()
    main() 

  