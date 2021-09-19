from django.db import models
from django.utils import timezone
from django.shortcuts import reverse
from django.contrib.auth.models import User

# python manage.py migrate app_name zero

# Create your models here.
class PickledModelsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(purpose= 'Summarizer')


class PickledModel(models.Model):
    purpose_choice=(
        ('Preprocessor', 'Preprocessor'),
        ('Summarizer', 'Summarizer')
    )
    accuracy_choice=(
        ('low',"Low"),
        ('medium','Medium'),
        ('high','High')
    )
    name = models.CharField(max_length=100, unique=True)
    purpose = models.CharField(max_length=100, choices=purpose_choice)
    file = models.FileField(upload_to="",null=True, blank=True)
    accuracy = models.CharField(max_length=10, choices=accuracy_choice ,default=accuracy_choice[0][0])
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL ,null=True, related_name='model_uploads')
    slug = models.SlugField(max_length=250, unique_for_date='created_at', default=None, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    preprocessor = models.CharField(max_length=250, default='strip')
    default = models.BooleanField(default=False)
    # Manager
    objects = models.Manager()
    summarizer = PickledModelsManager()

    class Meta:
        ordering = ('-purpose',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('Model:model_detail',\
            args=[self.purpose,  self.created_at.year, self.created_at.month, self.created_at.day, self.slug])
