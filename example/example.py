"""
JSON-log-formatter.
"""
import logging.config
import yaml
from math import sqrt

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file.read())
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)

nested = {
    'foo': 1,
    'bar': 'bar',
}

print('Print')
logger.debug('Dbg mes', extra={'extra_code': 'De', 'nested': nested})
logger.info('Inf mes', extra={'extra_code': 'In'})
logger.warning('Wrng mes', extra={'extra_code': 'Wa'})
logger.critical('Crtcl mes', extra={'extra_code': 'Cr'})

# Handled exception
try:
    1/0
except Exception:
    logger.error('Handled exception', extra={'extra_code': 'Ex'}, exc_info=True)

# Unhandled exception
sqrt(-1)  # STDERR
