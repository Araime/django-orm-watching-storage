from datacenter.models import Passcard, Visit
from django.shortcuts import render
from datacenter.models import get_durations_for_all_time, format_duration, is_visit_long
from django.utils.timezone import localtime


def passcard_info_view(request, passcode):
    passcard = Passcard.objects.get(passcode=passcode)
    all_visits_by_passcard = Visit.objects.filter(passcard=passcard)
    this_passcard_visits = []

    for visit in all_visits_by_passcard:
        entrance_time = localtime(value=visit.entered_at, timezone=None)
        duration = get_durations_for_all_time(visit)
        spent_time = format_duration(duration)
        suspicious_or_not = is_visit_long(duration, minutes=60)
        this_passcard_visit = {
                "entered_at": entrance_time,
                "duration": spent_time,
                "is_strange": suspicious_or_not
                }
        this_passcard_visits.append(this_passcard_visit)

    context = {
        "passcard": passcard,
        "this_passcard_visits": this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
