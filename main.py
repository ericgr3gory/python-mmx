import time
from datetime import date
from notify import notification
import subprocess
from dotenv import load_dotenv
import os
from home_assisstant import mmx_switch



def last_line_of_log(filename):
    try:
        with open(filename, "rb") as log:
            log.seek(-2, os.SEEK_END)
            
            while log.read(1) != b"\n":
                log.seek(-2, os.SEEK_CUR)
            
            return log.readline().decode().strip()
            

    except (OSError, IndexError):
        return ""
    
def current_log_name():
    current_date = date.today()
    log_name = f'mmx_harvester_{current_date.year}_{current_date.month:02}_{current_date.day:02}.txt'
    return log_name

def is_node_host_up(host):
    result = subprocess.run(['ping', '-c', '1', host], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        notification(f"{host} is up")
        return True
    else:
        notification(f"{host} is down")
        return False
    
def powercycle_node_host():
    if mmx_switch('turn_off'):
        time.sleep(3)
        if mmx_switch('turn_on'):
            timeout = 360  # Timeout period in seconds (e.g., 5 minutes)
            interval = 5  # Interval between checks in seconds
            start_time = time.time()
            while not is_node_host_up(NODE_HOST):
                if time.time() - start_time > timeout:
                    print("Timeout: Node host did not come up within the expected time.")
                    return False
                time.sleep(interval)
            return True
    return False
        
def main():
    log_directory = os.getenv('LOG_DIR')
    
    while True:
        log_file = current_log_name()
        log_file_path = os.path.join(log_directory, log_file)
        line = last_line_of_log(log_file_path)
        if 'WARN:' in line:
            notification(line)
            if not is_node_host_up(NODE_HOST):
                powercycle_node_host()
        time.sleep(10)
    

if __name__ == "__main__":
    load_dotenv()
    NODE_HOST = os.getenv('NODE_HOST')
    main() 

  