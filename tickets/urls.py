# coding=utf-8

from django.conf.urls import url
from tickets.views import TicketListView
from tickets.views import TicketCreateView
from tickets.views import TicketDetailView
from tickets.views import TicketStatusUpdateView
from tickets.views import TicketAssignedUpdateView

urlpatterns = [
    url(r"^$",
        TicketListView.as_view(),
        name="list"
        ),
    url(r"^crear/$",
        TicketCreateView.as_view(),
        name="create"
        ),
    url(r"^(?P<pk>[0-9]+)/$",
        TicketDetailView.as_view(),
        name="detail"
        ),
    url(r"^(?P<pk>[0-9]+)/cambiar/estado/$",
        TicketStatusUpdateView.as_view(),
        name="change_status",
        ),
    url(r"^(?P<pk>[0-9]+)/cambiar/asignado-prioridad/$",
        TicketAssignedUpdateView.as_view(),
        name="change_assigned",
        ),
]
