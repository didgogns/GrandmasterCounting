import json
import tweepy


def get_api():
    with open('auth.json') as json_file:
        auth_json = json.load(json_file)

    auth = tweepy.OAuthHandler(auth_json['API_KEY'], auth_json['API_SECRET_KEY'])
    auth.set_access_token(auth_json['ACCESS_TOKEN'], auth_json['ACCESS_TOKEN_SECRET'])

    api = tweepy.API(auth)
    return api


def post_picture(picture_path):
    api = get_api()
    api.update_with_media(picture_path)


if __name__ == '__main__':
    post_picture('C:\\Users\\USER-PC\\Pictures\\The_Coin_full.jpg')
