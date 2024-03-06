#Performance Monitoring Campaigns Creation Parameters

#Device IP address
device = '10.79.23.39:8443'

#Location of the authentication file
path='/home/SMO/SMO-Pipeline-offline-testbed/SMO-Pipeline-offline-testbed/'

#PM Campaign Name
params = {
        'name': 'pm_name',
    }

#Configuration Details
json_data = {
    #the configuration state for the PM (Performance Monitoring) session is always set to "started"
    "configurationState": "started",

    #the PM can be either with 15 minute granularity (cd15m) or a 24 hour granularity (cd24h)
    #the possible values for the "pm" are "disabled", "enabledCurrent", and "enabledCurrentAndArchive"
    "pm": {
        "cd15m": "enabledOnlyCurrent",
        "cd24h": "enabledOnlyCurrent"
    },
    #the "transports" field should specify the connection for which the peformance monitoring should be initiated
    #the "transports" name field should match the field of a lightpath and/or a service
    "transports": [
    {
        "name" : "lightpath_name",
        "name" : "service_name",
    }
    ]
}
