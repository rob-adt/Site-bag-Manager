from django.db import models


class Bags(models.Model):
    inbag=models.CharField(max_length=200)
    def __str__(self):
        return self.inbag

class Borrowingtime(models.Model):
    start=models.DateTimeField("date borrowed")
    end=models.DateTimeField("date returned")
    member= models.CharField(max_length=200)
    borrow= bool("Is it borrowed right now")


class Employees(models.Model):
    employee_name=models.CharField(max_length=100)
    borrowed = models.ForeignKey(Borrowingtime, on_delete=models.CASCADE)
    def __str__(self):
        return self.employee_name