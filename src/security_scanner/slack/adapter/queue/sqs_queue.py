from contextlib import AbstractContextManager
import os

import boto3
from botocore.exceptions import ClientError

from security_scanner.settings import SQS_queue_name


class SQSQueueRepository(AbstractContextManager):
    def __init__(self, queue_name: str = SQS_queue_name):
        self.queue_name = queue_name
        self.client = None
        self.queue_url = None

    def __enter__(self):
        if self.client is None:
            self.client = boto3.client('sqs')
        self._create_queue()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def _create_queue(self, attributes=None):
        if not attributes:
            attributes = {}
        try:
            response = self.client.create_queue(QueueName=self.queue_name, Attributes=attributes)
            self.queue_url = response.get('QueueUrl')
        except ClientError as error:
            raise error

    def send_message(self, message_body: str, message_attributes=None):
        if not message_attributes:
            message_attributes = {}

        try:
            response = self.client.send_message(QueueUrl=self.queue_url,
                                                MessageBody=message_body,
                                                MessageAttributes=message_attributes)
        except ClientError as error:
            raise error
        else:
            return response








