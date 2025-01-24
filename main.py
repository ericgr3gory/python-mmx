import time
from datetime import date
from notify import notification
import subprocess
from dotenv import load_dotenv
import os
from home_assisstant import mmx_switch
import logging

def last_line_of_log(filename):
    try:
        with open(filename, "rb") as mmx_log:
            mmx_log.seek(-2, os.SEEK_END)
            
            while mmx_log.read(1) != b"\n":
                mmx_log.seek(-2, os.SEEK_CUR)
            
            return mmx_log.readline().decode().strip()
            

    except (OSError, IndexError):
        return ""
    
def current_log_name():
    current_date = date.today()
    return f'mmx_harvester_{current_date.year}_{current_date.month:02}_{current_date.day:02}.txt'

def is_node_host_up(host):
    result = subprocess.run(['ping', '-c', '1', host], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        logger.info(f"{host} is up")
        notification(f"{host} is up")
        return True
    else:
        logger.info(f"{host} is down")
        return False
    
def powercycle_node_host():
    logger.info("attempting to powercycle in 45 seconds")
    notification("attempting to powercycle in 45 seconds")
    time.sleep(45)
    if mmx_switch('turn_off'):
        logger.info('mmx_switch off')
        time.sleep(3)
        if mmx_switch('turn_on'):
            logger.info('mmx_switch on')
            timeout = 360 
            interval = 45 
            start_time = time.time()
            logger.info('confirming host is up............')
            while not is_node_host_up(NODE_HOST):
                if time.time() - start_time > timeout:
                    logger.info("Timeout: Node host did not come up within the expected time.")
                    return False
                time.sleep(interval)
            logger.info(f"powercycle success {NODE_HOST} is up")
            notification(f"powercycle success {NODE_HOST} is up")
            return True
    logger.info("mmx_node switch failed to turn on or off")
    notification("mmx_node switch failed to on or turn off")
    return False
        
def main():
    mmx_log_directory = os.getenv('LOG_DIR')
    
    while True:
        mmx_log_file = current_log_name()
        mmx_log_file_path = os.path.join(mmx_log_directory, mmx_log_file)
        line = last_line_of_log(mmx_log_file_path)
        if 'WARN:' in line:
            notification(line)
            logger.info(line)
            if not is_node_host_up(NODE_HOST):
                powercycle_node_host()
        time.sleep(10)
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    load_dotenv()
    NODE_HOST = os.getenv('NODE_HOST')
    main() 

  