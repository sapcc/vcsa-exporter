from urllib3 import disable_warnings
from urllib3 import exceptions
import requests
import json
import os

class Connection:
    def login(target, user, password):
        disable_warnings(exceptions.InsecureRequestWarning)
        if os.environ['DEBUG'] == "1":
            print("login", target)
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
            print("request",target, key)
        url = "https://" + target + "/rest/" + key 
        try:
            response = requests.get(url, verify=False,
                                    headers={"vmware-api-session-id": session_id})
        except Exception as e:
            print("Problem handling", key, "for", target, ":", str(e))
            return False
        if response.status_code == 200:
            return response.json()
        else:
            print("Problem with get return of", target, ":", response.text)
            return False

    def post_request(target, key, post, session_id):
        disable_warnings(exceptions.InsecureRequestWarning)
        if os.environ['DEBUG'] == "1":
            print("request", target, key)
        url = "https://" + target + "/rest/" + key + '?' + post
        try:
            response = requests.post(url, verify=False,
                                    headers={"vmware-api-session-id": session_id})
        except Exception as e:
            print("Problem handling", key, "for", target, ":", str(e))
            return False
        if response.status_code == 200:
            return response.json()
        else:
            print("Problem with post return of", target, ":", response.text)
            return False

        # going to be used until reuse of session_id is in place
    def logout(target, session_id):
        disable_warnings(exceptions.InsecureRequestWarning)
        if os.environ['DEBUG'] == "1":
            print("logout",target)
        url = "https://" + target + "/rest/com/vmware/cis/session"
        try:
            response = requests.delete(url, verify=False,
                                    headers={"vmware-api-session-id": session_id})
        except Exception as e:
            print("Problem deleting session for", target, ":", str(e))
            return False
        if response.status_code == 200:
            return
        else:
            print("Problem with getting return of", target, ":", response.text)
