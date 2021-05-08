import boto3
from botocore.exceptions import ClientError

s3_client = boto3.client('s3')
BUCKET_NAME = 'hearthstonegrandmasterbucket'


def from_file(file_name):
    try:
        data = s3_client.get_object(Bucket=BUCKET_NAME, Key=file_name)
        return data['Body'].read()
    except ClientError as ex:
        if ex.response['Error']['Code'] == 'NoSuchKey':
            return None
        else:
            raise


def to_file(data, file_name):
    s3_client.put_object(Body=data, Bucket=BUCKET_NAME, Key=file_name)
