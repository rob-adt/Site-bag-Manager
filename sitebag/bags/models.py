from django.db import models
from django.conf import settings


class Bag(models.Model):
    inbag=models.CharField(max_length=200)
    contents=models.TextField(null=True,blank=True) 
    def __str__(self):
        return self.inbag
    
class Employee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)    
    def __str__(self):
        return self.user.username
    
class Borrowingtime(models.Model):
    start=models.DateTimeField("date borrowed")
    end=models.DateTimeField("date returned",null=" ",blank=" ")
    member = models.ForeignKey(Employee, on_delete=models.CASCADE,null=True)
    bag = models.ForeignKey(Bag, on_delete=models.CASCADE, related_name="borrowingtimes")    
    def __str__(self):
        # return f"{self.member} on {self.start.strftime("%d/%m/%y")}-{self.bag}"
        return f"{self.member} on {self.start.strftime('%d/%m/%y')}-{self.bag}"
