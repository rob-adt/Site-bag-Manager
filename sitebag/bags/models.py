from django.db import models


class Bags(models.Model):
    inbag=models.CharField(max_length=200)

class Borrowingtime(models.Model):
    start=models.DateTimeField("date borrowed")
    end=models.DateTimeField("date returned")
    member= models.CharField(max_length=200)
    borrow= bool("Is it borrowed right now")


class Employees(models.Model):
    borrowed = models.ForeignKey(Borrowingtime, on_delete=models.CASCADE)