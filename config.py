import tweepy
import logging
from usda import UsdaClient
import os

client = UsdaClient('AIpZZveymTa6bWWtZsicN2wMDw1kXiFxDwYfcP4A')
client = UsdaClient('XXXXXXXXXYYYYYYYYYhck2fenXXXXXXXXXXXXXXX')


logger = logging.getLogger()

CONSUMER_KEY = "xxxxxxxxxxxxXXXXXXXxxxxxx"
CONSUMER_SECRET = "######******xxxxxxxxXXXXXXXXXXYYYYYYYYYYYYYYYyyyyy"
ACCESS_TOKEN = "26523572864783693267**************XXXXXXXXXXXX"
ACCESS_TOKEN_SECRET = "xxxxxxx2635614x738798XXXXXXXXXXXXXXXyyyyyyyyy"


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

