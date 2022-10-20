from django.db import models


class URLMapping(models.Model):
    key = models.CharField(max_length=6, primary_key=True)
    target_url = models.URLField(max_length=1024)
    secret_key = models.CharField(max_length=16, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.key


class VisitedURL(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.ForeignKey(to=URLMapping, on_delete=models.DO_NOTHING)
    is_pc = models.BooleanField()
    user_ip = models.GenericIPAddressField()
    visited_date = models.DateTimeField(auto_now_add=True)
    # rrt = models.PositiveSmallIntegerField()  # values from 0 to 32767

    def __str__(self) -> str:
        return str(self.key)


