from modules.Connection import Connection
import requests
import master_password


class Vcenter:
    def __init__(self, name, mpw, user, password):
        self.user = user
        self.mpw = mpw
        self.pw = password
        if not password:
            self.pw_handle = self.generate_pw_handle()
            self.pw = self.generate_pw(name).replace('/', '')
        self.name = name

    @staticmethod
    def get_vcs_from_atlas(atlas_endpoint):
        response = requests.get(url=atlas_endpoint)
        netbox_json = response.json()
        vcenter_list = list()
        for target in netbox_json:
            if target['labels']['job'] == "vcenter":
                vcenter = target['labels']['server_name']
                vcenter_list.append(vcenter)
        return vcenter_list

    def generate_pw_handle(self):
        return master_password.MPW(self.user, self.mpw)

    def generate_pw(self, url):
        if self.pw:
            return self.pw
        return self.pw_handle.password(url)

    def login(self):
        self.con = Connection(self)
        self.con.login()

    def logout(self):
        if self.con.session_id:
            self.con.logout()
