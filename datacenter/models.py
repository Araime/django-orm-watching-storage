from django.db import models
from django.utils.timezone import localtime


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved='leaved at ' + str(self.leaved_at) if self.leaved_at else 'not leaved'
        )


def get_current_duration(visit):
    current_time = localtime(value=None, timezone=None)
    entrance_time = localtime(value=visit.entered_at, timezone=None)
    delta = current_time - entrance_time
    return delta.total_seconds()


def get_durations_for_all_time(visit):
    exit_time = localtime(value=visit.leaved_at, timezone=None)
    entrance_time = localtime(value=visit.entered_at, timezone=None)
    delta = exit_time - entrance_time
    return delta.total_seconds()


def format_duration(duration):
    number_of_seconds_total = int(duration)
    hours = number_of_seconds_total // 3600
    minutes = (number_of_seconds_total % 3600) // 60
    return f'{hours}ч {minutes}мин'


def is_visit_long(duration, minutes=60):
    total_minutes = int(duration) // 60
    return minutes < total_minutes
