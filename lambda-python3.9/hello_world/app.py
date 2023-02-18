import json
import boto3
import botocore

from datetime import datetime, timezone

def lambda_handler(event, context):
   
    client = boto3.client('dynamodb')
    
    ip = event['requestContext']['identity']['sourceIp']
    client.put_item(TableName='mh-resume', Item={'pk':{'S':'visitor'},'sk':{'S': ip}, 'date':{'S': datetime.utcnow().isoformat()}})
    try:
        response = client.update_item(TableName='mh-resume',
            Key={'pk': {'S':'visitor-stats'}, 'sk':{'S':'total-count'}},
            UpdateExpression="set stat_value = stat_value + :i",
            ExpressionAttributeValues={':i': {'N':'1'}},         
            ReturnValues='UPDATED_NEW')        
        return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "https://www.mh-resume.net",
            "Access-Control-Allow-Methods": "OPTIONS,GET"
        },
        "body": json.dumps({
            "visitorCount": response['Attributes']['stat_value']["N"],
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
        }
    except botocore.exceptions.ClientError as err:
        print(err)      
        return {
            'statusCode': 200,
             "headers": {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "https://www.mh-resume.net",
            "Access-Control-Allow-Methods": "OPTIONS,GET"
        },
            'visitorCount':0
        }

def test_fake_business_logic(foo):
    return len(foo)%2==0