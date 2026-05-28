from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from inventory.models import ProductStock, Warehouse, StockMovement
from analytics.models import InventoryReport, StockAlert

class Command(BaseCommand):
    help = 'Create groups and permissions for the warehouse system'

    def handle(self, *args, **options):
        # Define groups
        groups = ['admin', 'warehouse_manager', 'warehouse_staff', 'viewer']

        # Create groups
        for group_name in groups:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created group: {group_name}"))
            else:
                self.stdout.write(f"Group already exists: {group_name}")

        # Get all permissions
        all_permissions = Permission.objects.all()

        # Assign all permissions to admin group
        admin_group = Group.objects.get(name='admin')
        admin_group.permissions.set(all_permissions)
        self.stdout.write(self.style.SUCCESS(f"Assigned all {all_permissions.count()} permissions to admin group"))

        # Define permissions for warehouse_manager
        manager_perms = [
            'view_warehouse', 'add_warehouse', 'change_warehouse', 'delete_warehouse',
            'view_productstock', 'add_productstock', 'change_productstock', 'delete_productstock',
            'view_stockmovement', 'add_stockmovement',
            'view_inventoryreport', 'add_inventoryreport',
            'view_stockalert', 'change_stockalert',
        ]

        manager_group = Group.objects.get(name='warehouse_manager')
        for perm_codename in manager_perms:
            try:
                perm = Permission.objects.get(codename=perm_codename)
                manager_group.permissions.add(perm)
            except Permission.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"Permission not found: {perm_codename}"))
        self.stdout.write(self.style.SUCCESS(f"Assigned {len(manager_perms)} permissions to warehouse_manager"))

        # Define permissions for warehouse_staff
        staff_perms = [
            'view_warehouse',
            'view_productstock', 'change_productstock',
            'view_stockmovement', 'add_stockmovement',
            'view_stockalert',
        ]

        staff_group = Group.objects.get(name='warehouse_staff')
        for perm_codename in staff_perms:
            try:
                perm = Permission.objects.get(codename=perm_codename)
                staff_group.permissions.add(perm)
            except Permission.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"Permission not found: {perm_codename}"))
        self.stdout.write(self.style.SUCCESS(f"Assigned {len(staff_perms)} permissions to warehouse_staff"))

        # Define permissions for viewer
        viewer_perms = [
            'view_warehouse',
            'view_productstock',
            'view_stockmovement',
            'view_inventoryreport',
            'view_stockalert',
        ]

        viewer_group = Group.objects.get(name='viewer')
        for perm_codename in viewer_perms:
            try:
                perm = Permission.objects.get(codename=perm_codename)
                viewer_group.permissions.add(perm)
            except Permission.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"Permission not found: {perm_codename}"))
        self.stdout.write(self.style.SUCCESS(f"Assigned {len(viewer_perms)} permissions to viewer"))

        self.stdout.write(self.style.SUCCESS("Successfully created all groups and permissions"))
