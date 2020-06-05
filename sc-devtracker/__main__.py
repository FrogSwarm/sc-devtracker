from urllib.parse import urlparse
import locale, sched, time, logging
import configparser
from . import mercury

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

config = configparser.ConfigParser()
config.read('config.ini')

FEED_PARSE_DELAY = int(config['general']['fetch_delay'])
locale.setlocale(locale.LC_TIME, config['general']['locale'] + ".UTF-8")

mercury = mercury.Mercury(config)

def star_runner(sc): 
    """ Check for new RSS Post every FEED_PARSE_DELAY
    and send the last new entry to the set discord webhook
    """
    last_post = mercury._check_last_rss_post()
    if last_post:
        logger.info("Sending new entry to Discord: " + last_post.title + " [" + urlparse(last_post.link).hostname + "]")
        discord_embed = mercury._generate_discord_json(last_post)
        mercury._send_json_to_webhook(discord_embed)
    s.enter(FEED_PARSE_DELAY, 1, star_runner, (sc,))

s = sched.scheduler(time.time, time.sleep)
s.enter(0, 1, star_runner, (s,))
s.run()