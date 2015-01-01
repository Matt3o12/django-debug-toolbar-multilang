#!/usr/bin/env python

import logging
import sys
import multiprocessing
import django
from django.conf import settings
from django.test.utils import get_runner
import os

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer


class Colored:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    @classmethod
    def print_info(cls, msg, *args, **kwargs):
        cls._print(msg, cls.OKBLUE, *args, **kwargs)

    @classmethod
    def print_success(cls, msg, *args, **kwargs):
        cls._print(msg, cls.OKGREEN, *args, **kwargs)

    @classmethod
    def print_warning(cls, msg, *args, **kwargs):
        cls._print(msg, cls.WARNING, *args, **kwargs)

    @classmethod
    def print_fail(cls, msg, *args, **kwargs):
        cls._print(msg, cls.HEADER, *args, **kwargs)

    @classmethod
    def _print(cls, msg, color, *args, **kwargs):
        values = {
            "msg": msg,
            "color": color,
            "reset": cls.ENDC
        }

        return print("{color}{msg}{reset}".format(**values), *args, **kwargs)


class ReloadTestEventHandler(PatternMatchingEventHandler):
    def __init__(self, test_labels=None):
        patterns = ["*.yaml", "*.yml", "*.json", "*.py"]
        super(ReloadTestEventHandler, self).__init__(
            patterns, ignore_directories=True
        )

        self.test_labels = test_labels
        self.currentProcesses = None

    def on_modified(self, event):
        self.reload_tests()

    def on_created(self, event):
        self.reload_tests()

    def reload_tests(self):
        if self.currentProcesses and self.currentProcesses.is_alive():
            self.currentProcesses.join(.25)

            if self.currentProcesses.is_alive():
                self.currentProcesses.terminate()

        self.currentProcesses = TestRunnerProcess(self.test_labels)
        self.currentProcesses.start()
        self.currentProcesses.join()


class TestRunnerProcess(multiprocessing.Process):
    def __init__(self, test_labels=None, *args, **kwargs):
        super(TestRunnerProcess, self).__init__(*args, **kwargs)

        self.test_labels = test_labels

    def run(self):
        Colored.print_info("Running tests...")

        django.setup()
        TestRunner = get_runner(settings)
        testRunner = TestRunner()
        failures =  testRunner.run_tests(self.test_labels)

        print()
        if failures:
            Colored.print_fail("--- Unit tests failed. ---")
        else:
            Colored.print_success("--- Unit test finished successfully. ---")

        print()

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")
    handler = ReloadTestEventHandler(tuple(sys.argv[1:]))
    handler.reload_tests()

    observer = Observer()
    observer.schedule(handler, ".", recursive=True)
    observer.start()

    try:
        observer.join()
    except KeyboardInterrupt:
        print()
    finally:
        observer.stop()