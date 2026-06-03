from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import AuditLog
from .middleware import get_current_user   # <-- ajout

MODELS_TO_AUDIT = [
    'inventory.category',
    'inventory.product',
    'inventory.inventory',
    'suppliers.supplier',
    'customers.customer',
    'purchases.purchase',
    'purchases.purchaseitem',
    'sales.sale',
    'sales.saleitem',
]

def get_class(model_path):
    from django.apps import apps
    return apps.get_model(model_path)

@receiver(post_save)
def audit_post_save(sender, instance, created, **kwargs):
    model_path = f"{sender._meta.app_label}.{sender._meta.model_name}"
    if model_path not in MODELS_TO_AUDIT:
        return
    if created:
        action = 'CREATE'
    else:
        action = 'UPDATE'
    if sender == AuditLog:
        return
    try:
        AuditLog.objects.create(
            action=action,
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.pk,
            utilisateur=get_current_user(),   # <-- modifié
            description=str(instance)
        )
    except Exception as e:
        print(f"Erreur audit: {e}")

@receiver(post_delete)
def audit_post_delete(sender, instance, **kwargs):
    model_path = f"{sender._meta.app_label}.{sender._meta.model_name}"
    if model_path not in MODELS_TO_AUDIT:
        return
    if sender == AuditLog:
        return
    try:
        AuditLog.objects.create(
            action='DELETE',
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.pk,
            utilisateur=get_current_user(),   # <-- modifié
            description=str(instance)
        )
    except Exception as e:
        print(f"Erreur audit delete: {e}")