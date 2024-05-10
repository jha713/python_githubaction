# cf_client_configuration.py
import logging
from featureflags.client import CfClient
from featureflags.config import Config

logger = logging.getLogger(__name__)

class CfClientConfiguration:
    def __init__(self, api_key):
        self.api_key = api_key
        self.config = self.initialize_config()
        self.cf_client = self.initialize_cf_client()

    def initialize_config(self):
        try:
            config = Config()
            config.base_url = "https://config.ff.harness.io/api/1.0"
            config.events_url = "https://events.ff.harness.io/api/1.0"
            config.stream_enabled = True
            config.analytics_enabled = True
            config.poll_interval = 60
            return config
        except Exception as e:
            logger.error(f"Error initializing Config: {e}")

    def initialize_cf_client(self):
        try:
            client = CfClient(self.api_key, self.config)
            client.wait_for_initialization()
            return client
        except Exception as e:
            logger.error(f"Error initializing CfClient: {e}")
