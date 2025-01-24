from dotenv import load_dotenv
import os
import requests

ENTITY_ID = os.getenv('ENTITY_ID')
HA_URL = os.getenv('HA_URL')
HA_TOKEN = os.getenv('HA_TOKEN')
    
def mmx_switch(action):
    
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json",
    }

    data = {
        "entity_id": ENTITY_ID
    }

    response = requests.post(f"{HA_URL}/api/services/switch/{action}", headers=headers, json=data)

    if response.status_code == 200:
        return True
        
    else:
        return False