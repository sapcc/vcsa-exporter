import json
import master_password

class Vcenter:
    def __init__(self, atlasfile, mpw, user, password=None):
        self.vcenter_list = list()
        self.vc_pws = dict()
        self.atlasfile = atlasfile
        self.user = user
        self.mpw = mpw
        self.pw = password
        self.pw_handle = self.generate_pw_handle()

    def get_vcs_from_atlas(self):
        with open(self.atlasfile) as json_file:
            netbox_json = json.load(json_file)
        vcenter_list = list()
        for target in netbox_json:
            if target['labels']['job'] == "vcenter":
                vcenter = target['labels']['server_name']
                vcenter_list.append(vcenter)
        self.vcenter_list = vcenter_list

    def generate_pw_handle(self):
        return master_password.MPW(self.user, self.mpw)

    def generate_pw(self, url):
        if self.pw:
            return self.pw
        return self.pw_handle.password(url)
