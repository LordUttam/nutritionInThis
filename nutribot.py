import tweepy
import logging
from config import create_api
import time
from usda import UsdaClient
from usda import base

client = UsdaClient('AIpZZveymTa6bWWtZsicN2wMDw1kXiFxDwYfcP4A')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

FILE_NAME = 'last_seen_id.txt'


def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    data = f_read.readlines()
    data = [int(i) for i in data]
    last_seen_id = max(data)
    f_read.close()
    return last_seen_id


def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'a')
    f_write.write('\n')
    f_write.write(str(last_seen_id))
    f_write.close()
    return


def check_mentions(api, last_seen_id):
    logger.info("Retrieving mentions")
    new_since_id = last_seen_id

    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=last_seen_id).items():
        new_since_id = max(tweet.id, last_seen_id)

        if tweet.in_reply_to_status_id is not None:
            continue
        try:
            food_in_tweet = tweet.text
            print(food_in_tweet)
            food_in_tweet = food_in_tweet.rstrip("@nutritionInThis")
            print("searching for", food_in_tweet)

            foods_search = client.search_foods(food_in_tweet.lower(), 1)
            food = next(foods_search)
            logger.info(f"Answering to {tweet.user.screen_name} for query {food_in_tweet}")
            print(food)
            report = client.get_food_report(food.id)
            status = f'@{tweet.user.screen_name} {food} \n'
            newline = '\n'
            for nutrient in report.nutrients:
                if nutrient.name in ['Energy', 'Total lipid (fat)', 'Carbohydrate, by difference',
                                     'Fiber, total dietary', 'Sugars, total', 'Sodium',
                                     'Protein', 'Cholestrol', 'Vitamin A', 'Vitamin B-6',
                                     'Vitamin C', 'Vitamin K', 'Vitamin B-12', 'Iron, Fe']:
                    status_line = f"{nutrient.name} {nutrient.value} {nutrient.unit} {newline}"
                    status += status_line

            if not tweet.user.following:
                tweet.user.follow()
            api.update_status(
                status=status,
                in_reply_to_status_id=tweet.id,
            )
            print(tweet.id)

        except base.DataGovInvalidApiKeyError:
            print("Invalid usda API key.")
        except base.DataGovApiRateExceededError:
            print("Too many requests! Limit Reached.")
        except ValueError:
            status=f"@{tweet.user.screen_name} Sorry, that's not in the database. Try something else."
            api.update_status(
                status=status,
                in_reply_to_status_id=tweet.id,
            )
            logger.info(f"Answering to {tweet.user.screen_name} that {food_in_tweet} is not in database")


    return new_since_id


def main():
    api = create_api()
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    while True:
        last_seen_id = check_mentions(api, last_seen_id)

        f_read = open(FILE_NAME, 'r')
        data = f_read.readlines()
        data = [int(i) for i in data]

        if last_seen_id not in data:
            store_last_seen_id(last_seen_id, FILE_NAME)

        logger.info("Waiting...")
        time.sleep(60)


if __name__ == "__main__":
    main()

