from django.contrib.auth.models import User
from django.db import models


class Person(User):
    code = models.PositiveIntegerField()
    age = models.PositiveIntegerField()
    # notifications = models.CharField(max_length=1000000)
    # error = models.CharField(max_length=1000000)


class PaymentMethod(models.Model):
    type = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    balance = models.PositiveIntegerField
    user = models.ForeignKey(Person, on_delete=models.CASCADE)


class PetCategory(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category


class PetCategoryKind(models.Model):
    kind = models.CharField(max_length=100)
    category = models.ForeignKey(PetCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.category.category + ' : ' + self.kind


class Pet(models.Model):
    age = models.PositiveIntegerField()
    category = models.ForeignKey(PetCategory, on_delete=models.CASCADE)
    kind = models.ForeignKey(PetCategoryKind, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    state = models.CharField(max_length=10)
    image = models.CharField(max_length=100)

    def __str__(self):
        return str(self.age) + ' : ' + self.category.category + ' : ' + self.kind.kind


class HistoryRecord(models.Model):
    date = models.DateField(max_length=100)
    veterinary = models.CharField(max_length=500)
    description = models.CharField(max_length=90000)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
