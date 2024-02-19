from contextlib import AbstractContextManager
from typing import Self

import boto3
from botocore.exceptions import ClientError

from security_scanner.settings import SQS_queue_name


class SQSQueueRepository(AbstractContextManager):
    def __init__(self, queue_name: str = SQS_queue_name):
        self.queue_name = queue_name
        self.client = None
        self.queue_url = None

    def __enter__(self) -> Self:
        if self.client is None:
            self.client = boto3.client('sqs')
        self._get_queue()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def _get_queue(self):
        try:
            response = self.client.get_queue_url(QueueName=self.queue_name)
            self.queue_url = response.get('QueueUrl')
        except ClientError as error:
            raise error

    def get_messages(self):
        try:
            response = self.client.receive_message(QueueUrl=self.queue_url)
        except ClientError as error:
            raise error
        else:
            return response

    def acknowledge(self, handles: list[str]):
        try:
            response = self.client.delete_message_batch(QueueUrl=self.queue_url,
                                                        Entries=[
                                                            {'Id': str(i),
                                                             'ReceiptHandle': handle}
                                                            for i, handle in enumerate(handles)
                                                        ],
                                                        )
        except ClientError as error:
            raise error
        else:
            return response

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
