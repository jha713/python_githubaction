# cf_client_configuration.py

import logging
import requests
from cfclient import CfClient

logger = logging.getLogger(__name__)

class CfClientConfiguration:
    def __init__(self, api_key):
        self.api_key = '14bf5a69-086f-4ef7-ad06-f7f0a73c4509'
        self.connector_config = {
            "configUrl": "https://config.ff.harness.io/api/1.0",
            "eventUrl": "https://events.ff.harness.io/api/1.0"
        }
        self.options = {
            "pollIntervalInSeconds": 60,
            "streamEnabled": True,
            "analyticsEnabled": True
        }
        self.cf_client = self.initialize_cf_client()

    def initialize_cf_client(self):
        try:
            cf_client = CfClient(self.api_key, self.connector_config, self.options)
            cf_client.wait_for_initialization()
            cf_client.on("ready", self.on_ready)
            cf_client.on("changed", self.on_changed)
            return cf_client
        except Exception as e:
            logger.error(f"Error initializing CfClient: {e}")

    def on_ready(self, _):
        logger.info("Harness client initialized.")

    def on_changed(self, flag):
        try:
            value = self.cf_client.bool_variation(flag, None, False)
            logger.info(f"{flag}: {'Enabled' if value else 'Disabled'}")
            logger.info("---> Triggering GitHub Actions workflow <---")
            self.trigger_github_action_workflow()
        except Exception as e:
            logger.error(f"Error handling changed event: {e}")

    def trigger_github_action_workflow(self):
        # Add your logic to trigger GitHub Actions workflow here
        pass

def cf_client(api_key):
    return CfClientConfiguration(api_key).cf_client


# import logging
# import requests
# import json
# from django.conf import settings
# from django.http import StreamingHttpResponse

# logger = logging.getLogger(__name__)

# class CfClientConfiguration:
#     def __init__(self):
#         self.api_key = settings.FEATURE_FLAG_API_KEY
#         self.config_url = "https://config.ff.harness.io/api/1.0"
#         self.event_url = "https://events.ff.harness.io/api/1.0"
#         self.poll_interval = 60
#         self.stream_enabled = True
#         self.analytics_enabled = True
#         self.flag_names = ["githubaction"]  # List of feature flag names

#     def get_feature_flag_status(self):
#         try:
#             for flag_name in self.flag_names:
#                 response = self.fetch_feature_flag(flag_name)
#                 if response.status_code == 200:
#                     flag_status = response.json().get("value")
#                     logger.info(f"Feature flag '{flag_name}' status: {'Enabled' if flag_status else 'Disabled'}")
#                     # Add logic to trigger GitHub actions workflow based on flag status
#                     self.trigger_github_actions_workflow(flag_status)
#                 else:
#                     logger.error(f"Failed to fetch feature flag '{flag_name}': {response.text}")
#         except Exception as e:
#             logger.error(f"Error occurred while fetching feature flag status: {str(e)}")

#     def fetch_feature_flag(self, flag_name):
#         headers = {"Authorization": f"Bearer {self.api_key}"}
#         params = {"pollInterval": self.poll_interval, "streamEnabled": self.stream_enabled, "analyticsEnabled": self.analytics_enabled}
#         url = f"{self.config_url}/flags/{flag_name}"
#         return requests.get(url, headers=headers, params=params)

#     def trigger_github_actions_workflow(self, flag_status):
#         # Add logic to trigger GitHub actions workflow based on flag status
#         pass

#     def sse_event_stream(self):
#         headers = {"Authorization": f"Bearer {self.api_key}"}
#         url = f"{self.event_url}/flags/stream"
#         response = requests.get(url, headers=headers, stream=True)

#         for event in response.iter_lines():
#             if event:
#                 try:
#                     flag_event = json.loads(event)
#                     flag_name = flag_event.get("flagName")
#                     flag_status = flag_event.get("flagStatus")
#                     logger.info(f"Received SSE for flag '{flag_name}' with status: {'Enabled' if flag_status else 'Disabled'}")
#                     # Update feature flag status or trigger actions based on SSE event
#                     self.update_flag_status(flag_name, flag_status)
#                 except Exception as e:
#                     logger.error(f"Error processing SSE event: {str(e)}")

#     def update_flag_status(self, flag_name, flag_status):
#         # Update feature flag status or trigger actions based on SSE event
#         pass


# # Instantiate CfClientConfiguration and get feature flag status
# cf_client = CfClientConfiguration()
# cf_client.get_feature_flag_status()
