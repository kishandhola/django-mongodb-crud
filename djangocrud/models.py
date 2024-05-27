# models.py
from django.db import models

class MyModel(models.Model):
    """
    A class that represents a model for storing user information.

    Attributes:
        name (CharField): The name of the user.
        email (EmailField): The email of the user.
        gender (CharField): The gender of the user.
        dob (DateField): The date of birth of the user.
        country (CharField): The country of the user.
        hobbies (TextField): The hobbies of the user.
        message (CharField): The message of the user.
        createdAt (DateTimeField): The date and time of creation.

    """
    name = models.CharField(max_length=100, default="")
    email = models.EmailField(max_length=100, default="")
    gender = models.CharField(max_length=10, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
    ], default='not specified')
    dob = models.DateField()
    country = models.CharField(max_length=100, choices=[
        ('', 'Select Value'),
        ('US', 'United States'),
        ('UK', 'United Kingdom'),
        ('IN', 'India'),
        ('CA', 'Canada'),
    ], default='')

    hobbies = models.TextField(default='')
    message = models.CharField(max_length=300, default="")
    createdAt = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        """
        Returns a string representation of the MyModel object.

        Returns:
            str: The name of the object.
        """
        return self.name
    