import tweepy
import logging
from usda import UsdaClient
import os

client = UsdaClient('AIpZZveymTa6bWWtZsicN2wMDw1kXiFxDwYfcP4A')


logger = logging.getLogger()

CONSUMER_KEY = "scvrWYKtJYCHFLfvBQNgsztgk"
CONSUMER_SECRET = "7BGO75s7L78krMYxjqAfuP2l9dpdj7CVclqtry3OTD9DaUUXgj"
ACCESS_TOKEN = "1260586659088867328-GCHRNLu9orOqavGZyYcv8ppjYRAWmo"
ACCESS_TOKEN_SECRET = "dQxWaADJOiWW3vDJxwgrT323WVtkE0BdQvCdbLmWSDStW"


def create_api():
    # auth = tweepy.OAuthHandler("CONSUMER_KEY", "CONSUMER_SECRET")
    auth = tweepy.OAuthHandler(CONSUMER_KEY,
                               CONSUMER_SECRET)
    # auth.set_access_token("ACCESS_TOKEN", "ACCESS_TOKEN_SECRET")
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # Creating API object
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api

