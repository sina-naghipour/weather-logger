from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=100)
    last_connection = models.CharField(max_length=225)


class ClientToken(models.Model):
    token = models.UUIDField(default=uuid4, editable=False, unique=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expires = models.DateTimeField()
    is_revoked = models.BooleanField(default=False)

    def is_expired(self):
        return self.expires < timezone.now()

    def revoke(self):
        self.is_revoked = True
        self.save()

    def __str__(self):
        return f'Token for {self.client.name}'