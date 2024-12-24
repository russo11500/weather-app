# weather-app

## weatherapi.com API key
In order to get API key for https://www.weatherapi.com/ go by this link and finish a quick sign up.
After that you will be able to get the api key and set it to WEATHER_API_KEY env variable for weather api usage.

## Manual steps to run the app locally but with usage of AWS

All the commands executed from the root directory of the repository.
1. create new python venv 
```
python -m venv .venv
```
2. activate venv 
```
.venv/script/activate
```
3. install dev requirements 
```
pip install -r requirements.dev.txt
```
4. make sure you have valid AWS creds to you account in "Users/your user/.aws" folder on you PC.
5. From AWS console create S3 bucket for cache and populate its name to the S3_BUCKET_NAME env variable.
6. From AWS console create SQS standard queue with name cache-expiring and Delivery delay of 5 minutes. Retention period can be set to 10 minutes. We don't need to store those messages for a long time.
7. From AWS console create Lambda function with name expire-cache and Runtime Python 3.13. Deploy the code provided in the lambdas/expire_cache/lambda_function.py file.
8. Return to SQS and Create policy in the queue to allow reading and deletion of messages from lambda and sending messages from s3.
```
{
  "Version": "2012-10-17",
  "Id": "Policy1735030583635",
  "Statement": [
    {
      "Sid": "Stmt1735030582462",
      "Effect": "Allow",
      "Principal": {
        "Service": "s3.amazonaws.com"
      },
      "Action": "sqs:SendMessage",
      "Resource": "<queue arn>"
    }
  ]
}
```

9. Return to Lambda and set permissions for sqs. Go to Configuration -> Permission -> Edit -> chose "Create a new role from AWS policy templates" -> enter Role name ->  chose "Amazon SQS poller permissions" in Policy templates -> Save
10. Create trigger on our SQS queue (it will expire the cache). It can be done from lambda page Configuration -> Triggers.
11. Return to S3 and create event in our bucket to send message to the cache-expiring queue on object creation. On the bucket page open "Properties" tab and scroll to "Event notifications". Click create event and provide "Event name", check "All objects create events" checkbox and finally scroll down and chose Destination "SQS queue" and chose previously created queue cache-expiring.
12. Create policy in the bucket to allow deletion of objects from trigger
```
{
    "Version": "2012-10-17",
    "Id": "Policy1735032755321",
    "Statement": [
        {
            "Sid": "Stmt1735032753321",
            "Effect": "Allow",
            "Principal": {
                "AWS": "ARN of Lambda SQS Role that we created in step 9. Role can be found in the IAM service -> Roles -> our role name "
            },
            "Action": "s3:DeleteObject",
            "Resource": "{ARN of the bucket}/*"
        }
    ]
}
```
13. Create dynamoDB table weather_events with 'city' (string) as partition key and 'timestamp' (string) as sort key. Provide table name in WEATHER_TABLE_NAME env variable. In this task we don't read from db, only write, but I assume it's a possible use case that we will want to read from it in future so I decided to create composite primary key that consists from city and timestamp.
15. Populate last env variable AWS_REGION with region that you used for AWS services configuration.
14. Run fastApi server 
```
fastapi run src\main.py
```
15. Test the /weather endpoint with different values for "city" query parameter.
