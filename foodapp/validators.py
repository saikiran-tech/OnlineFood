import os
from django.core.exceptions import ValidationError

def allowed_image_extensions(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.png', '.jpg', '.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported files! Allowed files are only: ' +str(valid_extensions))