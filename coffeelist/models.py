from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Tag(models.Model):
    tag_value = models.CharField(max_length=200, unique=True)
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return '({}, Owner:{})'.format(self.tag_value, self.owner)


class Price(models.Model):
    date = models.DateTimeField('Date when the price changed', default=now)
    euros = models.DecimalField(max_digits=6, default=0, decimal_places=2)

    def __str__(self):
        return '({}€ since {:%x})'.format(self.euros, self.date)


class Purchase(models.Model):
    tag = models.ForeignKey(Tag, null=False, on_delete=models.CASCADE)
    date = models.DateTimeField(
        'date of purchase', default=now)  # Probably incorrect without a RTC
    price = models.ForeignKey(Price, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return '(Date: {:%x %X}, Tag:{}, Price: {})'.format(
            self.date, self.tag, self.price)


class Deposit(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField('Date of transaction', default=now)
    euros = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return '({person}, {date:%x %X}, {euros}€)'.format(
            person=self.person, date=self.date, euros=self.euros)
