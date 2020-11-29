import os

import boto3
from botocore.exceptions import ClientError

def store_link(link):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['db_table'])
    table.put_item(
        Item={'url': link},
        ConditionExpression='attribute_not_exists(#url)',
        ExpressionAttributeNames={'#url': 'url'}
    )

def store_posts(blogs):
    blogs_to_send = []
    for blog in blogs:
        items_to_send = []

        for item in blog['items']:
            try:
                store_link(item['link'])
                items_to_send.append(item)
            except ClientError as e:  
                if e.response['Error']['Code'] != 'ConditionalCheckFailedException':  
                    raise

        blogs_to_send.append({
            'title': blog['title'],
            'items': items_to_send
        })
    return blogs_to_send

def lambda_handler(event, context):
    return {
        'blogs': store_posts(event['blogs']),
        'email_from': event['email_from'],
        'email_to': event['email_to'],
    }
