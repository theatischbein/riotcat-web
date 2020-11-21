from django import template
from django.utils import timezone
import humanize
import datetime

register = template.Library()

@register.filter(name='humanizedtimedelta')
def humanizedtimedelta(value):
    delta = datetime.timedelta(seconds=value).total_seconds()
    hours = int(delta/60/60)
    minutes = int(delta/60 - hours*60)
    seconds = int(delta - minutes*60 - hours*60*60)
    return "%s%s%s" %(
        "%sh " %hours if hours > 0 else "",
        "%sm " %minutes if minutes > 0 else "",
        "< 1 Minute" if hours <= 0 and minutes <= 0 else "",
        #"%ss"  %seconds if seconds > 0 else ""
    )
    # _t = humanize.i18n.activate("de")
    # return humanize.precisedelta(datetime.timedelta(seconds=value),minimum_unit="minutes") if value else " -- "

@register.filter(name='getMonthTotal')
def getMonthTotal(value):
    sum = 0
    for work in value:
        if work.duration:
            sum += abs(work.duration)
    return "%sh %sm" %(int(sum / 60 / 60), int(sum % 60))

@register.filter(name="secondsToDays")
def secondsToDays(value, holiday=False):
    if holiday:
        return int(value / 60 / 60)
    else:
        return int(value / 60 / 60 / (40/30.5))+1