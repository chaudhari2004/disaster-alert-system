import boto3

sns = boto3.client(
    'sns',
    region_name='ap-south-1'
)

TOPIC_ARN = 'arn:aws:sns:ap-south-1:645920624235:DisasterAlerts'

def send_alert(message):

    response = sns.publish(
        TopicArn=TOPIC_ARN,
        Message=message,
        Subject='Disaster Emergency Alert'
    )

    return response