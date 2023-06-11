from django.core.validators import RegexValidator


alphanumeric_with_special_characters = RegexValidator(
    regex=r'^[a-zA-Z0-9\s!@#$%^&*()\[\]_\-=:"\']+',
    message='Only alphanumeric characters, spaces, and specific special characters are allowed.'
)
