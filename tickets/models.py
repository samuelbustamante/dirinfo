# coding=utf-8

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

STATUS_OPEN = 0
STATUS_ON_HOLD = 1
STATUS_BELATED = 2
STATUS_RESOLVED = 3
STATUS_CLOSED = 4
PRIORITY_LOW = 0
PRIORITY_NORMAL = 1
PRIORITY_HIGHT = 2
PERMISSION_CAN_ASSIGNED = "can_assigned"
PERMISSION_CAN_CHANGE_STATUS = "can_change_status"
PERMISSION_CAN_VIEW_PRIORITY = "can_view_priority"
PERMISSION_CAN_CHANGE_PRIORITY = "can_change_priority"


class Ticket(models.Model):
    """
    Ticket
    """
    STATUS_CHOICES = (
        (STATUS_OPEN, u'Abierto'),
        (STATUS_ON_HOLD, u'En proceso'),
        (STATUS_BELATED, u'Atrazado'),
        (STATUS_RESOLVED, u'Resuelto'),
        (STATUS_CLOSED, u'Cerrado'),
    )
    PRIORITY_CHOICES = (
        (PRIORITY_LOW, u"Baja"),
        (PRIORITY_NORMAL, u"Normal"),
        (PRIORITY_HIGHT, u"Alta"),
    )
    title = models.CharField(max_length=64)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="tickets_created")
    status = models.PositiveSmallIntegerField(default=STATUS_OPEN,
                                              choices=STATUS_CHOICES)
    priority = models.PositiveSmallIntegerField(default=PRIORITY_NORMAL,
                                                choices=PRIORITY_CHOICES)
    assigned = models.ManyToManyField(User, null=True,
                                 related_name="tickets_assigned")

    def get_absolute_url(self):
        return reverse("tickets:detail", args=[str(self.id)])

    def __unicode__(self):
        return u"%s" % self.title

    class Meta:
        permissions = (
            (PERMISSION_CAN_ASSIGNED, u"Can assigned"),
            (PERMISSION_CAN_CHANGE_STATUS, u"Can change status"),
            (PERMISSION_CAN_VIEW_PRIORITY, u"Can view priority"),
            (PERMISSION_CAN_CHANGE_PRIORITY, u"Can change priority"),
        )
        ordering = ["-created_on"]


class Comment(models.Model):
    """
    Comment
    """
    comment = models.TextField()
    created_by = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True)
    ticket = models.ForeignKey(Ticket, related_name="comments")

    def __unicode__(self):
        return u"%s" % self.comment

    class Meta:
        ordering = ["-created_on"]
        verbose_name = u"comment"
        verbose_name_plural = u"comments"
