from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import AuditLog

class AuditLogListView(LoginRequiredMixin, ListView):
    model = AuditLog
    template_name = 'audit/auditlog_list.html'
    context_object_name = 'logs'
    paginate_by = 25

    def get_queryset(self):
        queryset = AuditLog.objects.select_related('utilisateur', 'content_type').all()
        action = self.request.GET.get('action')
        user = self.request.GET.get('user')
        if action:
            queryset = queryset.filter(action=action)
        if user:
            queryset = queryset.filter(utilisateur__username__icontains=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_choices'] = AuditLog.ACTION_CHOICES
        return context