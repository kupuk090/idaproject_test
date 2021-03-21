from django import forms
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile

from io import BytesIO
from os import path
import requests


class UploadImageForm(forms.Form):
    image_url = forms.URLField(required=False)
    image = forms.ImageField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        url = cleaned_data.pop('image_url')
        image = cleaned_data.pop('image')

        if url and image or not (url or image):
            raise ValidationError("Выберите только один из вариантов загрузки изображения")
        if url:
            img = BytesIO()
            resp = requests.get(url, stream=True).content
            img.write(resp)
            
            fragment_removed = url.split("#")[0]
            query_string_removed = fragment_removed.split("?")[0]
            scheme_removed = query_string_removed.split("://")[-1].split(":")[-1]
            cleaned_data['image'] = InMemoryUploadedFile(img, 'image', path.basename(scheme_removed), None, len(resp), None, None)
        if image:
            cleaned_data['image'] = image
        cleaned_data['name'] = cleaned_data['image'].name

        return cleaned_data
        
        
class ResizeImageForm(forms.Form):
    width = forms.IntegerField(min_value=1, required=False)
    height = forms.IntegerField(min_value=1, required=False)

    def clean(self):
        cleaned_data = super().clean()
        width = cleaned_data.get('width')
        height = cleaned_data.get('height')

        if not (width or height):
            raise ValidationError("Размеры изображения не были заданы")

        return cleaned_data