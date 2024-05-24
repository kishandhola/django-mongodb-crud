import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.core import validators
from .models import MyModel

class PdfFileField(forms.FileField):
    def validate(self, value):
        super().validate(value)
        if value:
            if not value.name.lower().endswith('.pdf'):
                raise ValidationError(('File must be a PDF.'))


class MyForm(forms.ModelForm):
    """
    This module defines a Django form class `MyForm` for handling user input and validating various fields.
    The form is associated with the `MyModel` model and includes custom validation methods for several fields.

    Classes:
        MyForm(forms.ModelForm): A form class for `MyModel` with custom validation logic.

    Methods:
        __init__(self, *args, **kwargs): Initializes the form and sets the initial value of all fields to an empty string.
        clean_password(self): Validates the password field to ensure it meets specific criteria.
        clean_dob(self): Validates the date of birth field to ensure the user is at least 18 years old.
        clean_hobbies(self): Validates the hobbies field to ensure the user selects at least 3 hobbies.
        clean_message(self): Validates the message field to ensure it is between 8 and 300 characters long.
        clean_file(self): Validates the file field to ensure it meets size and type requirements.

    Meta:
        model (MyModel): The model associated with this form.
        fields (list): The list of fields to include in the form.
        widgets (dict): Custom widgets for specific fields.
    """

    HOBBIES_CHOICES = [
        ('reading', 'Reading'),
        ('sports', 'Sports'),
        ('music', 'Music'),
        ('traveling', 'Traveling'),
        ('gaming', 'Gaming'),
    ]

    hobbies = forms.MultipleChoiceField(
        choices=HOBBIES_CHOICES,
        widget=forms.CheckboxSelectMultiple
    )


    file = PdfFileField()


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.initial = ""


    def clean_password(self):
        """
        Validates the password input to ensure it meets the specified criteria:
        - Contains at least one letter
        - Contains at least one digit
        - Contains at least one uppercase letter
        - Contains at least one lowercase letter
        - Contains at least one special character
        Raises a ValidationError if any of the criteria is not met.
        
        Returns:
            str: The validated password data.
        """
        data = self.cleaned_data['password']
        if not any(c.isalpha() for c in data):
            raise forms.ValidationError("Password must contain at least one letter.")
        if not any(c.isdigit() for c in data):
            raise forms.ValidationError("Password must contain at least one digit.")
        if not any(c.isupper() for c in data):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        if not any(c.islower() for c in data):
            raise forms.ValidationError("Password must contain at least one lowercase letter.")
        if not any(c in '!@#$%^&*()-_=+[]{};:\'",.<>?/~`' for c in data):
            raise forms.ValidationError("Password must contain at least one special character.")
        return data

    def clean_dob(self):
        """
        Validates the date of birth input to ensure the user is at least 18 years old to register.

        Returns:
            datetime.date: The validated date of birth data.
        """
        data = self.cleaned_data['dob']
        today = datetime.date.today()
        age = today.year - data.year - ((today.month, today.day) < (data.month, data.day))
        if age < 18:
            raise forms.ValidationError("You must be at least 18 years old to register.")
        return data

    def clean_hobbies(self):
        """
        A method that validates the hobbies input to ensure the user selects at least 3 hobbies.
        Returns:
            list: The list of validated hobbies.
        """
        data = self.cleaned_data['hobbies']
        if len(data) < 3:
            raise forms.ValidationError("Select at least 3 hobbies.")
        return data

    def clean_message(self):
        """
        A method that validates the message input to ensure it is between 8 and 300 characters long.
        """
        data = self.cleaned_data['message']
        if 8 > len(data) > 300:
            raise forms.ValidationError(
                "Message must be at least 8 characters long "
                "and at most 300 characters long."
            )
        return data

    def clean_file(self):
        """
        A method that validates the file input to ensure it meets the size and type requirements.
        """
        data = self.cleaned_data['file']
        if data.size > 5 * 1024 * 1024:  # 5MB
            raise forms.ValidationError("File size should be less than 5MB.")
        if not data.name.endswith('.pdf'):
            raise forms.ValidationError("File type must be PDF.")
        return data

    class Meta:
        model = MyModel
        fields = [
            'name', 'email', 'password', 'gender', 'dob', 'country', 'hobbies',
            'message', 'file',
        ]
        widgets = {
            'password': forms.PasswordInput(),
            'gender': forms.RadioSelect,
            'dob' : forms.DateInput(attrs={'type': 'date'}),
            'country': forms.Select,
            'message': forms.Textarea(attrs={'rows': 5}),
            'file' : forms.ClearableFileInput(attrs={'accept': 'application/pdf'})
        }

