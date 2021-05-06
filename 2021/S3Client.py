import boto3

s3_client = boto3.client('s3')
BUCKET_NAME = 'hearthstonegrandmasterbucket'


def from_file(file_name):
    data = s3_client.get_object(Bucket=BUCKET_NAME, Key=file_name)
    return data['Body'].read()


def to_file(data, file_name):
    s3_client.put_object(Body=data, Bucket=BUCKET_NAME, Key=file_name)
