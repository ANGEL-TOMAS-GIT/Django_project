# accounts/models.py
from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Administrator'),
        ('warehouse_manager', 'Warehouse Manager'),
        ('warehouse_staff', 'Warehouse Staff'),
        ('viewer', 'Viewer'),
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='viewer')
    phone = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.username} - {self.get_user_type_display()}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        # Assign group based on user_type
        if is_new:
            self.assign_group()

    def assign_group(self):
        """Assign user to appropriate group based on user_type"""
        group_name = self.user_type
        try:
            group = Group.objects.get(name=group_name)
            self.groups.add(group)
        except Group.DoesNotExist:
            pass

    class Meta:
        db_table = 'accounts_user'
        permissions = [
            ("manage_inventory", "Can manage inventory"),
            ("view_analytics", "Can view analytics"),
        ]


# Signal to assign group when user_type changes
@receiver(post_save, sender=User)
def assign_group_on_update(sender, instance, **kwargs):
    if instance.groups.count() == 0:
        instance.assign_group()
