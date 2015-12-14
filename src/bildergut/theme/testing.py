# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import bildergut.theme


class BildergutThemeLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=bildergut.theme)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'bildergut.theme:default')


BILDERGUT_THEME_FIXTURE = BildergutThemeLayer()


BILDERGUT_THEME_INTEGRATION_TESTING = IntegrationTesting(
    bases=(BILDERGUT_THEME_FIXTURE,),
    name='BildergutThemeLayer:IntegrationTesting'
)


BILDERGUT_THEME_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(BILDERGUT_THEME_FIXTURE,),
    name='BildergutThemeLayer:FunctionalTesting'
)


BILDERGUT_THEME_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        BILDERGUT_THEME_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='BildergutThemeLayer:AcceptanceTesting'
)
