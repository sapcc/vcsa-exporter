from urllib3 import disable_warnings
from urllib3 import exceptions
import requests
import json
import os

class Connection:
    def login(target, user, password):
        disable_warnings(exceptions.InsecureRequestWarning)
        if os.environ['DEBUG'] == "1":
            print("logging in", target)
        url = "https://" + target + "/rest/com/vmware/cis/session" 
        try:
            response = requests.post(url, auth=(user, password), verify=False)
        except Exception as e:
            print("Problem connecting to", target, "Error:", str(e))
            return False
        
        if response.status_code == 200:
            return response.json()['value']
        else:
            print("Problem logging into", target, ":", response.text)
    
    def get_request(target, key, session_id):
        disable_warnings(exceptions.InsecureRequestWarning)
        if os.environ['DEBUG'] == "1":
            print("issuing request",target, key)
        url = "https://" + target + "/rest/" + key 
        try:
            response = requests.get(url, verify=False,
                                    headers={"vmware-api-session-id": session_id})
        except Exception as e:
            print("Problem handling", key, "for", target, ":", str(e))
        if response.status_code == 200:
            return response.json()
        else:
            print("Problem with get return of", target, ":", response.text)
