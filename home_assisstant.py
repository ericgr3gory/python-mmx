from dotenv import load_dotenv
import os
import requests
from requests.exceptions import RequestException
    
def mmx_switch(action):
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
    try:
        response = requests.post(f"{HA_URL}/api/services/switch/{action}", headers=headers, json=data)
        print(response)
        if response.status_code == 200:
            return True
        
        else:
            return False
    
    except RequestException as e:
        
        print(f"Error calling mmx_switch: {e}")
        return False