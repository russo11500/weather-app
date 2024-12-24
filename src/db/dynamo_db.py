import traceback

import aioboto3
from botocore.exceptions import ClientError

from src.db.db_abc import DBInterface
from src.config import Config as config
from src.logger import logger


class DynamoDBClient(DBInterface):
    async def save_data(self, city, timestamp, file_url):
        session = aioboto3.Session()
        async with session.client('dynamodb', region_name=config.AWS_REGION) as client:
            try:
                item = {
                        'city': {'S': city}, 
                        'timestamp': {'S': str(timestamp)},
                        'file_url': {'S': file_url}
                }
                logger.info(f'Putting item into the table, item = {item}')
                await client.put_item(
                    TableName=config.WEATHER_TABLE_NAME,
                    Item=item
                )
                logger.info('Put succesfully')
            except ClientError:
                logger.error(f'ERROR!!!\n {traceback.format_exc()}')
