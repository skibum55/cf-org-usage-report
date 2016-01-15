#!/usr/bin/env python
#Script runs as whoever is logged into the CF API. 
from subprocess import check_output
import json 
import numbers

orgs = json.loads(check_output(['cf', 'curl', '/v2/organizations']))

for org in orgs['resources']:
    name = org['entity']['name']
    guid = org['metadata']['guid']
    spaces_url = org['entity']['spaces_url']
    spaces = json.loads(check_output(['cf', 'curl', spaces_url]))
    for space in spaces['resources']:
        apps_url = space['entity']['apps_url']
        consumed = 0
        apps = json.loads(check_output(['cf', 'curl', apps_url]))
        print "Org " + name + " - Space " + space['entity']['name']
        for app in apps['resources']:
            instances = app['entity']['instances']
            memory = app['entity']['memory']
            consumed += (instances * memory)
            if app['entity']['state'] <> 'STOPPED':
                instances_url = app['metadata']['url'] + '/instances'
                instances = json.loads(check_output(['cf', 'curl', instances_url]))
                for i in instances:
#                    print  instances[i]['state']
                     state = instances[i]['state']
                     print "\tState is " + state + " for " + app['entity']['name'] + '/' + i
