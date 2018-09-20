from lambdas import nea_send_email
from unittest.mock import patch


@patch('lambdas.nea_send_email.boto3')
def test_send_mail(boto3):
    event = {
        'email_from': 'from@example.com',
        'email_to': 'to@example.com',
        'message': 'Test message'
    }

    nea_send_email.lambda_handler(event, {})

    boto3.client().send_email.assert_called_with(
        Source=event['email_from'],
        Destination={
            'ToAddresses': [event['email_to']],
        },
        Message={
            'Subject': {
                'Data': 'Weekly Digest',
                'Charset': 'utf8'
            },
            'Body': {
                'Html': {
                    'Data': event['message'],
                    'Charset': 'utf8'
                }
            }
        },
        ReplyToAddresses=[
            event['email_from']
        ]
    )
