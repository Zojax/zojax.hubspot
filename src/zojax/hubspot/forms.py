##############################################################################
#
# Copyright (c) 2008 Zope Foundation and Contributors.
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
from zope import interface
from zope.schema.fieldproperty import FieldProperty

from z3c.form.object import registerFactoryAdapter

from zojax.content.type.item import PersistentItem
from zojax.richtext.field import RichTextProperty

from interfaces import ILeadFormFactory, ILeadForm, IEmbedHubSpotForm


class LeadForm(object):
    interface.implements(ILeadForm)

    title = None

    id = None

    name = None

    def __init__(self, name='', title=''):
        self.name = unicode(name)
        self.title = unicode(title)


class LeadFormFactory(object):
    interface.implements(ILeadFormFactory)

    title = None

    name = None

    def __call__(self):
        return LeadForm(self.name, self.title)


registerFactoryAdapter(ILeadForm, LeadForm)


class EmbedHubSpotForm(PersistentItem):
    interface.implements(IEmbedHubSpotForm)

    body = RichTextProperty(IEmbedHubSpotForm['body'])
    embed = FieldProperty(IEmbedHubSpotForm['embed'])
