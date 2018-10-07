import boto3
import json
import os
import datetime
import  requests

print('Loading function')
# Get the service client
s3 = boto3.client('s3')
apigateway = boto3.client('apigateway')

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def lambda_handler(event,context):
    apiKey = apigateway.get_api_key(apiKey=event["requestContext"]["identity"]["apiKeyId"],includeValue=True)
    
    now = datetime.datetime.now()
    partition = now.strftime("year=%Y/month=%m/day=%d/hour=%H")

    presigned_url = s3.generate_presigned_url(
        ClientMethod='put_object',
        Params={
            'Bucket': os.environ['StudentLabDataBucket'],
            'Key': f"screenshot_stream/{partition}/id={apiKey['name']}"
        }
    )
    
    return respond(None, presigned_url)

#def lambda_handler(event,context):
#    apiKey = apigateway.get_api_key(apiKey=event["requestContext"]["identity"]["apiKeyId"],includeValue=True)
   
#    now = datetime.datetime.now()
#    partition = now.strftime("year=%Y/month=%m/day=%d/hour=%H")
#    filename = now.strftime("screenshot_%M_%S.jpg")
     
#    img = join(body).decode('utf8')
     
#    s3.put_object(Bucket=os.environ['StudentLabDataBucket'],
#            Key = f"screenshot_stream/{partition}/id={apiKey['name']}/{filename}",
#            Body = open(img, 'wb'),
#            ContentType="application/json"
#          )

#    return respond(None, apiKey["name"] + f" srceenshot events.")