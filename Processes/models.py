from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Process(models.Model):
    process_type_choices=(
        ('Book','Book summarize'),
        ('Keyword',"Keyword based summarize"),
        ('correct PDF','PDF normalize')
    )
    progress_choices=(
        ('start','start'),
        ('extract','extract'),
        ('get_text','get_text'),
        ('summary','summary'),
        ('finished','finished'),
        ('summarized','summarized'),
        ('error','error'),
        ('corrected','corrected')
    )
    actor=models.ForeignKey(User,on_delete=models.CASCADE)
    process_type=models.CharField(max_length=50,choices=process_type_choices)
    file = models.FileField(upload_to="processes/")
    progress=models.CharField(max_length=30,choices=progress_choices)
    created_at=models.DateTimeField(default=timezone.now)
