##
# -*- coding: utf-8 -*-
##
##
# SNS Subscribe.
##

# Import community modules.
import sys
import json
import argparse

# Import AWS SDK.
import boto3

# Initializing Amazon SNS client.
SNS = boto3.client('sns',region_name='us-west-2')

# Parsing command line arguments.
parser = argparse.ArgumentParser()
parser.add_argument('-t',dest='topic',type=str,required=True,help='ARN of the SNS topic.')
parser.add_argument('-e',dest='email',type=str,required=True,help='Subscriber email address. Example: tuto@sloopstash.com.')
args = parser.parse_args()

# Add new subscriber to specified Amazon SNS topic.
response = SNS.subscribe(
  TopicArn=args.topic,
  Protocol='email',
  Endpoint=args.email,
  ReturnSubscriptionArn=True
)
print(json.dumps(response, indent=4))