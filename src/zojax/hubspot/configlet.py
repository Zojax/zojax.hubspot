import logging
from rwproperty import getproperty, setproperty
import urllib
import xml.etree.ElementTree
from xml.parsers.expat import ExpatError

from zope import component, interface, schema

from interfaces import _, ILeadFormFactory, ILeadForm
from zojax.catalog.utils import getRequest

logger = logging.getLogger("zojax.hubspot")


class HubSpotConfiglet(object):

    def postForm(self, formName, **data):
        request = getRequest()
        
        def force_unicode(s):
            if isinstance(s, unicode):
                return s.encode('utf-8')
            return s
        data = dict(map(lambda (x, y): (x, force_unicode(y)), data.items()))
        
        data['UserToken'] = request.getCookie('hubspotutk')
        data['IPAddress'] = request.get('REMOTE_ADDR', '')
        apiUrl = self.apiURL
        if not self.enabled:
            return
        if not apiUrl:
            # HubSpot API is not configured. Abort the submission.
            logger.warning("HubSpot API is not configured.")
            return
        url = '%s?%s'%(apiUrl, urllib.urlencode(dict(data, app='leaddirector', FormName=formName)))
        try:
            urllib.urlopen(url)
        except IOError, exc:
            logger.warning('Form post error', exc_info=True)

    @getproperty
    def forms(self):
        forms = self.data.get('forms', {})
        if not isinstance(forms, dict):
            forms = {}
        updated = False
        res = []
        for name, factory in component.getUtilitiesFor(ILeadFormFactory):
            if name not in forms:
                forms[name] = factory()
                updated = True
            res.append(forms[name])
        if updated:
            self.data['forms'] = forms
        return sorted(res, key=lambda x: x.title)

    @setproperty
    def forms(self, value):
        if value:
            self.data['forms'] = dict([(lst.name, lst) for lst in value])

    def getForm(self, name):
        forms = self.forms
        return self.data['forms'][name]
