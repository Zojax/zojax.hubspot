# This file is necessary to make this directory a package.
from zope.proxy import removeAllProxies

from z3c.form.interfaces import IDataManager, IErrorViewSnippet

from zojax.layoutform.form import PageletForm
from zojax.content.space.browser.workspace import WorkspacesManagement

def extractData(self, setErrors=True):
    data, errors = super(PageletForm, self).extractData(setErrors=setErrors)
    for form in self.groups:
        formData, formErrors = form.extractData(setErrors=setErrors)
        data.update(formData)
        if formErrors:
            errors += formErrors

    for form in self.subforms:
        formData, formErrors = form.extractData(setErrors=setErrors)
        if formErrors:
            errors += formErrors

    return data, errors

PageletForm.extractData = extractData

def wizardExtractData(self, setErrors=True):
    data, errors = super(WorkspacesManagement, self).extractData(setErrors=setErrors)

    errs = []
    for error in errors:
        if IErrorViewSnippet.providedBy(error) and \
                removeAllProxies(error).field.__name__=='enabledWorkspaces':
            continue
        errs.append(error)

    return data, tuple(errs)

WorkspacesManagement.extractData = wizardExtractData
