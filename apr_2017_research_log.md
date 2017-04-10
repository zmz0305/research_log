
## Problems summery
-   ?

#### Vimuth's code
- Device registration use different mechanism now, how to update to the new way?
- Where to get the discovery.json file
  - Google discovery
    - Tried various GET urls in examples, got 404
  - try to hack weave_companion_client
  - account_companion.py:      discovery_url = ('https://{api}.googleapis.com/$discovery/rest?'
  - use https://weavecompanion.googleapis.com/$discovery/rest to get newest discovery file for weave. (The service is even no longer called weave but called weavecompanion)
    - it is so drastically different from the old one in Vimuth's code that makes the code no longer work
- Try to crack Vimuth's code to work with new discovery.json, or we should called api specification file
  - need to learn how google-api-client library works
  - look into resources_companion.py in weave_companion_client
    - it is a wrapper?
    - not helpful
  - look into device_companion.py in weave_companion_client
    - line 92
  - look into weave_companion_client.py
  - change to         ```ticket = api_client.devices().provision(body="").execute()```
  - using .json from weave_companion_client

### Google discovery api
- "resources"
- "schema"
- example "shorturl" apis: https://www.googleapis.com/discovery/v1/apis/urlshortener/v1/rest
- https://developers.google.com/discovery/v1/using#discovery-doc-resources

### Findings in https://weavecompanion.googleapis.com/$discovery/rest
-
