from apiclient import discovery
import httplib2
from oauth2client.client import OAuth2Credentials
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from time import sleep
import webbrowser
import time
import json
import argparse
import os


email = 'zmz305@gmail.com'
name = ''
client_id = '804117852738-53pqeftc47o0ng0tbj7ork43hjld2uej.apps.googleusercontent.com'
client_secret = '1jxre9jE82zbDtVCxbwzo6Im'

# lock
# device_id = 'devices/0-0b83a7d3-6bd7-42b6-ac83-7d4ac47aa3cc'
# manifest_id = 'AIAAA'

# hvac controller
device_id = 'devices/0-228839ca-5776-4e21-9b5e-9b66f458b255'
manifest_id = 'AHAAA'

# # standard light
# device_id = 'devices/0-49f188cc-07e9-4012-9418-bb0caee94a2d'
# manifest_id = 'AIAAA'

def connect():
    storage = Storage('newCredential.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        flow = OAuth2WebServerFlow(client_id=client_id,
                                   client_secret=client_secret,
                                   scope='email https://www.googleapis.com/auth/weave.app',
                                   redirect_uri='urn:ietf:wg:oauth:2.0:oob',
                                   login_hint=email)
        url = flow.step1_get_authorize_url()
        webbrowser.open(url)
        print(url + '\n')
        code = raw_input()
        credentials = flow.step2_exchange(code)
        storage.put(credentials)
        print(credentials.to_json())
    return credentials

def get_device(api_client):
    device = api_client.devices().get(name=device_id).execute()
    return device

def build_service(credentials):
    api_client = discovery.build('weavecompanion', 'v1',
                                 discoveryServiceUrl='https://{api}' +
                                 '.googleapis.com/$discovery/rest?version={apiVersion}',
                                 http=credentials.authorize(httplib2.Http()))
    return api_client


def create_command(api_client, body):
    result = api_client.devices().commands().create(body=body, device=device_id).execute();
    return result

def buildDictFromFile(filename):
    res = {}
    with open(filename) as f:
        lines = f.read()
        res = json.loads(lines)
    return res

def c_cm(state):
    return state['coolSubsystem']['state']['hvacSubsystemController']['controllerMode']

def h_cm(state):
    return state['heatSubsystem']['state']['hvacSubsystemController']['controllerMode']

def c_sss(state):
    return state['coolSubsystem']['state']['hvacSubsystemController']['subsystemState']

def h_sss(state):
    return state['heatSubsystem']['state']['hvacSubsystemController']['subsystemState']

def hc_sss(state):
    return state['heatCoolSubsystem']['state']['hvacSubsystemController']['subsystemState']

def hc_cm(state):
    return state['heatCoolSubsystem']['state']['hvacSubsystemController']['controllerMode']

def testCoolingModeToAutoDisablesOthers():
    body = {'commandName': 'coolSubsystem/hvacSubsystemController.setConfig', 'parameters': {'controllerMode': 'auto'}}
    result = create_command(api_client, body)
    print(result)
    os.system('python newClient.py state > hvac_state')
    state = buildDictFromFile('hvac_state')
    assert(c_cm(state) == 'auto'), 'case1 1'
    assert(h_cm(state) == 'disabled'), 'case1 2'
    assert(c_sss(state) == 'off' or c_sss(state) == 'on'), 'case1 3'
    assert(h_sss(state) == 'off'), 'case1 4'
    assert(hc_cm(state) == 'disabled'), 'case1 5'
    assert(hc_sss(state) == 'off'), 'case1 6'
    print('Pass case1')

def case2():
    os.system('python newClient.py state > hvac_state')
    state = buildDictFromFile('hvac_state')
    pre_heat_controller_mode = h_cm(state)
    pre_heat_state = h_sss(state)
    pre_hc_controller_mode = hc_cm(state)
    body = {'commandName': 'coolSubsystem/hvacSubsystemController.setConfig', 'parameters': {'controllerMode': 'disabled'}}
    result = create_command(api_client, body)
    print(result)
    os.system('python newClient.py state > hvac_state')
    state = buildDictFromFile('hvac_state')
    cur_heat_controller_mode = h_cm(state)
    cur_heat_state = h_sss(state)
    cur_hc_controller_mode = hc_cm(state)
    assert(cur_hc_controller_mode == pre_hc_controller_mode), 'case2 1'
    assert(cur_heat_controller_mode == pre_heat_controller_mode), 'case2 2'
    assert(cur_heat_state == pre_heat_state), 'case2 3'
    assert(c_cm(state) == 'disabled'), 'case2 4'
    assert(hc_sss(state) == 'off'), 'case2 5'
    print('Pass case2')

def case3():
    body = {'commandName': 'heatSubsystem/hvacSubsystemController.setConfig', 'parameters': {'controllerMode': 'auto'}}
    result = create_command(api_client, body)
    print(result)
    os.system('python newClient.py state > hvac_state')
    state = buildDictFromFile('hvac_state')
    assert(c_cm(state) == 'disabled'), 'case2 1'
    assert(h_cm(state) == 'auto'), 'case2 2'
    assert(c_sss(state) == 'off'), 'case2 3'
    assert(h_sss(state) == 'off' or c_sss(state) == 'on'), 'case2 4'
    assert(hc_cm(state) == 'disabled'), 'case2 5'
    assert(hc_sss(state) == 'off'), 'case2 6'
    print('Pass case3')

