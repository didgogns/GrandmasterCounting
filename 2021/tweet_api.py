import tweepy
import boto3
import os
from base64 import b64decode

import Util


def decrypt(encrypted):
    decrypted = boto3.client('kms').decrypt(
        CiphertextBlob=b64decode(encrypted),
        EncryptionContext={'LambdaFunctionName': os.environ['AWS_LAMBDA_FUNCTION_NAME']}
    )['Plaintext'].decode('utf-8')
    return decrypted


def identity_function(encrypted):
    return encrypted


def get_api():
    decrypt_func = identity_function
    if Util.is_aws():
        decrypt_func = decrypt
    auth = tweepy.OAuthHandler(decrypt_func(os.environ['API_KEY']), decrypt_func(os.environ['API_SECRET_KEY']))
    auth.set_access_token(decrypt_func(os.environ['ACCESS_TOKEN']), decrypt_func(os.environ['ACCESS_TOKEN_SECRET']))

    api = tweepy.API(auth)
    return api


def post_message(message):
    api = get_api()
    api.update_status(message)


def post_picture(picture_path):
    api = get_api()
    api.update_with_media(picture_path)


def post_picture_and_message(picture_path, message):
    api = get_api()
    result = api.media_upload(picture_path)
    api.update_status(status=message, media_ids=[result.media_id_string])


if __name__ == '__main__':
    post_picture('C:\\Users\\USER-PC\\Pictures\\The_Coin_full.jpg')
