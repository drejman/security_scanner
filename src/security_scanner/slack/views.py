import json

from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator

from slack.adapter.queue.sqs_queue import SQSQueueRepository


@method_decorator(csrf_exempt, name='dispatch')
class EventView(View):
    async def post(self, request):
        payload = json.loads(request.body)
        if payload.get("challenge"):
            return JsonResponse({'challenge': payload['challenge']})
        else:
            print(payload)
            with SQSQueueRepository() as queue:
                queue.send_message(json.dumps(payload['event']))
            # Message queue should be injected
            return HttpResponse("OK", status=200)
