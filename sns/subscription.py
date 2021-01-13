##
# -*- coding: utf-8 -*-
##
##
# Manage SNS subscriptions.
##

# Import community modules.
import sys
import json
import argparse
import boto3

# Initialize SNS client.
SNS = boto3.client('sns',region_name='us-west-2')

# Parse CLI arguments.
cli = argparse.ArgumentParser(description='A CLI to manage SNS subscriptions.')
cli.add_argument('-t',dest='topic',type=str,required=True,help='ARN of the SNS topic.')
cli.add_argument('-e',dest='email',type=str,required=True,help='Email address of the SNS subscription.')
args = cli.parse_args()

# Create SNS subscription.
response = SNS.subscribe(
  TopicArn=args.topic,
  Protocol='email',
  Endpoint=args.email,
  ReturnSubscriptionArn=True
)
print(json.dumps(response, indent=4))
