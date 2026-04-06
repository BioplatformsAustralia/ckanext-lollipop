"""
Tests for interface.py.
"""
import pytest

import ckan.tests.factories as factories
import ckanext.lollipop.interface as interface


class TestLollipopInterface(object):
    def test_lollipop_required(self):
        lollipop = interface.ILollipop()

        result = lollipop.lollipop_required()

        assert result == True
