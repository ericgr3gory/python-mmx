from dotenv import load_dotenv
import os
import requests
import time


def mmx_switch():
    
    load_dotenv()
    ENTITY_ID = os.getenv('ENTITY_ID')
    HA_URL = os.getenv('HA_URL')
    HA_TOKEN = os.getenv('HA_TOKEN')
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json",
    }

    data = {
        "entity_id": ENTITY_ID
    }

    response = requests.post(f"{HA_URL}/api/services/switch/turn_off", headers=headers, json=data)

    if response.status_code == 200:
        print(f"Successfully turned off {ENTITY_ID}")
        time.sleep(10)
        response = requests.post(f"{HA_URL}/api/services/switch/turn_on", headers=headers, json=data)
        if response.status_code == 200:
            print("switch back on")
    else:
        print(f"Failed to turn off {ENTITY_ID}: {response.text}")