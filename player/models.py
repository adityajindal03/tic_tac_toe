# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


from django.contrib.auth.models import User

class Invitation(models.Model):
    from_user = models.ForeignKey(User, related_name="invitation_sent")
    to_user = models.ForeignKey(User, related_name="invitation_recieved")
    message = models.CharField(max_length=300)
    timestamp = models.DateTimeField(auto_now_add=True)



# Create your models here.
