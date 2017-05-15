from apiclient.discovery import build_from_document
import httplib2
import argparse
import os
from oauth2client.file import Storage
from oauth2client import client
import string
import logging
import random
from googleapiclient.errors import HttpError
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import json
# logging.getLogger().addHandler(logging.StreamHandler())

# random.seed(100)                # Seeding the random function. What is a good seed?

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.basicConfig(filename='./logs/random_commands_' + time.strftime("%Y%m%d-%H%M%S") + '.log')
# httplib2.debuglevel = 2

APP_ROLE = ["user"]

# Account details for a Google Account with access to weave
GOOGLE_USERNAME = "USERNAME"
GOOGLE_PASSWORD = "PASSWORD"

DEVICES = []
MAX_SEQ_LENGTH = 10


# Simulates loging in to a Google Account and authorizing the app to use devices
# Requires a valid Google Account with permission to use the weave platform
def authorizeApps(authorization_token):
    try:
        browser = webdriver.Chrome()
        browser.get('https://accounts.google.com/Login#identifier')
        action = webdriver.ActionChains(browser)
        emailElem = browser.find_element_by_id('Email')
        emailElem.send_keys(GOOGLE_USERNAME)
        nextButton = browser.find_element_by_id('next')
        nextButton.click()
        time.sleep(1)
        passwordElem = browser.find_element_by_id('Passwd')
        passwordElem.send_keys(GOOGLE_PASSWORD)
        signinButton = browser.find_element_by_id('signIn')
        signinButton.click()
        browser.get('https://weave.google.com/manager/share?role=user&token=' + authorization_token)
        time.sleep(3)
        nextButton = browser.find_element(By.XPATH, "//paper-button")
        nextButton.click()
    except:
        manager_url = 'https://weave.google.com/manager/share?role=user&token=' + authorization_token
        print "ERROR : Unable to automatically provide authorization"
        raw_input("Please provide permission to access apps by visiting : \n" + manager_url)


def getRandomNumber(type_spec, random_func):
    int_max = 10000  # sys.maxsize
    int_min = -10000  # -sys.maxsize - 1
    if 'minimum' in type_spec:
        int_min = type_spec['minimum']
    if 'maximum' in type_spec:
        int_max = type_spec['maximum']
    return random_func(int_min, int_max)


def getRandomString(type_spec):
    alpha = 0.5  # 0.5 is the shape of the pareto distribution used to bias towards smaller strings
    len_min = 0
    len_max = 100
    if 'maxLength' in type_spec:
        len_min = type_spec['maxLength']
    if 'minLength' in type_spec:
        len_max = type_spec['minLength']
    str_len = min(len_min + int(random.paretovariate(alpha)) - 1, len_max)
    return ''.join(random.choice(string.lowercase) for i in xrange(str_len))


def getRandomArray(type_spec):
    # TODO : Fix the length to read from the definition if exists
    arrayLength = 10
    return [getRandomFromType(type_spec["items"]) for _ in xrange(arrayLength)]


# TODO : ignoring the required, additional keywords and generating for all now
def getRandomObject(type_spec):
    temp_obj = {}
    for prop in type_spec['properties']:
        temp_obj[prop] = getRandomFromType(type_spec['properties'][prop])
    return temp_obj


# Returns a random variable for a given type
def getRandomFromType(type_spec):
    if 'enum' in type_spec:
        assert len(type_spec['enum']), "Enum type with 0 elements"
        return random.choice(type_spec['enum'])  # [random.randint(0, len(type_spec['enum']) - 1)]
    if type_spec['type'] == 'integer':
        return getRandomNumber(type_spec, random.randint)
    if type_spec['type'] == 'number':
        return getRandomNumber(type_spec, random.uniform)
    if type_spec['type'] == 'boolean':
        return random.choice([True, False])
    if type_spec['type'] == 'string':
        return getRandomString(type_spec)
    if type_spec['type'] == 'array':
        return getRandomArray(type_spec)
    if type_spec['type'] == 'object':
        return getRandomObject(type_spec)
    assert False, "Undefined type specification"

