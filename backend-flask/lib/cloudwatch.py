import watchtower
import logging
from flask import request

# Configure logging for CLOUDWATCH
LOGGER = logging.getLogger(__name__)  
LOGGER.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
# cw_handler = watchtower.CloudWatchLogHandler(log_group='cruddur')
LOGGER.addHandler(console_handler)
# LOGGER.addHandler(cw_handler)
LOGGER.info("Test Log")

def init_cloudwatch(response):
  timestamp = strftime('[%Y-%b-%d %H:%M]')
  LOGGER.error('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
  return response