def case4():
    os.system('python newClient.py state > hvac_state')
    state = buildDictFromFile('hvac_state')
    pre_cool_controller_mode = c_cm(state)
    pre_cool_state = c_sss(state)
    pre_hc_controller_mode = hc_cm(state)
    body = {'commandName': 'heatSubsystem/hvacSubsystemController.setConfig', 'parameters': {'controllerMode': 'disabled'}}
    result = create_command(api_client, body)
    print(result)
    os.system('python newClient.py state > hvac_state')
    state = buildDictFromFile('hvac_state')
    cur_cool_controller_mode = c_cm(state)
    cur_cool_state = c_sss(state)
    cur_hc_controller_mode = hc_cm(state)
    assert (cur_hc_controller_mode == pre_hc_controller_mode), 'case4 1'
    assert (cur_cool_controller_mode == pre_cool_controller_mode), 'case4 2'
    assert (cur_cool_state == pre_cool_state), 'case4 3'
    print(h_cm(state))
    assert (h_cm(state) == 'disabled'), 'case4 4'
    assert (hc_sss(state) == 'off'), 'case4 5'
    print('Pass case4')

def case5():
    body = {'commandName': 'heatCoolSubsystem/hvacSubsystemController.setConfig', 'parameters': {'controllerMode': 'auto'}}
    result = create_command(api_client, body)
    print(result)
    os.system('python newClient.py state > hvac_state')
    state = buildDictFromFile('hvac_state')
    assert(c_cm(state) == 'disabled'), 'case5 1'
    assert(h_cm(state) == 'disabled'), 'case5 2'
    assert(c_sss(state) == 'off' or c_sss(state) == 'on'), 'case5 3'
    assert(h_sss(state) == 'off' or h_sss(state) == 'on'), 'case5 4'
    assert(hc_cm(state) == 'auto'), 'case5 5'
    assert(hc_sss(state) == 'off'), 'case5 6'
    print('Pass case5')

def case6():
    os.system('python newClient.py state > hvac_state')
    state = buildDictFromFile('hvac_state')
    pre_heat_controller_mode = h_cm(state)
    pre_cool_controller_mode = h_cm(state)
    pre_hc_controller_mode = hc_cm(state)
    pre_heat_state = h_sss(state)
    pre_cool_state = c_sss(state)
    body = {'commandName': 'heatCoolSubsystem/hvacSubsystemController.setConfig', 'parameters': {'controllerMode': 'disabled'}}
    result = create_command(api_client, body)
    print(result)
    os.system('python newClient.py state > hvac_state')
    state = buildDictFromFile('hvac_state')
    assert(h_cm(state) == pre_heat_controller_mode), 'case6 1'
    if(pre_hc_controller_mode == 'auto'):
        assert(h_sss(state) == 'off'), 'case6 2'
        assert(c_sss(state) == 'off'), 'case6 3'
    else:
        assert(h_sss(state) == pre_heat_state), 'case6 4'
        assert(c_sss(state) == pre_cool_state), 'case6 5'
    assert(c_cm(state) == pre_cool_controller_mode), 'case6 6'
    assert(hc_cm(state) == 'disabled')
    assert(hc_sss(state) == 'off')
    print('Pass case6')




if __name__ == '__main__':
    credentials = connect()
    sleep(0.1)
    api_client = build_service(credentials)
    device = get_device(api_client)

    # case1()
    # case2()
    # case3()
    # case4()
    # case5()
    # case6()

    # body = {'commandName': 'displayUnits/tempUnitsSetting.setConfig',
    #         'parameters': {'units': 'celsius'}}
    # result = create_command(api_client, body)
    # print(result)

    # body = {'commandName': 'coolSubsystem/hvacSubsystemController.setConfig', 'parameters': {'controllerMode': 'auto'}}
    # result = create_command(api_client, body)
    # print(result)

    # body = {'commandName': 'heatSubsystem/hvacSubsystemController.setConfig', 'parameters': {'controllerMode': 'auto'}}
    # result = create_command(api_client, body)
    # print(result)
    #
    body = {'commandName':'heatSetting/tempSetting.setConfig', 'parameters':{'degreesCelsius': 10}}
    result = create_command(api_client, body)
    print(result)

    # body = {'commandName': 'heatCoolSubsystem/hvacSubsystemController.setConfig', 'parameters': {'controllerMode': 'auto'}}
    # result = create_command(api_client, body)
    # print(result)

    # Cannot make this one work!!!!!
    # body = {'commandName':'coolSetting/tempSetting.setConfig', 'parameters':{'degreeCelsius': 10}}
    # result = create_command(api_client, body)
    # print(result)


    # For lights:

    # body = {'commandName': 'powerSwitch/onOff.setConfig', 'parameters': {'state': 'on'}}
    # result = create_command(api_client, body)
    # print(result)
    #
    # body = {'commandName': 'dimmer/brightness.setConfig', 'parameters': {'brightness': 0.5}}
    # result = create_command(api_client, body)
    # print(result)

