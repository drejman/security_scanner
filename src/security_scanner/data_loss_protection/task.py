import re

from asgiref.sync import sync_to_async

from data_loss_protection.models import Alert, Pattern


@sync_to_async
def get_all_patterns():
    return list(Pattern.objects.all())


async def dlp_scan(*args, **kwargs):
    print(f"Logging from dlp task"
          f"Args: {args}, kwargs: {kwargs}", flush=True)
    event = kwargs.get("event", {})
    text = event.get("text")
    print(text)
    async for pattern in Pattern.objects.all():
        regexp = re.compile(pattern.pattern)
        if regexp.search(text):
            for match in regexp.finditer(text):
                alert = Alert(message=f"Data leak detected for rule {pattern.name}",
                              content=f"Leaked string: {match.group(0)} found in '{text}' at position {match.span()}",
                              channel=event.get("channel"),
                              pattern=pattern,
                              )
                await sync_to_async(alert.save)()
