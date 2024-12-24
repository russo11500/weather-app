import json
import boto3

def lambda_handler(event, _):

    for record in event['Records']:
        body = json.loads(record['body'])
        for rec in body['Records']:

            bucketName = rec['s3']['bucket']['name']
            objectKey = rec['s3']['object']['key']
            s3 = boto3.resource('s3')
            obj = s3.Object(bucketName, objectKey)
            obj.delete()

    return {
        'statusCode': 200,
        'body': json.dumps('Deleted')
    }
