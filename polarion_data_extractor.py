#!/usr/bin/env python

from zeep import Client
from zeep.plugins import HistoryPlugin

import re
from lxml.etree import Element
from lxml import etree

##### feed the initial data here .....!!!


url = "https://almdemo.polarion.com/polarion" #
username= "bhavesh.itankar@gmail.com"  #xjh0qx
password= "VnT4wryC$" #aptiv@june20
project_id = 'bhavesh.itankar_gmail.com'
type = 'systemrequirement'
###############################################
###############################################

history = HistoryPlugin()
session = Client(wsdl=url + '/ws/services/SessionWebService?wsdl', plugins=[history])
session.service.logIn(username, password)
tree = history.last_received['envelope'].getroottree()
sessionHeaderElement = tree.find('.//{http://ws.polarion.com/session}sessionID')
__tracker = Client(wsdl=url + '/ws/services/TrackerWebService?wsdl', plugins=[history])
__tracker.set_default_soapheaders([sessionHeaderElement])

__tracker.wsdl.messages['{http://ws.polarion.com/TrackerWebService}getModuleWorkItemsRequest'].parts['parameters'].element.type._element[1].nillable = True
__tracker.service.getModuleWorkItemUris._proxy._binding.get('getModuleWorkItemUris').input.body.type._element[1].nillable = True
__tracker.service.getModuleWorkItemUris._proxy._binding.get('getModuleWorkItems').input.body.type._element[1].nillable = True

data = __tracker.service.queryWorkItems('project.id:%s AND type:%s' % (project_id, type),'id',['id','title','description', 'linkedWorkItems'])

#uri = 'subterra:data-service:objects:/default/%s${Module}{moduleFolder}%s#%s' % (project_id, document_folder, document_name)
#__tracker.service.getModuleWorkItems(uri, None, True, ['id','title','type','description', 'linkedWorkItems'])
