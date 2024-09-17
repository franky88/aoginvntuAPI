from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile

def resize_image_to_square(image, size):
    img = Image.open(image)
    width, height = img.size
    min_dimension = min(width, height)
    left = (width - min_dimension) / 2
    top = (height - min_dimension) / 2
    right = (width + min_dimension) / 2
    bottom = (height + min_dimension) / 2
    img_cropped = img.crop((left, top, right, bottom))
    img_resized = img_cropped.resize((size, size), Image.LANCZOS)
    img_io = BytesIO()
    img_resized.save(img_io, format='JPEG')
    img_name = image.name
    img_file = ContentFile(img_io.getvalue(), img_name)
    
    return img_file
