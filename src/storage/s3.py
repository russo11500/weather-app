import json


import aioboto3
from botocore.exceptions import ClientError

from src.logger import logger
from src.config import Config as config
from src.storage.storage_abc import StorageInterface


class S3Client(StorageInterface):
    async def get_file(self, city):
        session = aioboto3.Session()
        async with session.client('s3', region_name=config.AWS_REGION) as s3:
            try:
                logger.info('Receiving file from S3')
                response = await s3.list_objects_v2(
                    Prefix=city,
                    Bucket=config.S3_BUCKET_NAME,
                    MaxKeys=1
                )

            except ClientError as e:
                logger.error(e)
                return
            if 'Contents' not in response:
                logger.info('No files found in the bucket')
                return 

            logger.info('Found file in the bucket')
            latest_file = response['Contents'][0]

            file_key = latest_file['Key']
            obj = await s3.get_object(Bucket=config.S3_BUCKET_NAME, Key=file_key)
            file_content = await obj['Body'].read()

            return json.loads(file_content.decode('utf-8'))

    async def upload(self, file_name, file_data):
        session = aioboto3.Session()
        async with session.client('s3', region_name=config.AWS_REGION) as s3:
            try:
                logger.info('Uploading file to S3')
                json_file = json.dumps(file_data).encode('UTF-8')
                await s3.put_object(
                    Body=json_file, 
                    Bucket=config.S3_BUCKET_NAME, 
                    Key=file_name
                )
                logger.info('Uploaded file to S3')
                return f's3://{config.S3_BUCKET_NAME}/{file_name}'
            except ClientError as e:
                logger.error(e)
                return 
            