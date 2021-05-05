from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from datacenter.models import get_durations, format_duration, is_visit_long
from django.utils.timezone import localtime


def passcard_info_view(request, passcode):
    passcard = Passcard.objects.get(passcode=passcode)
    all_visits = Visit.objects.filter(passcard=passcard)
    this_passcard_visits = []
    for visit in all_visits:
        when_entrance = localtime(value=visit.entered_at, timezone=None)
        duration = get_durations(visit)
        time_spent = format_duration(duration)
        suspicious_or_not = is_visit_long(duration, minutes=60)
        this_passcard_visit = {
                "entered_at": when_entrance,
                "duration": time_spent,
                "is_strange": suspicious_or_not
                }
        this_passcard_visits.append(this_passcard_visit)

    context = {
        "passcard": passcard,
        "this_passcard_visits": this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
