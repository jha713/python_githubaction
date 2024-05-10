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

# Initialize a global variable to hold the current feature flag status
current_flag_status = False
# Initialize a threading Event to control the continuous polling
stop_event = threading.Event()

# Your Django view that will receive events from Harness.io
@csrf_exempt
@require_POST
def event_receiver(request):
    global current_flag_status
    # Extract data from the request
    data = request.POST
    flag_status = data.get('flag_status')

    # Perform any necessary processing with the flag status
    # For example, you could update a database record or trigger some action based on the flag status

    # Return a JSON response indicating successful processing
    return JsonResponse({'message': 'Event received and processed successfully.'})

# Function to continuously poll Harness.io for feature flag updates
def poll_harness():
    global current_flag_status
    log.debug("Starting continuous polling")
    api_key = "14bf5a69-086f-4ef7-ad06-f7f0a73c4509"
    client = CfClient(api_key,
                      with_base_url("https://config.ff.harness.io/api/1.0"),
                      with_events_url("https://events.ff.harness.io/api/1.0"))
    target = Target(identifier='python_githubaction', name="target1")
    while not stop_event.is_set():
        result = client.bool_variation('githubaction', target, False)
        log.debug("Result %s", result)
        # Convert the result to a boolean before comparison
        result = bool(result)
        # If the flag status has changed, send an event to the Django application
        if result != current_flag_status:
            current_flag_status = result
            # Send an HTTP POST request to the event_receiver endpoint with the updated status
            requests.post('http://127.0.0.1:8002/event_receiver/', data={'flag_status': str(result)})
        time.sleep(10)  # Polling interval

# Your main entry point
def main():
    log.debug("Starting example")
    # Start the continuous polling in a separate thread
    polling_thread = threading.Thread(target=poll_harness)
    polling_thread.start()

# Your Django view to stop the continuous polling
def stop_continuous_polling(request):
    global stop_event
    log.debug("Stopping continuous polling")
    stop_event.set()
    return HttpResponse("Continuous polling stopped.", status=200)
