#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

from django.db import models
from bravo.models import Bravo

class Alpha(models.Model):
    bravo = models.ForeignKey(Bravo)
