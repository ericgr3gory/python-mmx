import time
from datetime import date
from notify import notification

def last_line_of_log(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    return lines[-2].strip()

def current_log_name():
    current_date = date.today()
    log_name = f'/home/ericgr3gory/mmx-node/mainnet/logs/mmx_harvester_{current_date.year}_{current_date.month:02}_{current_date.day:02}.txt'
    return log_name
    

def main():
    while True:
        file = current_log_name()
        line = last_line_of_log(file)
        if 'WARN: connect() failed with: Connection refused' in line:
            print(line)
            notification(line)
        time.sleep(60)
    

if __name__ == "__main__":
   main() 
