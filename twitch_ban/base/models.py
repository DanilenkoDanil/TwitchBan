from django.db import models


class Chanel(models.Model):
    county_choices = [
        ('Gr', 'Gr'),
        ('Fi', 'Fi'),
        ('No', 'No'),
        ('Ca', 'Ca'),
    ]
    title = models.CharField(max_length=256)
    link = models.CharField(max_length=256)
    ban = models.BooleanField(default=False)
    check_date = models.DateTimeField(auto_now=True)
    add_date = models.DateTimeField(auto_now=True)
    ban_date = models.DateTimeField(blank=True, null=True)
    county = models.CharField(choices=county_choices, max_length=100)
    spectators = models.IntegerField(default=0)
    subscribers = models.IntegerField(default=0)
    notes = models.TextField(default='', null=True, blank=True)


class TelegramAccount(models.Model):
    name = models.CharField(max_length=256)
    telegram_id = models.PositiveIntegerField()
