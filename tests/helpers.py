from __future__ import absolute_import
from optparse import make_option
from unittest.loader import TestLoader

from django.test.client import RequestFactory
from django.test.runner import DiscoverRunner
from django.test.testcases import TestCase


try:
    from django.utils.translation import LANGUAGE_SESSION_KEY
except ImportError:  # backwards compatible with django 1.6
    LANGUAGE_SESSION_KEY = "django_language"

try:
    from unittest import mock
    from unittest.mock import patch, MagicMock, Mock, call
except ImportError:
    import mock
    from mock import patch, MagicMock, Mock, call


UNITTEST_TEST, FUNCTIONAL_TEST, INTEGRATION_TEST = range(3)


class DebugToolbarMultiLangTestCase(TestCase):
    TEST_TYPE = UNITTEST_TEST

    def setUp(self):
        self.factory = RequestFactory()

    def get_host_url(self, request):
        """
        Returns the host url (and ignores ports!).

        :param request: HttpRequest
        :return: str
        """

        # Django 1.6 does not support schemes properly.
        # The RequestFactory does not know anything about
        # schemes, as well.

        # values = {
        #     "schema": "https" if request.is_secure() else "http", or
        #     "schema": request.get_scheme
        #     "host": request.get_host()
        # }
        # return "%(schema)s://%(host)s/" % values

        return "http://%s/" % request.get_host()


class DJDTMultilangTestLoader(TestLoader):
    """
    Just like the default test loader but it filters all
    DebugToolbarMultiLangTestCase according to the test type
    values.
    """

    def __init__(self, test_types=None, *args, **kwargs):
        """
        :param test_types: list
        :param args: args of super class
        :param kwargs: kwargs of super class
        """
        super(DJDTMultilangTestLoader, self).__init__(*args, **kwargs)

        # we allow test_types to be empty so that no
        # DebugToolbarMultiLangTestCase are being run.
        if test_types is None:
            test_types = [
                UNITTEST_TEST,
                FUNCTIONAL_TEST,
                INTEGRATION_TEST
            ]

        self.test_types = test_types

    def loadTestsFromTestCase(self, testCaseClass):
        """
        Loads all tests from the test case just like its super
        implementation unless testCaseClass is an instance of
        DebugToolbarMultiLangTestCase and the test type (of that
        TestCase) is not in the loaders allowed test types. Then,
        it just returns an empty list.
        """
        if not (issubclass(testCaseClass, DebugToolbarMultiLangTestCase)
                and testCaseClass.TEST_TYPE not in self.test_types):
            return super(DJDTMultilangTestLoader, self).loadTestsFromTestCase(
                testCaseClass
            )
        else:
            return self.suiteClass()

combineStr = "This option can be combined with --unittest, --functional," \
             "and --integration"


class DJDTMultilangRunner(DiscoverRunner):
    test_types = None
    _test_loader_class = DJDTMultilangTestLoader

    option_list = DiscoverRunner.option_list + (
        make_option(
            "-u", "--unittest", action="store_true",
            help="Run unittests. %s" % combineStr
        ), make_option(
            "-f", "--functional", action="store_true",
            help="Run functional tests. %s" % combineStr
        ), make_option(
            "-i", "--integration", action="store_true",
            help="Run integration tests. %s" % combineStr
        )
    )

    def __init__(self, unittest=False, integration=False, functional=False,
                 *args, **kwargs):
        super(DJDTMultilangRunner, self).__init__(*args, **kwargs)

        types = []
        if unittest: types.append(UNITTEST_TEST)
        if functional: types.append(FUNCTIONAL_TEST)
        if integration: types.append(INTEGRATION_TEST)

        if types:
            self.test_types = types

    @property
    def test_loader(self):
        return self._test_loader_class(self.test_types)
