### Often used commands
- make -C examples/host/light
- ./out/host/examples/light/light
- ./weave_client account -l/-a ...
- ./weave_client config ...



### Oauth for weave daemon will expire and will need to refresh
```
[(6947535.571)I gcm.c:816] Connecting to GCM
[(6947535.571)I gcm.c:838] Sending GCM connect request to url: https://fcm.googleapis.com/fcm/bind?token=dffn0B6Pp-0%3AAPA91bHZtXoPKjGCyEfYi3TzRvmBqHZrv4rjUs7Q4Ioyxn9HR1UaXAQ5KB-obe2MNI75G80Y9CctkoNMupCOk_bcQkpoyuECGzbbO7WlCXAZs99oV9xePXINKuN6UTFxYx-qj_eSfVGM
[(6947642.805)I weave.c:181] OAuth Token Expired
[(6947642.805)I weave.c:345] Sending OAuth Refresh Request
[(6947642.805)I weave_http.c:98] Sending POST Request https://accounts.google.com/o/oauth2/token

```

### Weave periodically sends a GCM connect request to fcm.googleapis.com
```
[(6949340.775)I gcm.c:838] Sending GCM connect request to url: https://fcm.googleapis.com/fcm/bind?token=dffn0B6Pp-0%3AAPA91bHZtXoPKjGCyEfYi3TzRvmBqHZrv4rjUs7Q4Ioyxn9HR1UaXAQ5KB-obe2MNI75G80Y9CctkoNMupCOk_bcQkpoyuECGzbbO7WlCXAZs99oV9xePXINKuN6UTFxYx-qj_eSfVGM

```
One request packets saved to ./iot_stuff/wireshark_data/one_request_to_fcm_google.pcapng

fcm = firebase cloud message

### After running a change colorTemp command from https://iot.google.com/console/
#### daemon console output
##### (illegal data range)
```
[(6950263.750)I gcm.c:551] Requesting command queue query.
[(6950263.750)I weave_http.c:98] Sending POST Request https://fcm.googleapis.com/fcm/ack
[(6950263.750)I weave.c:550] Fetching Command Queue
[(6950263.750)I weave_http.c:98] Sending GET Request https://www.googleapis.com/weave/v1/commands/queue?deviceId=fe438b6b-2303-7ea7-8f85-30751751726e&maxResults=3&reason=GcmConnected
[(6950265.123)I weave_state_machine.c:30] CommandQueueFetch: 1373ms
[(6950265.124)I weave.c:840] command_queue:
[(6950265.124)I weave.c:841] {
[(6950265.124)I weave.c:841]  "commands": [
[(6950265.124)I weave.c:841]   {
[(6950265.124)I weave.c:841]    "kind": "weave#command",
[(6950265.124)I weave.c:841]    "id": "fe438b6b-2303-7ea7-8f85-30751751726e8f9c3d3f-d433-a6da-231d-df3e57db9b4e",
[(6950265.124)I weave.c:841]    "deviceId": "fe438b6b-2303-7ea7-8f85-30751751726e",
[(6950265.124)I weave.c:841]    "creatorEmail": "zmz305@gmail.com",
[(6950265.124)I weave.c:841]    "component": "colorTemp",
[(6950265.124)I weave.c:841]    "name": "colorTemp.setConfig",
[(6950265.124)I weave.c:841]    "parameters": {
[(6950265.124)I weave.c:841]     "colorTemp": 1
[(6950265.124)I weave.c:841]    },
[(6950265.124)I weave.c:841]    "state": "queued",
[(6950265.124)I weave.c:841]    "creationTimeMs": "1486950263851",
[(6950265.124)I weave.c:841]    "expirationTimeMs": "1486950563851",
[(6950265.124)I weave.c:841]    "expirationTimeoutMs": "300000",
[(6950265.124)I weave.c:841]    "lastUpdateTimeMs": "1486950263851"
[(6950265.124)I weave.c:841]   }
[(6950265.124)I weave.c:841]  ]
[(6950265.124)I weave.c:841] }
[(6950265.124)W light_traits.c:333] ColorTemp: 1 out of specified bounds
[(6950265.124)I weave.c:537] Dispatch result: 0
[(6950265.124)I weave.c:434] Updating Command Status fe438b6b-2303-7ea7-8f85-30751751726e8f9c3d3f-d433-a6da-231d-df3e57db9b4e
[(6950265.124)I weave_http.c:98] Sending PATCH Request https://www.googleapis.com/weave/v1/commands/fe438b6b-2303-7ea7-8f85-30751751726e8f9c3d3f-d433-a6da-231d-df3e57db9b4e
[(6950265.252)I weave_state_machine.c:30] CommandPatch: 128ms

```
##### legal data range
```
[(6951003.553)I light_traits.c:35] turning light on
[(6951003.553)I light_traits.c:83] ColorTemp: 222
[(6951003.553)I light_traits.c:99] ColorMode: colorTemp
[(6951003.553)I weave.c:434] Updating Command Status fe438b6b-2303-7ea7-8f85-30751751726e8123e8b6-6c11-eadc-9acd-c666eb5f1c70
[(6951003.553)I weave_http.c:98] Sending PATCH Request https://www.googleapis.com/weave/v1/commands/fe438b6b-2303-7ea7-8f85-30751751726e8123e8b6-6c11-eadc-9acd-c666eb5f1c70
[(6951003.553)I weave_http.c:98] Sending POST Request https://fcm.googleapis.com/fcm/ack
[(6951003.668)I weave_state_machine.c:30] CommandPatch: 115ms

```

