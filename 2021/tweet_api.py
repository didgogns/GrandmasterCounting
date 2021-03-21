import os
import tweepy


def get_api():
    auth = tweepy.OAuthHandler(os.environ['API_KEY'], os.environ['API_SECRET_KEY'])
    auth.set_access_token(os.environ['ACCESS_TOKEN'], os.environ['ACCESS_TOKEN_SECRET'])

    api = tweepy.API(auth)
    return api


def post_message(message):
    api = get_api()
    api.update_status(message)


def post_picture(picture_path):
    api = get_api()
    api.update_with_media(picture_path)


if __name__ == '__main__':
    post_picture('C:\\Users\\USER-PC\\Pictures\\The_Coin_full.jpg')
