import json
import time
import threading
import requests
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from featureflags.evaluations.auth_target import Target
from featureflags.client import CfClient
from featureflags.util import log
from featureflags.config import with_base_url
from featureflags.config import with_events_url
import logging
from featureflags.client import CfClient
from featureflags.config import *
from featureflags.util import log
import os
import asyncio 
from featureflags import sse_client
from featureflags.sse_client import Event as E
import redis
from django.http import JsonResponse
from django.views.decorators.http import require_GET
#logging.basicConfig(level=logging.DEBUG)
#logger = logging.getLogger(__name__)

# Initialize a global variable to hold the current feature flag status
current_flag_status = False
# Initialize a threading Event to control the continuous polling
stop_event = threading.Event()
# API Key
api_key = os.getenv('FF_API_KEY', "")

# Flag Name
flagName = os.getenv('FF_FLAG_NAME', "test")

configURL = os.environ.get("FF_CONFIG_URL", "https://ffserver:8000/api/1.0")
eventsURL = os.environ.get("FF_CONFIG_URL", "https://ffserver:8001/api/1.0")


previousDict= {}


keys=["githubaction","featureflagvalue2"]


# Initialize a Redis client with the specified host and password
r = redis.Redis(host='redis-10120.c321.us-east-1-2.ec2.redns.redis-cloud.com', port=10120, db=0, password='vw7NTK5m3dsYKPg6E5eb1oKXKzCFPLU9',decode_responses=True)
# Ping the Redis server
try:
    response = r.ping()
    print("Redis server is running:", response)
except redis.ConnectionError:
    print("Unable to connect to Redis server.")


def onFeatureFlagValueChanged(featureFlagName, previousValue,currentValue):
    if previousValue !=currentValue:
     print(f"Feature flag value: {featureFlagName} has changed From  {previousValue} to {currentValue}")
     r.set(featureFlagName,int(currentValue))
     
@require_GET
def get_feature_flag_value(request):
    key = request.GET.get('key')
    if key:
        value = r.get(key)
        print("Feature flag value", value)
        if value:
            return JsonResponse({'value': value.decode('utf-8')})
        else:
            return JsonResponse({'error': 'No value found for the given key.'})
    else:
        return JsonResponse({'value': 'default_value'})
   
async def checkFFStatus():

    for key in keys:
     print(f"current value of {key} is{r.get({key})}")
   
    log.setLevel(logging.INFO)
    log.info("Harness SDK Getting Started")
    api_key = "14bf5a69-086f-4ef7-ad06-f7f0a73c4509"
    api_key2 = "6cf39c1b-4d5d-4fc2-9a84-e37c67a3d1f8"#api key for featureflagvalue2
  
    # Create a Feature Flag Client
    client = CfClient(api_key,Config(enable_stream=False,enable_analytics=False,pull_interval=1))
    client.wait_for_initialization()


   
    # Create a target (different targets can get different results based on
    target = Target(identifier='python_githubaction')
    
    # Loop forever reporting the state of the flag.  If there is an error
    # the default value will be returned
    while True:
        for eachKey in keys:   
          result = client.bool_variation(eachKey, target, False)
          if eachKey not in previousDict.keys():
              previousDict[eachKey] = result
          onFeatureFlagValueChanged(eachKey,previousDict[eachKey],result)
          previousDict[eachKey] = result
          

       #print("Checking")
        
        await asyncio.sleep(1)
#threading.Thread(target=run_check_ff_status).start()
asyncio.run(checkFFStatus())