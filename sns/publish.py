##
# -*- coding: utf-8 -*-
##
##
# SNS Publish.
##

# Import community modules.
import sys
import json
import argparse

# Import AWS SDK.
import boto3

# Initializing Amazon SNS client.
SNS = boto3.client('sns',region_name='us-west-2')

# Parsing commandline arguments.
parser = argparse.ArgumentParser()
parser.add_argument('-t',dest='topic',type=str,required=True,help='ARN of the SNS Topic.')
parser.add_argument('-s',dest='subject',type=str,required=True,help='Subject. Example: Feature release.')
parser.add_argument('-m',dest='message',type=str,required=True,help='Message.')
args = parser.parse_args()

# Send message to subscribers.
response = SNS.publish(
  TopicArn=args.topic,
  Message=args.message,
  Subject=args.subject
)
print(json.dumps(response, indent=4))