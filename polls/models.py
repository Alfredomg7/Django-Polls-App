import datetime
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __repr__(self):
        return f'<Question: {self.question_text}>'

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?'
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def clean(self):
        if len(self.question_text) > 200:
            raise ValidationError('Question text is too long.')
    
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __repr__(self):
        return f'<Choice: {self.choice_text}>'