### Continue duplicate PATCH request test on libiota
- segfault is not happending in the second ```cloud->providers->httpc->send_request(cloud->providers->httpc,&request, NULL);```, but after send_()
- which means the duplicate PATCH request is sent out already :)
- that's how it looks like when duplicate PATCH are sent to server![Alt text](./patch.png)
- does not see any actually negative impact towards the cloud server.
- maybe one PATCH request is just one entry of log data.


### tcpreplay continued

```
~/workspace/research/iot_stuff/libiota > $ (master) sudo tcpreplay -intf1=wlp3s0 ../wireshark_data/one_request_to_fcm_google.pcapng 

Fatal Error in tcpreplay.c:post_args() line 455:
 Invalid interface name/alias: ntf1=wlp3s0
~/workspace/research/iot_stuff/libiota > $ (master) sudo tcpreplay -intf1=lo ../wireshark_data/one_request_to_fcm_google.pcapng 

Fatal Error in tcpreplay.c:post_args() line 455:
 Invalid interface name/alias: ntf1=lo
```

correction: it's -i wlp3s0 or --ntf1=wlp3s0

##### Results:
-  Cannot see any impact towards anything.
-  Didn't see any response in any way.
-  GCM token expires every few minutes (very short), may need to use re-captured packets every period of time to apply actual effect.

Try tcpliveplay: http://tcpreplay.synfin.net/wiki/tcpliveplay
 