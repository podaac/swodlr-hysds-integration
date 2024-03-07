import json
from importlib import resources
from os import environ
from os.path import expanduser

import boto3
from dotenv import load_dotenv
import fastjsonschema

def notify_swodlr(context):
    topic_arns = environ['SWODLR_SNS_TOPIC_ARNS'].split(',')
    sns = boto3.client('sns')

    update_schema = json.load(
        resources.files.join_path('schemas/sds_update.json').open('r')
    )
    
    message_body = fastjsonschema.validate(update_schema, {
        'job_id': context['job_id'],
        'status': context['status'],
        'products_staged': context['products_staged']
    })
    
    for arn in topic_arns:
        sns.publish(
            TopicArn=arn,
            Message=json.dumps(
                message_body,
                separators=(',', ':'),
                indent=None
            )
        )
        

def main():
    load_dotenv(dotenv_path=expanduser('~/.swodlr'))
    context = json.load(open('_context.json', 'r'))
    notify_swodlr(context)


if __name__ == '__main__':
    main()
