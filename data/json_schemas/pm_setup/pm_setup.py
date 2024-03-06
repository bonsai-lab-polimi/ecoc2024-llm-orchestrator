import requests
import urllib3

from cookie import cookie

from Simulator.Offline_Pipeline.PM_Setup.pm_parameters import json_data,params,path,device

#use to diable the warning (insecurerequestwarning)
urllib3.disable_warnings()

def pmcreation():
    session = requests.session()
    
    cookies = cookie(path)
    session.verify = False
    
    headers = {
        'accept': '*/*',
        'Content-Type': 'application/json',
    }

    response = session.post('https://{}/onc/nbi/pmCampaign'.format(device), params=params, headers=headers, json=json_data, cookies=cookies)
    print(response.status_code)    
    if response.status_code == 200:
        message = 'PM Creation successful'
    else:
        message = 'PM Creation failed'

    session.close()

    return message

def main():
    print('Starting the Performance Monitoring Campaign creation')
    
    message = pmcreation()

    print(message)

if __name__ == main():
    main()
    