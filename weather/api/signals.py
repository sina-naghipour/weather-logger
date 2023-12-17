from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Client, ClientToken
from django.utils import timezone

@receiver(post_save, sender=Client)
def create_client_token(sender, instance, created, **kwargs):
    if created:
        token, token_created = ClientToken.objects.get_or_create(client=instance)
        if token_created:
            token.created = timezone.now()
            token.expires = token.created + timezone.timedelta(days=30)
            token.save()

@receiver(pre_delete, sender=Client)
def revoke_client_tokens(sender, instance, **kwargs):
    tokens = ClientToken.objects.filter(client=instance)
    for token in tokens:
        token.is_revoked = True
        token.save()