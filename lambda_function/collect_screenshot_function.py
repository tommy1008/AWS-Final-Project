import boto3
import json
import os
import datetime
import  requests
def lambda_handler(event,context):
    # Get the service client
    s3 = boto3.client('s3')
    apigateway = boto3.client('apigateway')

    apiKey = apigateway.get_api_key(apiKey=event["requestContext"]["identity"]["apiKeyId"],includeValue=True)
    now = datetime.datetime.now()
    filename = now.strftime("screenshot_%M_%S.json")
    partition = now.strftime("year=%Y/month=%m/day=%d/hour=%H")
    fields = {"acl": "public-read"}

    conditions = [
        {"acl": "public-read"},
        ["content-length-range", 30, 1000]
    ]

    post = s3.generate_presigned_post(
        Bucket=os.environ['StudentLabDataBucket'],
        Key = f"screenshot_stream/{partition}/id={apiKey['name']}/{filename}",
        Fields=fields,
        Conditions=conditions

    )

    files = {"file": "file_content"}
    response = requests.post(post["url"], data=post["fields"], files=files)
    return response