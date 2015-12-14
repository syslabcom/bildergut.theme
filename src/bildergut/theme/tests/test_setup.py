# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from bildergut.theme.testing import BILDERGUT_THEME_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that bildergut.theme is properly installed."""

    layer = BILDERGUT_THEME_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if bildergut.theme is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'bildergut.theme'))

    def test_browserlayer(self):
        """Test that IBildergutThemeLayer is registered."""
        from bildergut.theme.interfaces import (
            IBildergutThemeLayer)
        from plone.browserlayer import utils
        self.assertIn(IBildergutThemeLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = BILDERGUT_THEME_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['bildergut.theme'])

    def test_product_uninstalled(self):
        """Test if bildergut.theme is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'bildergut.theme'))

    def test_browserlayer_removed(self):
        """Test that IBildergutThemeLayer is removed."""
        from bildergut.theme.interfaces import IBildergutThemeLayer
        from plone.browserlayer import utils
        self.assertNotIn(IBildergutThemeLayer, utils.registered_layers())