Wireshark capture at: ./iot_stuff/wireshark_data/after_cmd_from_web_iot_console

Since there is a patch request: ```Sending PATCH Request https://www.googleapis.com/weave/v1/commands/fe438b6b-2303-7ea7-8f85-30751751726e8123e8b6-6c11-eadc-9acd-c666eb5f1c70```,
PATCH request:
- <b>PATCH is neither safe nor idempotent</b>.
- source: http://restcookbook.com/HTTP%20Methods/patch/
- idempotent
  - From a RESTful service standpoint, for an operation (or service call) to be idempotent, clients can make that same call repeatedly while producing the same result. In other words, making multiple identical requests has the same effect as making a single request. Note that while idempotent operations produce the same result on the server (no side effects), the response itself may not be the same (e.g. a resource's state may change between requests).
  - source: http://www.restapitutorial.com/lessons/idempotency.html

### cppcheck
- ~/workspace/research > $ cppcheck --enable=all --force ./iot_stuff/
- ~/workspace/research > $ cppcheck --enable=all --force -i ./iot_stuff/libiota/cmake-build-debug/ ./iot_stuff/

### reproduce weave_client bug
- ./weave_client.sh config client_id 804117852738-dm73hhhdegg9odvs93gef5pt8g55e9ds.apps.googleusercontent.com
- ./weave_client.sh default_account zmz305@gmail.com
- then you cannot run anything with weave_client.sh

### weaviate
- go run weav...
- go get link.to.package to install missing libraries
- doc at: https://weaviate.github.io/
	- all not implemented...
- github at: https://github.com/weaviate
- official site: http://weaviate.com/
- 

### replay 
##### from source code and postman
- tried to modify source code (weave_http.c) to send consecutive PATCH request, end up with segfault
```
[(7607257.110)I weave_http.c:99] Sending PATCH Request https://www.googleapis.com/weave/v1/commands/fe438b6b-2303-7ea7-8f85-30751751726efd1a1e5d-53b7-6023-e4aa-a72b8f2bae78
[(7607257.110)I weave_http.c:105] Sending PATCH Request https://www.googleapis.com/weave/v1/commands/fe438b6b-2303-7ea7-8f85-30751751726efd1a1e5d-53b7-6023-e4aa-a72b8f2bae78
[(7607258.225)I weave_state_machine.c:30] CommandPatch: 115ms
[(7607258.308)I weave_state_machine.c:30] DeviceStateSync: 198ms
Segmentation fault (core dumped)
```
- PATCH data
```
[(7608864.236)I weave_http.c:105] data: {"id":"fe438b6b-2303-7ea7-8f85-30751751726e76de7a67-8662-74bb-5654-dc20842129fb","state":"done"}
```
- send PATCH data through POSTMAN returns error message (no Oauth2.0 specified in POSTMAN)
```
{
  "error": {
    "errors": [
      {
        "domain": "global",
        "reason": "required",
        "message": "Login Required",
        "locationType": "header",
        "location": "Authorization"
      }
    ],
    "code": 401,
    "message": "Login Required"
  }
}
```
<b>how to setup Oauth in postman?</b>

- directly add ```IOTA_LOG_INFO("data: %s", data->bytes);``` before return will cause segfault, may because of missing '\0' ?
	- Solved, data is NULL when request type is GET. Use local variable ```bytes``` instead.
- ```cloud->providers->httpc->send_request(cloud->providers->httpc,&request, NULL);``` send_request is a interface? where to find which function is actually called?


##### Tcpreplay http://tcpreplay.synfin.net/

