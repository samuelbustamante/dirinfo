# coding=utf-8

from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DetailView
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from tickets.models import PERMISSION_CAN_ASSIGNED
from tickets.models import PERMISSION_CAN_CHANGE_STATUS
from tickets.models import Ticket, Comment
from tickets.forms import CommentForm

CAN_ASSIGNED = "tickets.%s" % PERMISSION_CAN_ASSIGNED
CAN_CHANGE_STATUS = "tickets.%s" % PERMISSION_CAN_CHANGE_STATUS


class TicketListView(ListView):
    """
    Ticket list
    """
    model = Ticket
    context_object_name = "ticket_list"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TicketListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        if self.request.user.has_perm(CAN_CHANGE_STATUS):
            if self.request.user.has_perm(CAN_ASSIGNED):
                return Ticket.objects.all()
            else:
                from django.db.models import Q
                return Ticket.objects.order_by("-priority").filter(
                    Q(assigned=self.request.user) |
                    Q(created_by=self.request.user))#.distinct("pk")
        else:
            return Ticket.objects.filter(created_by=self.request.user.pk)


class TicketCreateView(CreateView):
    """
    Create ticket
    """
    model = Ticket
    fields = ["title", "description"]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TicketCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(TicketCreateView, self).form_valid(form)


class TicketStatusUpdateView(UpdateView):
    """
    Assign and change priority to a ticket.
    """
    model = Ticket
    fields = ["status"]
    template_name_suffix = "_status_form"

    @method_decorator(login_required)
    @method_decorator(permission_required(CAN_CHANGE_STATUS))
    def dispatch(self, *args, **kwargs):
        return super(TicketStatusUpdateView, self).dispatch(*args, **kwargs)


class TicketAssignedUpdateView(UpdateView):
    """
    Assign and change priority to a ticket.
    """
    model = Ticket
    fields = ["assigned", "priority"]
    template_name_suffix = "_assigned_form"

    @method_decorator(login_required)
    @method_decorator(permission_required(CAN_ASSIGNED))
    def dispatch(self, *args, **kwargs):
        return super(TicketAssignedUpdateView, self).dispatch(*args, **kwargs)


class TicketDetailView(DetailView):
    """
    Ticket detail
    """
    model = Ticket
    context_object_name = "ticket"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TicketDetailView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TicketDetailView, self).get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            self.form_valid(form)
        return super(TicketDetailView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.instance
        comment.created_by = self.request.user
        comment.ticket = Ticket.objects.get(pk=self.kwargs['pk'])
        comment.save()
