from datacenter.models import Visit
from django.shortcuts import render
from django.utils.timezone import localtime
from .models import get_current_duration, format_duration


def storage_information_view(request):
    visits = Visit.objects.filter(leaved_at=None)
    non_closed_visits = []

    for visit in visits:
        visitor_name = visit.passcard.owner_name
        entrance_time = localtime(value=visit.entered_at, timezone=None)
        duration = get_current_duration(visit)
        how_much_is_there = format_duration(duration)
        non_closed_visit = {
            'who_entered': visitor_name,
            'entered_at': entrance_time,
            'duration': how_much_is_there,
            }
        non_closed_visits.append(non_closed_visit)

    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
