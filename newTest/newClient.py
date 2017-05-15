from apiclient import discovery
import httplib2
from oauth2client.client import OAuth2Credentials
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
import webbrowser
import time
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('param', help='Choose what information about this device to display')

email = 'zmz305@gmail.com'
name = ''
client_id = '804117852738-53pqeftc47o0ng0tbj7ork43hjld2uej.apps.googleusercontent.com'
client_secret = '1jxre9jE82zbDtVCxbwzo6Im'

#lock
# device_id = 'devices/0-0b83a7d3-6bd7-42b6-ac83-7d4ac47aa3cc'
# manifest_id = 'AIAAA'

#hvac
device_id = 'devices/0-228839ca-5776-4e21-9b5e-9b66f458b255'
manifest_id = 'AHAAA'

# standard light
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

def build_service(credentials):
    api_client = discovery.build('weavecompanion', 'v1',
                                 discoveryServiceUrl='https://{api}' +
                                 '.googleapis.com/$discovery/rest?version={apiVersion}',
                                 http=credentials.authorize(httplib2.Http()))
    return api_client

def printStuff(data, description=''):
    print(description)
    print(json.dumps(data, indent=2, sort_keys=True))

def get_all_devices(api_client):
    devices = api_client.devices().list().execute();
    return devices

def get_device(api_client):
    device = api_client.devices().get(name=device_id).execute()
    return device

def get_device_component(device):
    return device['components']

def get_device_state(device):
    return device['state']

def get_device_commands(device):
    return None

def get_device_traits(device):
    return device['traits']

def get_commands(api_client):
    result = api_client.devices().commands().list(device=device_id).execute()
    return result

# def get_device_traits(api_client):
#     traits = api_client.devices().traits().execute()

# def get_device_properties(api_client):
#     properties = api_client.devices().properties()

def get_device_provision(api_client):
    provision = api_client.devices().provision(body={'model_manifest_id': 'AIAAA'}).execute()
    return provision

def create_command(api_client, body):

    return None

if __name__ == '__main__':
    args = parser.parse_args()
    credentials = connect()
    time.sleep(0.1)
    api_client = build_service(credentials)
    device = get_device(api_client)
    if 'device' ==  args.param:
        printStuff(device)
    elif 'devices' == args.param:
        devices = get_all_devices(api_client)
        printStuff(devices)
    elif 'commands' == args.param:
        # commands = get_device_commands(device)
        commands = get_commands(api_client)
        printStuff(commands)
    elif 'register' == args.param:
        reg_info = get_device_provision(api_client)
        printStuff(reg_info, 'Registration information')
    elif 'state' == args.param:
        printStuff(get_device_state(device))
    elif 'components' == args.param:
        printStuff(get_device_component(device))
    elif 'traits' == args.param:
        printStuff(get_device_traits(device))
    elif 'create_command' == args.param:
        body = {}
        create_command(api_client, body)
    else:
        print('Unrecognized command argument: ' + args.param)
    # properties = get_device_properties(api_client)
    # printStuff(properties)
    # devices = get_all_devices(api_client)
    # printStuff(devices)
    # device = get_device(api_client)
    # commands = get_commands(api_client)
    # printStuff(commands)
    # printStuff(get_device_component(device))
    # printStuff(get_device_state(device))