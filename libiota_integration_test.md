### Checkout the libiota library
- git clone https://weave.googlesource.com/weave/libiota

### How to run integration test
- Checkout the autotest folder from ```https://chromium.googlesource.com/chromiumos/third_party/autotest/+/master```
- Put the folder at the same layer as the libiota folder
- Run ```make lib```, ```make test```, then ```make integration_tests```
- In libiota folder, go to ```./out/autotest/site_utils```, run ```sudo python test_iota.py --help``` to see the instructions.
- Example command ```sudo python test_iota.py --binary_path /home/zmz/workspace/research/iot_stuff/libiota/out/host/examples/hvac_controller/hvac_controller -b host --instance_name hvac_controller --weave_client /home/zmz/workspace/research/iot_stuff/weave_client-0.1.16/weave_companion_client.sh wipeout```, replace paths as needed.
- Search in libiota source folder for test_suits. Avoid running test suits from the autotest folder cloned from chromium repo.
