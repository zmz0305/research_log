### Continue duplicate PATCH request test on libiota
- segfault is not happending in the second ```cloud->providers->httpc->send_request(cloud->providers->httpc,&request, NULL);```, but after send_()
- which means the duplicate PATCH request is sent out already :)
- that's how it looks like when duplicate PATCH are sent to server![Alt text](./patch.png)

### tcpreplay continued
```
~/workspace/research/iot_stuff/libiota > $ (master) sudo tcpreplay -intf1=wlp3s0 ../wireshark_data/one_request_to_fcm_google.pcapng 

Fatal Error in tcpreplay.c:post_args() line 455:
 Invalid interface name/alias: ntf1=wlp3s0
~/workspace/research/iot_stuff/libiota > $ (master) sudo tcpreplay -intf1=lo ../wireshark_data/one_request_to_fcm_google.pcapng 

Fatal Error in tcpreplay.c:post_args() line 455:
 Invalid interface name/alias: ntf1=lo```