"""
Tests for interface.py.
"""
import pytest

import ckan.tests.factories as factories
import ckanext.lollipop.interface as interface


class TestLollipopInterface(object):
    def test_lollipop_set(self):
        lollipop = interface.ILollipop()

        result = lollipop.lollipop_set(None)

        assert result == True

    def test_lollipop_update(self):
        lollipop = interface.ILollipop()

        result = lollipop.lollipop_update(None)

        assert result == True

    def test_lollipop_clear(self):
        lollipop = interface.ILollipop()

        result = lollipop.lollipop_clear(None)

        assert result == True

    def test_lollipop_required(self):
        lollipop = interface.ILollipop()

        result = lollipop.lollipop_required()

        assert result == True

    def test_lollipop_process(self):
        lollipop = interface.ILollipop()

        context = {}
        data_dict = {}
        result = lollipop.lollipop_process(context, data_dict)

        assert result == True
