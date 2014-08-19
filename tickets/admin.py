# coding=utf-8

from django.contrib import admin
from tickets.models import Ticket, Comment


class TicketAdmin(admin.ModelAdmin):
    """ Ticket admin """
    pass


class CommentAdmin(admin.ModelAdmin):
    """ Comment admin """
    pass


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Comment, CommentAdmin)
