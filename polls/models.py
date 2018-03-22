from django.db import models
from django.utils import timezone
import datetime
# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length = 200, verbose_name='问题')
    pub_date = models.DateTimeField('日期/时间')

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = '是最近发布的问题'


    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='选择')
    choice_text = models.CharField(max_length=200, verbose_name='选择文本')
    votes = models.IntegerField(default=0, verbose_name='投票')

    def __str__(self):
        return self.choice_text