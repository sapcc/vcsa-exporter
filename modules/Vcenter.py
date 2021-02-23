from modules.Connection import Connection
import json
import master_password


class Vcenter:
    def __init__(self, name, atlasfile, mpw, user, password=None):
        self.user = user
        self.mpw = mpw
        self.pw = password
        if not password:
            self.pw_handle = self.generate_pw_handle()
        self.session_id = None
        self.name = name

    @staticmethod
    def get_vcs_from_atlas(atlasfile):
        with open(atlasfile) as json_file:
            netbox_json = json.load(json_file)
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
        self.session_id = Connection.login(self.name, self.user, self.generate_pw(self.name))

    def logout(self):
        if self.session_id:
            Connection.logout(self.name, self.session_id)
