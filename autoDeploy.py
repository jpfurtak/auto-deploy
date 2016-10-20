#!/usr/bin/env python

import cvp
import json
import requests
import yaml

## Stuff to install
## sudo pip install requests
## sudo pip install PyYAML

CVPCONFIGFILE = "./settings/cvpconfig.yaml"

class CvpSettings(object):

    """ Stores the CVP configuration settings
    """
    def __init__(self):
        
        cvpconfig = yaml.safe_load(open(CVPCONFIGFILE))
        
        self.cvphost = cvpconfig['cvp_setting']['cvphost']
        self.cvpuser = cvpconfig['cvp_setting']['cvpuser']
        self.cvppasswd = cvpconfig['cvp_setting']['cvppasswd']
        self.config = cvpconfig['cvp_setting']['settings_configlet']

def main():
    
    ## Load CVP Settings
    
    cvpsettings = CvpSettings()
    server = cvp.Cvp(cvpsettings.cvphost)
    server.authenticate(cvpsettings.cvpuser, cvpsettings.cvppasswd)
    
    
    #configfile = server.getConfiglet(cvpsettings.config)
    #config = yaml.safe_load(configfile.config)
    
    undefined = [d for d in server.getDevices() if d.containerName == 'Undefined']
    
    print undefined
    
if __name__ == '__main__':
   main()