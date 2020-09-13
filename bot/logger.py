from datetime import datetime
import json
import logging
from bot.config import LOG_PATH, LOG_LEVEL, DATA

str_date = datetime.now().isoformat(timespec='hours')
logging.basicConfig(
    filename=f'{LOG_PATH}/{str_date}.log',
    level=LOG_LEVEL,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
)
logger = logging.getLogger(__name__)
is_debug = logger.getEffectiveLevel() == 10  # True if logging level = logging.DEBUG

msg = f"Current configuration bot/conf.json:\n" \
      f"{json.dumps(DATA, sort_keys=False, indent=4, separators=(',', ': '))}"
logger.debug(msg)

if is_debug:
    print(msg)
