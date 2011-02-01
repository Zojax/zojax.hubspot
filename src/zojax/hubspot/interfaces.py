from zope import interface, schema
from zope.i18nmessageid.message import MessageFactory

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

    name = schema.TextLine(title=_(u'Name'))

    title = schema.TextLine(title=_(u'Title'))


class ILeadForm(interface.Interface):

    name = schema.TextLine(title=_(u'Name'))

    title = schema.TextLine(title=_(u'Title'))


class IHubSpotConfiglet(interface.Interface):

    enabled = schema.Bool(title=_(u'Enabled'),
                          default=False)
    
    apiURL = schema.URI(title=_(u'API Url'),

                             default="http://your-shortname.app101.hubspot.com/")
    forms = schema.Tuple(title=_(u"Forms"),
                         value_type=schema.Object(title=_(u'form'),
                                                 schema=ILeadForm),
                         default=(),
                         required=False)

    def getForm(name):
        """get form by name"""

    def postForm(formName, **data):
        """ post form """
