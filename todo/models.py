from django.db import models


# Create your models here.
# null=False restrics the field from being submitted whilst empty
# black=False means the field will be required within forms
class Item(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    done = models.BooleanField(null=False, blank=False, default=False)

    def __str__(self):
        return self.name
