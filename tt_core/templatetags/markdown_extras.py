from django import template
import datetime
from django.template.defaultfilters import stringfilter

import markdown as md

register = template.Library()
message_to_send = "New feature! Task suggestions can now be sorted by vote and time, and have a \"backburner\". Suggested tasks that are not given a vote within 10 days are placed in the backburner. A vote for a backburner task brings it out of the backburner. Hopefully then stagnant tasks have a kind of archive to live in."
date_of_message_timeout = datetime.datetime(year=2020, month=4, day=4)  # 20200405

# @stringfilter
@register.filter
def markdown(value):
    return md.markdown(value, extensions=['markdown.extensions.fenced_code'])

@register.simple_tag
def motd():
    return message_to_send if date_of_message_timeout > datetime.datetime.today() else ""