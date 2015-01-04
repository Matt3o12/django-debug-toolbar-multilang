from __future__ import absolute_import
from unittest.suite import TestSuite

from django.test.testcases import TestCase

from tests.helpers import DebugToolbarMultiLangTestCase, \
    DJDTMultilangTestLoader, FUNCTIONAL_TEST, UNITTEST_TEST, patch, \
    INTEGRATION_TEST, DJDTMultilangRunner, MagicMock


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


class TestDJDTMultilangTestLoader(TestCase):
    def setUp(self):
        super(TestCase, self).setUp()

        class MockTestCase(DebugToolbarMultiLangTestCase):
            pass

        self.loader = DJDTMultilangTestLoader()
        self.testCaseClass = MockTestCase

    def assertCountEqual(self, first, second, msg=None):
        """
        Most simple backport of assertCountEqual for python 2.7

        :return:
        """

        self.assertEqual(set(first), set(second), msg)

    def testInit_noArgs(self):
        loader = DJDTMultilangTestLoader()
        allTypes = [FUNCTIONAL_TEST, UNITTEST_TEST, INTEGRATION_TEST]
        self.assertCountEqual(allTypes, loader.test_types)

    def testInit_emptyList(self):
        loader = DJDTMultilangTestLoader([])
        self.assertEqual([], loader.test_types)

    def testInit(self):
        types = [INTEGRATION_TEST, UNITTEST_TEST]
        loader = DJDTMultilangTestLoader(types)
        self.assertCountEqual(types, loader.test_types)

    def _patchSuper(self, *args, **kwargs):
        return patch("django.utils.six.moves.builtins.super", *args, **kwargs)

    def assertSuperCalled(self, superMock, result):
        expected = superMock().loadTestsFromTestCase.return_value
        self.assertEqual(expected, result)

    def testLoadTestsFromModule_normalTC(self):
        with self._patchSuper() as superMock:
            result = self.loader.loadTestsFromTestCase(TestCase)

        self.assertSuperCalled(superMock, result)

    def assertTestSuitIsEmpty(self, suit):
        self.assertIsInstance(suit, TestSuite)
        self.assertEqual(0, len(list(suit)))

    def testAssertTestSuitIsEmpty(self):
        suit = TestSuite()
        self.assertTestSuitIsEmpty(suit)

    def testAssertTestSuitNotEmpty(self):
        suit = TestSuite()
        suit.addTest(self.testAssertTestSuitIsEmpty)

        with self.assertRaises(AssertionError):
            self.assertTestSuitIsEmpty(suit)

    def testAssertTestSuitWrongInstance(self):
        with self.assertRaises(AssertionError):
            self.assertTestSuitIsEmpty(object())

    def testLoadTestsFromModule(self):
        with self._patchSuper() as superMock:
            result = self.loader.loadTestsFromTestCase(self.testCaseClass)

        self.assertSuperCalled(superMock, result)

    def testLoadTestsFromModuleCustomTypeFail(self):
        self.loader.test_types = [FUNCTIONAL_TEST]

        with self._patchSuper() as superMock:
            result = self.loader.loadTestsFromTestCase(self.testCaseClass)

        self.assertTestSuitIsEmpty(result)

    def testLoadTestsFromModuleCustomType(self):
        self.loader.test_types = [UNITTEST_TEST]

        with self._patchSuper() as superMock:
            result = self.loader.loadTestsFromTestCase(self.testCaseClass)

        self.assertSuperCalled(superMock, result)


class TestDJDTMultilangRunner(TestCase):
    def setUp(self):
        super(TestDJDTMultilangRunner, self).setUp()

        self.runner = DJDTMultilangRunner()

    def testGetTest_loader(self):
        types = object()
        loader_class = MagicMock()
        self.runner._test_loader_class = loader_class
        self.runner.test_types = types

        loader = self.runner.test_loader
        self.assertEqual(loader, loader_class.return_value)
        loader_class.assert_called_once_with(types)

    def testInitNoArgs(self):
        self.assertIsNone(self.runner.test_types)

    def testInitArgs(self):
        runner = DJDTMultilangRunner(unittest=True, integration=True)

        expected = [INTEGRATION_TEST, UNITTEST_TEST]
        self.assertEqual(set(expected), set(runner.test_types))
