from django import forms


class ContactForm(forms.Form):
    """
    Form for sending vacancies or contact information.

    Has fields:
    - name: character field maximum characters 100 (optional)
    - email: field email (optional)
    - phone: character field maximum characters 16 (optional)
    - message: character field (optional)
    - file: field file (optional)

    Validation:
    - Checks if one field is from phone, message, file, if not then returns ValidationError.
    """
    name = forms.CharField(required=False, label="Name", max_length=100, widget=forms.TextInput())
    email = forms.EmailField(required=False, label="Email", widget=forms.EmailInput())
    phone = forms.CharField(required=False, label="Phone", max_length=16, widget=forms.TextInput())
    message = forms.CharField(required=False, label="Message", widget=forms.Textarea())
    file = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={"class": "file-input", "id": "vacancy-file"}))

    def clean(self):
        """Checks if one field is from phone, message, file, if not then returns ValidationError."""
        cleaned_data = super().clean()
        phone = cleaned_data.get("phone")
        message = cleaned_data.get("message")
        file = cleaned_data.get("file")

        if not (phone or message or file):
            raise forms.ValidationError("Send at least your phone number or a message or a file")