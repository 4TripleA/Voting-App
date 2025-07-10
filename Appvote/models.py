from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField(max_length=200)
    total_vote = models.IntegerField(default=0)
    voters = models.ManyToManyField(User, blank=True)
 
    def __str__(self):
        return self.title

class CategoryItem(models.Model):
    title = models.CharField(max_length=100)
    total_vote = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="items")
    voters = models.ManyToManyField(User, blank=True)

    @property
    def percentagevote(self):
        categoryvotes = self.category.total_vote
        itemvotes = self.total_vote
 
        if categoryvotes == 0:
            voteinpercentage = 0
        else:
            voteinpercentage = (itemvotes / categoryvotes ) * 100
        return voteinpercentage

    def __str__(self):
        return self.title
