import json
import boto3

sns = boto3.client('sns')

TOPIC_ARN = 'YOUR_TOPIC_ARN'

def lambda_handler(event, context):

    for record in event['Records']:

        new_image = record['dynamodb']['NewImage']

        name = new_image['name']['S']
        location = new_image['location']['S']
        emergency = new_image['emergency']['S']

        message = f"""
🚨 AUTOMATED DISASTER ALERT 🚨

Citizen Name: {name}

Location: {location}

Emergency Type: {emergency}

Immediate rescue required.
"""

        sns.publish(
            TopicArn=TOPIC_ARN,
            Message=message,
            Subject='Automatic Emergency Alert'
        )

    return {
        'statusCode': 200,
        'body': json.dumps('Alert Sent')
    }