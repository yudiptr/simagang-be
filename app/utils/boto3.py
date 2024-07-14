import boto3
from app.config import Config


s3 = boto3.client(
    's3',
    aws_access_key_id = Config.AWS_ACCESS_KEY,
    aws_secret_access_key = Config.AWS_SECRET_KEY
)

bucket_name = str(Config.AWS_BUCKET_NAME)