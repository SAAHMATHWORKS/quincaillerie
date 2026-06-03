from django.core.management.base import BaseCommand
from apps.inventory.models import StockMovement
from apps.sales.models import Sale
from apps.purchases.models import Purchase
import re

class Command(BaseCommand):
    help = 'Lie les anciens StockMovement aux ventes/achats via la référence textuelle'

    def handle(self, *args, **options):
        mouvements = StockMovement.objects.filter(vente__isnull=True, achat__isnull=True)
        for mvt in mouvements:
            ref = mvt.reference or ''
            # Essayer de trouver "Vente #<id>"
            match = re.search(r'Vente\s*#?(\d+)', ref)
            if match:
                sale_id = int(match.group(1))
                try:
                    sale = Sale.objects.get(pk=sale_id)
                    mvt.vente = sale
                    mvt.save()
                    self.stdout.write(f'Lié mouvement {mvt.id} -> Vente #{sale_id}')
                    continue
                except Sale.DoesNotExist:
                    pass
            # Essayer de trouver "Achat #<id>"
            match = re.search(r'Achat\s*#?(\d+)', ref)
            if match:
                purchase_id = int(match.group(1))
                try:
                    purchase = Purchase.objects.get(pk=purchase_id)
                    mvt.achat = purchase
                    mvt.save()
                    self.stdout.write(f'Lié mouvement {mvt.id} -> Achat #{purchase_id}')
                    continue
                except Purchase.DoesNotExist:
                    pass
        self.stdout.write(self.style.SUCCESS('Terminé.'))