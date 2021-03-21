import json
import tweet_api


def run(event, context):
    message = 'Hello, world!'
    tweet_api.post_message(message)
    return {
        'statusCode': 200,
        'body': json.dumps(message)
    }


if __name__ == '__main__':
    run(None, None)
