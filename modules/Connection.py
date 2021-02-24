from urllib3 import disable_warnings
from urllib3 import exceptions
import requests
import logging

LOG = logging.getLogger('vcsa-exporter')


class Connection:
    def __init__(self, vcenter):
        self.target = vcenter.name
        self.user = vcenter.user
        self.pw = vcenter.pw
        self.session_id = None

    def login(self):
        disable_warnings(exceptions.InsecureRequestWarning)
        LOG.debug(f"login {self.target}")
        url = "https://" + self.target + "/rest/com/vmware/cis/session"
        try:
            response = requests.post(url, auth=(self.user, self.pw), verify=False)
        except Exception as e:
            LOG.error(f"Problem connecting to {self.target} Error: {str(e)}")
            return False
        if response.status_code == 200:
            self.session_id = response.json()['value']
            LOG.debug(f"login session id {self.target} {self.session_id}")
        else:
            LOG.warning(f"Problem logging into {self.target}: {response.text}")
            return False

    def get_request(self, key):
        disable_warnings(exceptions.InsecureRequestWarning)
        LOG.debug(f"request {self.target}, {key}")
        url = "https://" + self.target + "/rest/" + key
        try:
            response = requests.get(url, verify=False,
                                    headers={"vmware-api-session-id": self.session_id})
        except Exception as e:
            LOG.error(f"Problem handling {key} for {self.target}: {str(e)}")
            return False
        if response.status_code == 200:
            return response.json()
        else:
            LOG.warning(f"Problem with get return of {self.target}: {response.text}")
            return False

    def post_request(self, key, data):
        disable_warnings(exceptions.InsecureRequestWarning)
        LOG.debug(f"request {self.target} {key}")
        url = "https://" + self.target + "/rest/" + key
        try:
           response = requests.post(url, verify=False, data=data, headers={"vmware-api-session-id": session_id})	            
        try:
            response = requests.post(url, verify=False,
                                     headers={"vmware-api-session-id": self.session_id})
        except Exception as e:
            LOG.error(f"Problem handling {key} for {self.target}: {str(e)}")
            return False
        if response.status_code == 200:
            return response.json()
        else:
            LOG.warning(f"Problem with post return of {self.target}: {response.text}")
            return False

    def logout(self):
        disable_warnings(exceptions.InsecureRequestWarning)
        LOG.debug(f"Logout {self.target} {self.session_id}")
        url = "https://" + self.target + "/rest/com/vmware/cis/session"
        try:
            response = requests.delete(url, verify=False,
                                       headers={"vmware-api-session-id": self.session_id})
        except Exception as e:
            LOG.error(f"Problem deleting session for {self.target}: {str(e)}")
            return False
        if response.status_code == 200:
            return
        else:
            LOG.warning(f"Problem logging out, getting return of {self.target} {self.session_id}: {response.text}")
