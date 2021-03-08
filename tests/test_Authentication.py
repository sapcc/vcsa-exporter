from tests.ServerSetup import ServerSetup
from modules.Vcenter import Vcenter


class TestAuthentication(ServerSetup):
    def test_authentication(self):
        self.name = "Mocking"
        self.authentication_success()

    def authentication_success(self):
        vcenter = Vcenter("localhost", None, self.name, "Nula8.VeyuCaru")
        vcenter.login()
        assert vcenter.user == "Mocking"
