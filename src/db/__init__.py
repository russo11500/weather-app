from src.db.dynamo_db import DynamoDBClient


class DB:    
    def __new__(cls, db_type):
        if db_type == 'DynamoDB':
            return DynamoDBClient()
        else:
            raise NotImplementedError('Unsupported db type')



