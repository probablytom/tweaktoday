from django import template
import datetime
from django.template.defaultfilters import stringfilter

import markdown as md

register = template.Library()
message_to_send = \
"""
New features!

1. Suggested tasks that are not given a vote within 10 days are placed in the backburner.<br>A vote for a backburner task brings it out of the backburner. Hopefully then stagnant tasks have a kind of archive to live in.
2. Task suggestions can now be sorted by vote, time, and "backburner".
3. Old challenges can still be submitted to even if a new one has been posted, by request from @kellydna.
4. Submissions and comments support markdown (and by extension, things like youtube and imgur embeds). Throw me an email at tweaktoday -at- tomwallis -dot- net if you want photo/video comments.
5. Submissions and comments support deletion.

This message will be removed automatically tomorrow.
"""
date_of_message_timeout = datetime.datetime(year=2020, month=4, day=4)  # 20200405

# @stringfilter
@register.filter
def markdown(value):
    return md.markdown(value, extensions=['markdown.extensions.fenced_code'])

@register.simple_tag
def motd():
    return md.markdown(message_to_send, extensions=['markdown.extensions.fenced_code']) if date_of_message_timeout > datetime.datetime.today() else ""

def motd_context(_request):
    return {'motd': message_to_send if date_of_message_timeout > datetime.datetime.now() else ""}
