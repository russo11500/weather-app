import os

class Config:
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    WEATHER_API_URL = os.getenv('WEATHER_API_URL', 'https://api.weatherapi.com/v1')
    WEATHER_API_ENDPOINT = os.getenv('WEATHER_API_ENDPOINT', '/current.json')
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', '132464cd0d4d41a2bc3104703242312')

    AWS_REGION = os.getenv('AWS_REGION', 'eu-north-1')
    STORAGE_TYPE = os.getenv('STORAGE_TYPE', 'S3')
    S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'weather-data00')
    DB_TYPE = os.getenv('DB_TYPE', 'DynamoDB')
    WEATHER_TABLE_NAME = os.getenv('WEATHER_TABLE_NAME', 'weather_events1')
    