# Builds the message for a Weave command based on the spevcification. Random values are used
def getCommandBodyFromSpec(deviceId, command_name, spec):
    temp_parameters = {}
    if 'parameters' in spec:
        for para in spec['parameters']:
            temp_parameters[para] = getRandomFromType(spec['parameters'][para])
    command = {
        'name': command_name,  # Command name to execute.
        'parameters': temp_parameters,
        'deviceId': deviceId  # Device to send the command to.
    }
    return command


# Get the device state from Weave cloud API
def getDeviceState(deviceId, api_client_in):
    response = api_client_in.devices().get(deviceId=deviceId).execute()
    return response


# Get the state of the device. Return true if it is True
def isDeviceAlive(deviceId, api_client):
    state = getDeviceState(deviceId, api_client)
    isOnline = state["connectionStatus"]
    print "==========> ", isOnline
    if isOnline == "online":
        return True
    else:
        return False


def withUserPermissions(spec):
    if 'minimalRole' in spec:
        if 'user' != spec['minimalRole']:
            return False
    return True


# Three random picks. Can be made cleaner
def getRandomCommand(device):
    return random.choice(device['commands'])


# The device representation on 09/12/2016 changed to two possible ways to represent allowed commands
# Whether this is a bug or expected behaviour is unclear
# This function creates an internal data structure to hold the device data
def parseDevices(devices):
    device_list = []
    for device in devices:
        temp_device = {}
        temp_device['id'] = device['id']
        temp_device['starting-state'] = device['state']
        if "commandDefs" in device.keys():
            temp_command_list = []
            for component in device['commandDefs']:
                temp_comp = device['commandDefs'][component]
                for command in temp_comp:
                    temp_command_list.append({'name': component + '.' + command,
                                              'command_spec': temp_comp[command]})
            temp_device["commands"] = temp_command_list
            device_list.append(temp_device)
        elif "traits" in device.keys():
            temp_command_list = []
            for component in device['traits']:
                temp_comp = device['traits'][component]
                if 'commands' not in temp_comp:
                    continue
                for command in temp_comp['commands']:
                    temp_command_list.append({'name': component + '.' + command,
                                              'command_spec': temp_comp["commands"][command]})
            temp_device["commands"] = temp_command_list
            device_list.append(temp_device)
    return device_list


def startDevice(device_command, api_client, email, outfile):
    try:
        ticket = api_client.devices().provision(body={'model_manifest_id': args.model_manifest_id}).execute()
        reg_option = " -r=" + ticket['id']
        proc = subprocess.Popen([device_command, reg_option],
                                cwd="/home/zmz/workspace/research/iot_stuff/libiota",
                                )
        time.sleep(5)
        print "Successfully started the device"
        response = api_client.devices().get(deviceId=ticket["deviceId"]).execute()
        logging.debug(response)
        return proc, response
    except Exception as e:
        print "Failed to start the device : ", e
        exit(-1)


