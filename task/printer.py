# -*- coding: utf-8 -*-
from amortization.task.models import Firm

__author__ = 'cm'

import sys, os, logging
import uno
from com.sun.star.uno import Exception as UnoException
from com.sun.star.task import ErrorCodeIOException
from amortization.settings import MEDIA_ROOT, MEDIA_URL
from amortization.debug import debug, error

# soffice --accept="socket,host=localhost,port=2002;urp;StarOffice.ServiceManager" --norestore -nofirstwizard --nologo --headless &

def get_document(file_name):
    path = os.path.join(MEDIA_ROOT, "template_docs/" + file_name)
    debug(__name__, path)
    
    local = uno.getComponentContext()
    resolver = local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local)

    document = None
    try:
        context = resolver.resolve( "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext" )
        desktop = context.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", context)
        document = desktop.loadComponentFromURL("file://" + path, "_blank", 0, ())
    except UnoException, e:
        error(__name__,"OpenOffice connection error: %s" % e.Message)
        return None

    debug(__name__, "Connected to OpenOffice")
    return document

def replace(document, what, for_what):
  ReplaceDescr = document.createReplaceDescriptor()
  ReplaceDescr.SearchString = "$%s" % what
  ReplaceDescr.ReplaceString = for_what
  Found = document.replaceAll( ReplaceDescr )

def generate(document, values, save_to):
    for k in values.keys():
        replace(document, k, values[k])

    file_name = 'file://' + save_to
    if file_name[-4:] != '.odt':
        file_name += '.odt'
    try:
        document.storeAsURL(file_name, ())
    except ErrorCodeIOException, e:
        error(__name__, "File writing error: %s" % e.Message)
        
    debug(__name__, "Saved file: %s" % file_name)
    return file_name

def fill_data(keys, obj):
    data = {}
    for k in keys:
        data[k] = getattr(obj, k, "<!!>")

    return data

def expertise_result(req, rewrite=False):
    if req.doc_url:
        return req.doc_url

    document = get_document('result.odt')
    if document:
        path = os.path.join(MEDIA_ROOT, "docs/") + req.number
        keys = ('address', 'inn', 'bank', 'racc', 'cacc', 'bic', 'boss_name')

        firm = Firm.objects.filter(for_print=True)
        if firm:
            firm = firm[0]
            data = fill_data(keys, firm)
        else:
            document.dispose()
            return ''

        keys_req = ('number', 'serial', 'device', 'year')
        data.update(fill_data(keys_req, req))

        res = generate(document, data, path)
        url = os.path.join(MEDIA_URL, "docs/" + req.number + ".odt")
        if res:
            req.doc_url = url
            req.save()
        document.dispose()
        return req.doc_url

    return ''
