import asyncio
import json

from adapter.queue.sqs_queue import SQSQueueRepository
from security_scanner.settings import SQS_queue_name


class Manager:
    def __init__(self, tasks: dict, queue_name: str = SQS_queue_name):
        self.loop = asyncio.get_event_loop()
        self.tasks = tasks
        self.queue = SQSQueueRepository(queue_name=queue_name)

    async def _get_messages(self):
        """Read and pop messages from SQS queue
        """
        with self.queue as queue:
            response = queue.get_messages()
            messages = response.get('Messages', [])
            if messages:
                queue.acknowledge(handles=[m['ReceiptHandle'] for m in messages])
            return messages

    async def main(self):
        """For a given task:
        >>> async def say(something):
                pass

        Messages from queue are expected to have the format:
        >>> message = dict(task='say', args=('something',), kwargs={})
        >>> message = dict(task='say', args=(), kwargs={'something': 'something else'})
        """
        while True:
            messages = await self._get_messages()
            for message in messages:
                body = json.loads(message['Body'])

                task_name = body.get('task')
                args = body.get('args', ())
                kwargs = body.get('kwargs', {})

                task_coro = self.tasks.get(task_name)
                task = self.loop.create_task(task_coro(*args, **kwargs))
                print(f"Scheduled task {task_name} with {args} and {kwargs}")
            await asyncio.sleep(1)
