from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from django.utils.timezone import localtime
from .models import get_duration, format_duration
from .models import Visit


def storage_information_view(request):
    visits = Visit.objects.filter(leaved_at=None)

    for visit in visits:
        non_closed_visits = []
        visitor_name = visit.passcard.owner_name
        then = localtime(value=visit.entered_at, timezone=None)
        duration = get_duration(visit)
        time_spent = format_duration(duration)
        non_closed_visit = {
            "who_entered": visitor_name,
            "entered_at": then,
            "duration": time_spent,
            }
        non_closed_visits.append(non_closed_visit)

    context = {
        "non_closed_visits": non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
