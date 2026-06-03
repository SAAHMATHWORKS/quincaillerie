from django.contrib.contenttypes.models import ContentType
from .models import AuditLog

class AuditMixin:
    """
    Mixin à ajouter aux vues génériques CreateView, UpdateView, DeleteView.
    Enregistre automatiquement un log de l'action.
    """

    def form_valid(self, form):
        # Appeler la méthode parente d'abord pour créer/mettre à jour l'objet
        response = super().form_valid(form)
        # Déterminer l'action
        if self.request.resolver_match.url_name in ['create', 'customer_create_ajax', 'supplier_create', 'purchase_create', 'sale_create'] \
                or isinstance(self, CreateView):
            action = 'CREATE'
        else:
            action = 'UPDATE'
        self._log_action(action, self.object)
        return response

    def form_valid(self, form):
        """Override pour capturer la création/modification"""
        response = super().form_valid(form)
        # Déterminer si création ou modification
        if hasattr(self, 'object') and self.object.pk and not getattr(self, '_audit_created', False):
            # Modification
            action = 'UPDATE'
            self._log_action(action, self.object)
        return response

    def form_valid_create(self, form):
        # Appelé spécifiquement pour les créations
        response = super().form_valid(form)
        self._audit_created = True
        self._log_action('CREATE', self.object)
        return response

    def form_valid_update(self, form):
        response = super().form_valid(form)
        self._log_action('UPDATE', self.object)
        return response

    def delete(self, request, *args, **kwargs):
        # Pour les DeleteView
        self.object = self.get_object()
        self._log_action('DELETE', self.object)
        return super().delete(request, *args, **kwargs)

    def _log_action(self, action, obj):
        """Crée l'entrée de log."""
        try:
            AuditLog.objects.create(
                action=action,
                content_type=ContentType.objects.get_for_model(obj),
                object_id=obj.pk,
                utilisateur=self.request.user if self.request.user.is_authenticated else None,
                description=str(obj)
            )
        except Exception as e:
            print(f"Erreur audit: {e}")