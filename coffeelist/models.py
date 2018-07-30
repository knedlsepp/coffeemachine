from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    tag_value = models.CharField(max_length=200, unique=True)
    owner = models.ForeignKey(User, null=False)
    def __str__(self):
        return '%s => %s' % (self.tag_value, self.owner)

class Purchase(models.Model):
    tag = models.ForeignKey(Tag, null=False)
    date = models.DateTimeField('date of purchase')
    def __str__(self):
        return '%s => %s' % (self.date, self.tag)

class Price(models.Model):
    date = models.DateTimeField('Date when the price changed')
    euros = models.DecimalField(max_digits=6, default=0, decimal_places=2)
    def __str__(self):
        return '%s: %s' % (self.date, self.euros)

class Deposit(models.Model):
    person = models.ForeignKey(User)
    date = models.DateTimeField('Date of transaction')
    euros = models.DecimalField(max_digits=6, decimal_places=2)
    def __str__(self):
        return '%s, %s => %s' % (self.person, self.date, self.euros)
