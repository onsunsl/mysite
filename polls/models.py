from django.db import models

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length = 200, verbose_name='问题')
    pub_date = models.DateField('date published')

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='选择')
    choice_text = models.CharField(max_length=200, verbose_name='选择文本')
    votes = models.IntegerField(default=0, verbose_name='投票')

    def __str__(self):
        return self.choice_text