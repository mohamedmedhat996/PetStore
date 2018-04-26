from django.db import models

from Home.models import Person, Pet


class RecentSearch(models.Model):
    keys = models.CharField(max_length=1000)
    user = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return "search for : " + str(self.keys)


class Comment(models.Model):
    body = models.CharField(max_length=5000)
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pet) + " " + str(self.pk)
