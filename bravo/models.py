#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

from django.db import models
from charlie.models import Charlie
from delta.models import Delta

class Bravo(models.Model):
    charlie = models.ForeignKey(Charlie)
    delta = models.ForeignKey(Delta)
