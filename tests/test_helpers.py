from tests.helpers import DebugToolbarMultiLangTestCase


class TestDebugToolbarMultiLangTestCase(DebugToolbarMultiLangTestCase):
    # not supported in djagno 1.6

    # def testGetHostURLHTTPs(self):
    #     request = self.factory.get("/test/", secure=True, SERVER_NAME="test")
    #     self.assertEqual("https://test/", self.get_host_url(request))

    def testGetHostURLHTTP(self):
        request = self.factory.get("/test/", secure=False, SERVER_NAME="test")
        self.assertEqual("http://test/", self.get_host_url(request))

    def testGetHostURLDefault(self):
        request = self.factory.get("/test/")
        self.assertEqual("http://testserver/", self.get_host_url(request))

    def testGetHostURLCustomName(self):
        request = self.factory.get("test", SERVER_NAME="serverName.tld")
        self.assertEqual("http://serverName.tld/", self.get_host_url(request))