def reStartDevice(device_command, outfile):
    try:
        proc = subprocess.Popen(device_command, cwd="/home/zmz/workspace/research/iot_stuff/libiota")
        print "Successfully re-started the device"
        return proc
    except Exception as e:
        print "Failed to restart the device : ", e
        exit(-1)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Random Command Sequence Generator for IoT devices')
    parser.add_argument('--email', metavar='user-email', required=True,
                        help='Email to use for registering devices')
    parser.add_argument('--device_command', required=True, help='The command to run the device program')
    parser.add_argument('--output', help='Output file', default="output.txt")

    args = parser.parse_args()

    USER_EMAIL = args.email
    DEVICE_COM = args.device_command

    # Establish authentication for the application. Either use an exsisting authentication
    # If no authorization is not available, Go to the link and copy paste the code
    # Can be automated with selenium, but not needed as it is a one time thing
    try:
        storage = Storage('my_credentials.dat')
        credentials = storage.get()
        if credentials is None or credentials.invalid:
            flow = client.flow_from_clientsecrets(
                'client_secrets.json',
                scope='https://www.googleapis.com/auth/weave.app',
                redirect_uri="oob")
            auth_url = flow.step1_get_authorize_url()
            print ('Navigate to the following URL to allow access to Cloud Devices, '
                   'then paste the given code here.\n%s' % auth_url)
            code = raw_input("Authorization code: ")
            credentials = flow.step2_exchange(code)
            storage.put(credentials)

        http = httplib2.Http()
        http = credentials.authorize(httplib2.Http())

        f = file(os.path.join(os.path.dirname(__file__), "weave-discovery2.json"), "r")
        discovery = f.read()
        service = api_client = build_from_document(discovery, http=http)
    except Exception as e:
        print(e)
        print "Unable to Establish Connection to the Google Weave API"
        exit(-1)

    print "Created an API Client with Athorization\n"

    # Start the device prgram and register it with weave using a generated authentication ticket
    device_output = open("device_output.txt", "wb")

    # Store the generated device sequences
    no_permission_commands = []
    failed_commands = []
    successful_commands = []

    seq_len = 0
    sequences = []
    failing_sequences = []

    print "Testing Device : ", DEVICE_COM

    while len(sequences) + len(failing_sequences) < 10:
        temp_seq = []
        fail = False

        # Restart the device to allow new sequences
        proc1, response = startDevice(DEVICE_COM, api_client, USER_EMAIL, device_output)

        # Uncomment the lines if the device is not automatically authorized
        # tokens = api_client.authorizedApps().createappauthenticationtoken().execute()
        # authorizeApps(tokens['token'])

        # Parse and build the data structures used to store devices
        device = parseDevices([response])[0]

        while seq_len < MAX_SEQ_LENGTH and not fail:
            print "--------------------"

            # Get a random command from the device
            selected_command = getRandomCommand(device)
            print "Testing Command : ", selected_command['name']
            if withUserPermissions(selected_command['command_spec']):
                # Run the command if the "user" role is enough to run it
                # Get the body for the command API call
                command_body = getCommandBodyFromSpec(device['id'],
                                                      selected_command['name'],
                                                      selected_command['command_spec'])
                print command_body
                try:
                    # Run the command
                    command_out = api_client.commands().insert(body=command_body).execute()
                    temp_seq.append((selected_command['name'], command_body, command_out))
                    # Sleep to allow the command to run. This can be skipped
                    time.sleep(10)
                    if isDeviceAlive(device['id'], api_client):
                        print "Result : Success : ", command_out
                        seq_len += 1
                    else:
                        print "Device went offline : Assumed due to error"
                        fail = True
                except HttpError as e:
                    failed_commands.append((selected_command, command_body, e))
                    print "Result : Failure : ", e
                    temp_seq.append((selected_command['name'], command_body, command_out))
                    fail = True
            else:
                print "Result : No Permission"
                no_permission_commands.append((device, selected_command))
        if fail:
            failing_sequences.append(temp_seq)
        else:
            sequences.append(temp_seq)
        print "----------------------------------------"
        seq_len = 0
        proc1.terminate()
        # proc1, response = startDevice(DEVICE_COM, api_client, USER_EMAIL, device_output)
        # device = parseDevices([response])[0]

    # Write the output to a file and exit
    with open("output.txt", "w") as output_file:
        output_file.write("Device Under Test : \n")
        output_file.write(json.dumps(response, indent=2))
        output_file.write("\nFailing Sequences : \n")
        output_file.write(json.dumps(failing_sequences, indent=2))
        output_file.write("\nPassing Sequences : \n")
        output_file.write(json.dumps(sequences, indent=2))
    proc1.terminate()
