# f,rom email.policy import default
from django.db import models
from django.contrib.auth.models import User

    
class Content(models.Model):
   
    title = models.CharField(max_length=140)
    # blurがかかった単語
    blur_word = models.CharField(max_length=140)
    # blurのかかっていない単語
    content = models.TextField()
    new_content = models.TextField(null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.IntegerField()
    
    def __str__(self):
        return self.title
    
    