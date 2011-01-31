from zope import component, interface, schema
from z3c.form.object import registerFactoryAdapter

from interfaces import _, ILeadFormFactory, ILeadForm


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
