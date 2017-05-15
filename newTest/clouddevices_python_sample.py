from apiclient.discovery import build_from_document
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
import httplib2
import json
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# See the "Authorizing requests" documentation on how to set up your
# project and obtain
# client ID, client secret and API key:
# https://developers.google.com/cloud-devices/v1/dev-guides/getting-started/authorizing#setup
OAUTH_CLIENT_ID="369783136059-8ca5fspi8ums09h27pt8h81dlbcmqpk9.apps.googleusercontent.com"
OAUTH_SECRET="zynmUHiRoy_YqhtrcItCp14X"
API_KEY="AIzaSyBQVYDaCiUHkpjppZoeTsih7bDXklXFyoG4A"
OAUTH_SCOPE="https://www.googleapis.com/auth/weave.app"

# Command definitions of a new device if we need to create it.
# More about commands and command definitions:
# https://developers.google.com/cloud-devices/v1/dev-guides/getting-started/commands-intro
DEVICE_DRAFT = {
  "kind": "weave#device",
  'id': 'NAS12418',
  'deviceKind': 'vendor',
  'modelManifestId' : 'AAeqN',
  'channel': {
    'supportedType': 'xmpp'
  },
  'commandDefs': {
    'storage': {
      'list': {
        'parameters': {
          'path': {
            'type': 'string',
            'isRequired': True
          },
          'continuationToken': {'type': 'string'},
          'entryCount': {'type': 'integer'}
        }
      },
      '_blinkLed': {
      },
    },
  },
  "personalizedInfo": {
    "name": 'Network Access Storage',
  },
}

# More details at: https://developers.google.com/api-client-library/python/guide/aaa_oauth
def get_credentials():
  storage = Storage('credentials.dat')
  credentials = storage.get()
  if credentials is None or credentials.invalid:
    # There are also other flows that may be used for authorization:
    # https://developers.google.com/accounts/docs/OAuth2
    flow = OAuth2WebServerFlow(OAUTH_CLIENT_ID, OAUTH_SECRET, OAUTH_SCOPE, redirect_uri="oob")
    url = flow.step1_get_authorize_url()
    print ('Navigate to the following URL to allow access to Cloud Devices, '
        'then paste the given code here.\n%s' % url)
    code = raw_input("Authorization code: ")
    # If you have SSL problems at this step, check that certificates are world-readable.
    # Usually at the following path:
    # sudo chmod a+r /usr/local/lib/python2.7/dist-packages/httplib2/cacerts.txt
    credentials = flow.step2_exchange(code)
    storage.put(credentials)
  return credentials

def create_device(api_client):
  ticket = {
    'userEmail': 'me',
    'oauthClientId': OAUTH_CLIENT_ID,
    'deviceDraft': DEVICE_DRAFT
  }
  ticket = api_client.registrationTickets().insert(body=ticket).execute()
  ticket = api_client.registrationTickets().finalize(registrationTicketId=ticket['id']).execute()
  device = ticket['deviceDraft']
  print 'Created new device: %s' % device['id']
  return device

def main():
  # Load the local copy of the discovery document. discovery.json file is available to download
  # from the samples documentation page:
  # https://developers.google.com/cloud-devices/v1/samples/samples
  f = file(os.path.join(os.path.dirname(__file__), "discovery.json"), "r")
  discovery = f.read()
  f.close()

  # Get OAuth 2.0 credentials and authorize.
  http = httplib2.Http()
  credentials = get_credentials()
  http = credentials.authorize(http)

  # Construct an API client interface from the local documents
  api_client = build_from_document(discovery,
      base="https://www.googleapis.com/weave.app/v1/",
      http=http)

  print "Created a API Client\n"
  #response = api_client.commands().list().execute()
  #print response



  # Listing devices, request to devices.list API method, returns a list of devices
  # available to user. More details about the method:
  # https://developers.google.com/cloud-devices/v1/reference/cloud-api/devices/list
  print "Here " + str(type(api_client))
  object = api_client.devices()
  print "There " + str(type(object))
  print api_client.devices().list()
  response = api_client.devices().list().execute()

  print json.dumps(response, indent=2)

  devices = response.get('devices', [])
  if not devices:
    print 'No devices, creating one.'

    device = create_device(api_client)
  else:
    device = devices[0]
  print 'Available device: %s' % device['id']

  print 'Sending a new command to the device'
  command = {
    'name': 'storage.list',  # Command name to execute.
    'parameters': {
      'path': '/tmp'  # Required command parameters
    },
    'deviceId': device['id']  # Device to send the command to.
  }
  # Calling commands.insert method to send command to the device, more details about the method:
  # https://developers.google.com/cloud-devices/v1/reference/cloud-api/commands/insert
  command = api_client.commands().insert(body=command).execute()

  # The state of the command will be "queued". In normal situation a client may request
  # command again via commands.get API method to get command execution results, but our fake
  # device does not actually receive any commands, so it will never be executed.
  print 'Sent command to the device:\n%s' % json.dumps(command, indent=2)

if __name__ == '__main__':
  main()
