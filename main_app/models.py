from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



# Create your models here.
class Digimon(models.Model):
  name = models.CharField(max_length=260, unique=True)
  img = models.CharField(max_length=260)
  level = models.TextField(max_length=260)
  happiness = models.IntegerField()
  # Create a cat >--< Toy relationship
  user = models.ManyToManyField(User, related_name='digimon')
  toys = models.ManyToManyField('Toy')
  # User --< Digimon
  # user = models.ForeignKey(User, on_delete=models.CASCADE)
  def clean(self):
    """Ensure a user cannot have more than 6 Digimon."""
    for user in self.user.all():
      if user.digimon.count() >= 6:
        raise ValidationError(f"{user.username} cannot have more than 6 Digimon in their digifarm.")
  def save(self, *args, **kwargs):
    """Call clean() before saving to enforce validation."""
    self.clean()
    super().save(*args, **kwargs)
  def add_user(self, user):
    """Custom method to add a user while enforcing the limit."""
    if user.digimon.count() >= 6:
      raise ValidationError(f"{user.username} cannot have more than 6 Digimon in their digifarm.")
    self.user.add(user)  
  
  
  def __str__(self):
    return f"{self.name} ({self.id})"
  
  # def fed_for_the_day(self):
  #   return self.feeding_set.filter(date='2025-02-14').count() >= 3
  
  # Define a method to get the URL for this particular cat instance
  def get_absolute_url(self):
    # Use the 'reverse' function to dynamically find URL for 
    #   viewing this cat's details
    return reverse('digimon-index', kwargs={'digimon_id': self.id })
  
class Toy(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('toy-detail', kwargs={'pk': self.id})
  
    

  