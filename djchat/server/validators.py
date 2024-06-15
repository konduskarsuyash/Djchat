from PIL import Image
from rest_framework.exceptions import ValidationError
import os


def validate_icon_image_size(image):
    if image:
        with Image.open(image) as img:
            if img.width>70 or img.height>70:
                raise ValidationError(
                    f"The maximum dimension allowed for image are 70x70 - size of your image is {img.size}"
                )
                
    
def validate_image_file_extension(value):
    ext = os.path.splitext(value.name)[1]            
    valid_extensions = [".png", ".jpg", ".jpeg", ".svg"]
    if not ext.lower() in valid_extensions:
        raise ValidationError(
            f"Image extension must be one of the following: {valid_extensions} But you uploaded {ext}"
        )