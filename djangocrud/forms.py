import datetime
from django import forms
from .models import MyModel

class MyForm(forms.ModelForm):
    """
    Form for MyModel with custom validation methods.
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


    def __init__(self, *args, **kwargs):
        """
        Initializes the form with the given arguments and keyword arguments.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None

        Sets the initial values for all fields in the form to an empty string.
        """
        super().__init__(*args, **kwargs)

        # Set initial values for other fields
        for field in self.fields.values():
            field.initial = ""



    def clean_dob(self):
        """
        Validates that the user is at least 18 years old.
        """
        data = self.cleaned_data['dob']
        today = datetime.date.today()
        age = today.year - data.year - ((today.month, today.day) < (data.month, data.day))
        if age < 18:
            raise forms.ValidationError("You must be at least 18 years old to register.")
        return data

    def clean_hobbies(self):
        """
        Validates that the user has selected at least 3 hobbies.
        """
        data = self.cleaned_data['hobbies']
        if len(data) < 3:
            raise forms.ValidationError("Select at least 3 hobbies.")
        return data

    def clean_message(self):
        """
        Validates that the message is between 8 and 300 characters long.
        """
        data = self.cleaned_data['message']
        if 8 > len(data) > 300:
            raise forms.ValidationError(
                "Message must be at least 8 characters long "
                "and at most 300 characters long."
            )
        return data

    class Meta:
        model = MyModel
        fields = [
            'name', 'email', 'gender', 'dob', 'country', 'hobbies',
            'message',
        ]
        widgets = {
            'gender': forms.RadioSelect,
            'dob' : forms.DateInput(attrs={'type': 'date'}),
            'country': forms.Select,
            'message': forms.Textarea(attrs={'rows': 5}),
        }

