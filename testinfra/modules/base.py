# -*- coding: utf8 -*-
# Copyright © 2015 Philippe Pepiot
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import unicode_literals

import pytest


class Module(object):

    def __init__(self, _backend):
        self._backend = _backend
        super(Module, self).__init__()

    def run(self, command, *args, **kwargs):
        return self._backend.run(command, *args, **kwargs)

    def run_expect(self, expected, command, *args, **kwargs):
        """Run command and check it return an expected exit status

        :param expected: A list of expected exit status
        :raises: AssertionError
        """
        __tracebackhide__ = True
        out = self.run(command, *args, **kwargs)
        if out.rc not in expected:
            pytest.fail("Unexpected exit code %s for %s" % (out.rc, out))
        return out

    def run_test(self, command, *args, **kwargs):
        """Run command and check it return an exit status of 0 or 1

        :raises: AssertionError
        """
        return self.run_expect([0, 1], command, *args, **kwargs)

    def check_output(self, command, *args, **kwargs):
        """Get stdout of a command which has run successfully

        :returns: stdout without trailing newline
        :raises: AssertionError
        """
        __tracebackhide__ = True
        out = self.run(command, *args, **kwargs)
        if out.rc != 0:
            pytest.fail("Unexpected exit code %s for %s" % (out.rc, out))

        if len(out.stdout) and out.stdout[-1] == "\n":
            return out.stdout[:-1]
        else:
            return out.stdout

    @classmethod
    def get_module(cls, _backend):
        return cls(_backend)

    @classmethod
    def as_fixture(cls):
        @pytest.fixture(scope="module")
        def f(testinfra_backend):
            return testinfra_backend.get_module(cls.__name__)
        f.__doc__ = cls.__doc__
        return f
