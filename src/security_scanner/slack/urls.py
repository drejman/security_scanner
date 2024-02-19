from django.urls import path
from slack.views import EventView

app_name = "slack"

urlpatterns = [
    path("events/", EventView.as_view(), name="slack_verification"),
]
