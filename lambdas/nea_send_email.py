import boto3


def lambda_handler(event, context):
    message = event['message']
    if not message:
        return {'code': 0, 'message': 'No new posts to send this week'}

    toEmail = event['email_to']
    fromEmail = event['email_from']
    replyTo = fromEmail
    subject = 'Weekly Digest'

    client = boto3.client('ses')
    response = client.send_email(
        Source=fromEmail,
        Destination={
            'ToAddresses': [toEmail],
        },
        Message={
            'Subject': {
                'Data': subject,
                'Charset': 'utf8'
            },
            'Body': {
                'Html': {
                    'Data': message,
                    'Charset': 'utf8'
                }
            }
        },
        ReplyToAddresses=[
            replyTo
        ]
    )

    return {'code': 0, 'message': 'success'}
