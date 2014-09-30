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
from zope.i18nmessageid.message import MessageFactory
from zope.schema import Bool, Object, Text, TextLine, Tuple, URI

from zojax.content.type.interfaces import IItem
from zojax.richtext.field import RichText

_ = MessageFactory('zojax.hubspot')

HUBSPOT_FIELDS = [
                  'FirstName',
                  'LastName',
                  'Email',
                  'TwitterHandle',
                  'Phone',
                  'Fax',
                  'Company',
                  'Address',
                  'JobTitle',
                  'City',
                  'State',
                  'ZipCode',
                  'Country',
                  'Message',
                  'Website',
                  'NumberEmployees',
                  'Annual Revenue',
                  'CloseDate'
    ]


class ILeadFormFactory(interface.Interface):

    name = TextLine(title=_(u'Name'))

    title = TextLine(title=_(u'Title'))


class ILeadForm(interface.Interface):

    name = TextLine(title=_(u'Name'))

    title = TextLine(title=_(u'Title'))


class IHubSpotConfiglet(interface.Interface):

    enabled = Bool(title=_(u'Enabled'),
                          default=False)

    apiURL = URI(title=_(u'API Url'),

                             default="http://your-shortname.app101.hubspot.com/")
    forms = Tuple(title=_(u"Forms"),
                         value_type=Object(title=_(u'form'),
                                                 schema=ILeadForm),
                         default=(),
                         required=False)

    def getForm(name):
        """get form by name"""

    def postForm(formName, **data):
        """ post form """


class IEmbedHubSpotForm(IItem):
    """ HubSpot Form """

    description = interface.Attribute('Object Description')

    body = RichText(
        title = _(u'Before the Form text'),
        required = False)

    embed = Text(
        title=_(u"Embed a snippet from HubSpot"),
        required=True)


class IEmbedHubSpotFormType(interface.Interface):
    """ HubSpot Form type """

