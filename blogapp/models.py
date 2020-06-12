from django.db import models
from django.conf import settings
from django.urls import reverse

# Create your models here.
class Base(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    title = models.CharField(max_length = 100, blank = True)
    body = models.TextField()

    def __str__(self):
        return str(self.title)

    def get_url(self):
        return reverse("blogs-api:create")

 


class AddComment(models.Model):
    post_id = models.ForeignKey(Base, null=True, blank=True,  on_delete = models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    parent      = models.ForeignKey("self", null=True, blank=True, on_delete = models.CASCADE)


    comment = models.TextField()


    def get_api_url(self):
        return reverse("blogs-api:r-create", kwargs={"pk": self.post_id_id, "parent_id":self.id})



    def children(self): #replies
        return AddComment.objects.filter(parent=self)

    @property
    def is_parent(self):          #check wheter cmnt is actually a cmnt or just reply to a cmnt, if reply return false
        if self.parent is not None:    
            return False
        return True