from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

GROUPS_PERMISSIONS = {
    'Administrateur': {
        'all': True,
    },
    'Gérant': {
        'models': ['product', 'category', 'supplier', 'customer', 'purchase', 'sale', 'stockmovement'],
        'permissions': ['view', 'add', 'change'],
    },
    'Magasinier': {
        'models': ['product', 'category', 'supplier', 'purchase', 'stockmovement'],
        'permissions': ['view', 'add', 'change'],
    },
    'Caissier': {
        'models': ['sale', 'customer'],
        'permissions': ['view', 'add', 'change'],
    },
}

class Command(BaseCommand):
    help = 'Initialise les groupes et leurs permissions'

    def handle(self, *args, **options):
        for group_name, config in GROUPS_PERMISSIONS.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(f'Groupe {group_name} créé.')
            else:
                self.stdout.write(f'Groupe {group_name} existe déjà.')

            if config.get('all'):
                permissions = Permission.objects.all()
                group.permissions.set(permissions)
                self.stdout.write(f'→ Toutes les permissions attribuées à {group_name}.')
            else:
                # Permissions spécifiques à configurer plus tard (quand les modèles existeront)
                self.stdout.write(f'→ Permissions spécifiques à configurer plus tard pour {group_name}.')

        self.stdout.write(self.style.SUCCESS('Groupes initialisés avec succès.'))