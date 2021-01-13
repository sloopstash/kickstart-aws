##
# -*- coding: utf-8 -*-
##
##
# Manage SNS topics.
##

# Import community modules.
import sys
import json
import argparse
import boto3

# Initialize SNS client.
SNS = boto3.client('sns',region_name='us-west-2')

# Parse CLI arguments.
cli = argparse.ArgumentParser(description='A CLI to manage SNS topics.')
cli.add_argument('-t',dest='topic',type=str,required=True,help='ARN of the SNS topic.')
cli.add_argument('-s',dest='subject',type=str,required=True,help='Subject. Example: Feature release.')
cli.add_argument('-m',dest='message',type=str,required=True,help='Message.')
args = cli.parse_args()

# Publish message to SNS subscriptions.
response = SNS.publish(
  TopicArn=args.topic,
  Message=args.message,
  Subject=args.subject
)
print(json.dumps(response,indent=4))
