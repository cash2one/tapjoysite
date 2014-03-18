# -*- encoding: utf-8 -*-

from django.db import models

# Create your models here.


class Campaign(models.Model):
    campaign_id = models.CharField(max_length=64)
    campaign_name = models.CharField(max_length=200)
    app_id = models.CharField(max_length=36)
    CAMP_CHOICES = (
        (0, 'off'), (1, 1), (2, 2), (3, 3),
        (4, 4), (5, 5), (6, 6), (7, 7),
        (8, 8), (9, 9), (10, 'on')
    )

    campaign_level = models.SmallIntegerField(default=11, choices=CAMP_CHOICES)

    def __unicode__(self):
        return self.campaign_name
