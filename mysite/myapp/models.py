from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Line(models.Model):                    # model - class    - table
    text = models.CharField(max_length=255)  # field   - column


# Store translations - is ASCII enough?
class Word(models.Model):                    # model - class    - table
    english_text = models.CharField(max_length=255)
    spanish_text = models.CharField(max_length=255)

    def __str__(self):
        return '%s - %s' % (self.english_text, self.spanish_text)


class WordsUse(models.Model):                    # model - class    - table
    user = models.ForeignKey(User)
    english_text = models.ForeignKey(Word)
    translation_active = models.BooleanField(default=False)
    aparitions = models.IntegerField(default=0)
    click = models.IntegerField(default=0)




    def __str__(self):
        return '%s - %s- %s- %s- %s' % (self.user, self.english_text, self.translation_active, self.aparitions, self.click, )
