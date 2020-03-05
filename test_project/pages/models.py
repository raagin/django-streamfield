from django.db import models
from django.urls import reverse

from streamfield.fields import StreamField
from streamblocks.models import RichText, Column

class Page(models.Model):
    title = models.CharField(max_length=255)
    stream = StreamField(
        model_list=[ 
            RichText,
            Column
        ],
        verbose_name="Page blocks"
        )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('page', args=[self.pk])