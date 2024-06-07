from django.db import models
from categories.models import Category
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=60)
    car_price = models.DecimalField(decimal_places=2, max_digits=20, default=0.00)
    description = models.TextField()
    quantity = models.IntegerField(default=1)
    is_completed = models.BooleanField(default='False')
    assign_date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/media/uploads/', blank = True, null = True)

    def __str__(self):
        return self.title    



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=30)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"comments by {self.name}"