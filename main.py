import time
from datetime import date
import logging
import os
import subprocess

from dotenv import load_dotenv
from home_assisstant import mmx_switch
from notify import notification

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
load_dotenv()
NODE_HOST = os.getenv('NODE_HOST')

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
    
    message = "attempting to powercycle in 45 seconds"
    logger.info(message)
    notification(message)
    time.sleep(45)
    
    if mmx_switch('turn_off'):
        
        message = ('mmx_switch truned off')
        logger.info(message)
        notification(message)
        time.sleep(3)
        
        if mmx_switch('turn_on'):
            
            message = "mmx_switch is turned on"
            logger.info(message)
            notification(message)
            
            timeout = 360 
            interval = 45 
            start_time = time.time()
            
            message = "confirming host is up............"
            logger.info(message)
            notification(message)
            
            while not is_node_host_up(NODE_HOST):
                
                if time.time() - start_time > timeout:
                    message = "Timeout: Node host did not come up within the expected time."
                    logger.info(message)
                    notification(message)
                    return False
                
                time.sleep(interval)
            message = f"powercycle success {NODE_HOST} is up waiting 2 minutes for mmx node to restart"
            logger.info(message)
            notification(message)
            time.sleep(120)
            return True
    
    else:    
        message =  "mmx_node switch failed to turn on or off"   
        logger.info(message)
        notification(message)
    
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
        else:
            logger.info(f'we are farmers ba db bab bab ...\n{line}')
        
        time.sleep(10)
    

if __name__ == "__main__":
    main() 

  