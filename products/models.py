from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=255)  # Change 'name' to 'title'
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()  # Add description field
    image = models.URLField()  # Add image field
    category = models.CharField(max_length=255)  # Add category field

    def __str__(self):
        return self.title  # Ensure it returns title
