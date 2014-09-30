##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
import os.path
import unittest, doctest
from zope import interface, event
from zope.app.component.hooks import setSite
from zope.app.intid import IntIds
from zope.app.intid.interfaces import IIntIds
from zope.app.testing import functional
from zope.app.testing.functional import ZCMLLayer
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.app.container.interfaces import IContainer as IBaseContainer
from zope.app.rotterdam import Rotterdam
from zope.lifecycleevent import ObjectCreatedEvent
from zope.security.management import newInteraction, endInteraction
from zojax.layoutform.interfaces import ILayoutFormLayer
from zojax.content.space.content import ContentSpace
from zojax.content.type.item import PersistentItem
from zojax.content.type.interfaces import IItem

from zojax.hubspot.forms import LeadFormFactory


class TestLeadFormFactory(LeadFormFactory):
    name = u'testForm'

    title = u'Test Form'


class IDefaultSkin(ILayoutFormLayer, Rotterdam):
    """ skin """


class IPortal(interface.Interface):
    """ portal """


class IContent(IItem):
    """ content """


class IContentType(interface.Interface):
    """ content type """


class IPortalContent(IItem):
    """ simple content """


class IContainer(IBaseContainer):
    """ container """


class Content(PersistentItem):
    interface.implements(IContent)


class PortalContent(PersistentItem):
    interface.implements(IPortalContent, IAttributeAnnotatable)


hubspot = ZCMLLayer(
    os.path.join(os.path.split(__file__)[0], 'ftesting.zcml'),
    __name__, 'hubspot', allow_teardown=True)



def FunctionalDocFileSuite(*paths, **kw):
    layer = hubspot

    globs = kw.setdefault('globs', {})
    globs['http'] = functional.HTTPCaller()
    globs['getRootFolder'] = functional.getRootFolder
    globs['sync'] = functional.sync

    kw['package'] = doctest._normalize_module(kw.get('package'))

    kwsetUp = kw.get('setUp')
    def setUp(test):
        functional.FunctionalTestSetup().setUp()

        newInteraction()

        root = functional.getRootFolder()
        setSite(root)
        sm = root.getSiteManager()

        # IIntIds
        root['ids'] = IntIds()
        sm.registerUtility(root['ids'], IIntIds)
        root['ids'].register(root)

        # space
        space = ContentSpace(title=u'Space')
        event.notify(ObjectCreatedEvent(space))
        root['space'] = space

        endInteraction()

    kw['setUp'] = setUp

    kwtearDown = kw.get('tearDown')
    def tearDown(test):
        setSite(None)
        functional.FunctionalTestSetup().tearDown()

    kw['tearDown'] = tearDown

    if 'optionflags' not in kw:
        old = doctest.set_unittest_reportflags(0)
        doctest.set_unittest_reportflags(old)
        kw['optionflags'] = (old|doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE)

    suite = doctest.DocFileSuite(*paths, **kw)
    suite.layer = layer
    return suite


def test_suite():
    return unittest.TestSuite((
            FunctionalDocFileSuite("tests.txt"),
            ))
