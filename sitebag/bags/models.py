from django.db import models
from django.conf import settings

class Tags(models.Model):
    tag=models.CharField(max_length=100)
    def __str__(self):
        return self.tag

class Bag(models.Model):
    inbag=models.CharField(max_length=200)
    contents=models.TextField(null=True,blank=True) 
    tagg=models.ForeignKey(Tags, on_delete=models.CASCADE, related_name="Bag",null=True,blank=True)
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
    bag = models.ForeignKey(Bag, on_delete=models.CASCADE, related_name="borrowingtimes" ,null=" ",blank=" ")
    def __str__(self):
        # return f"{self.member} on {self.start.strftime("%d/%m/%y")}-{self.bag}"
        return f"{self.member} on {self.start.strftime('%d/%m/%y')}-{self.bag}"

