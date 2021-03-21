from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from PIL import Image as PILImage
import base64
from io import BytesIO

from .forms import UploadImageForm, ResizeImageForm
from .models import Image


def mainpage(request: HttpRequest) -> HttpResponse:
    return render(request, template_name='resizer/mainpage.html', context={'images': Image.objects.all()})


def upload_file(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            new_img = Image.objects.create(name=form.cleaned_data['name'], image=form.cleaned_data['image'])
            new_img.save()
            return redirect('resize_image', new_img.id)
    else:
        form = UploadImageForm()
    return render(request, template_name='resizer/file_upload.html', context={'form': form})


def resize_image(request: HttpRequest, image_id: int) -> HttpResponse:
    try:
        img = Image.objects.get(id=image_id)
    except Image.DoesNotExist:
        return redirect('home')

    if request.method == 'POST':
        form = ResizeImageForm(request.POST)
        if form.is_valid():
            new_img = PILImage.open(img.image)
            h = form.cleaned_data['height']
            w = form.cleaned_data['width']
            if h and w:
                # пытаемся сохранить пропорции и выбираем более близкую к исходной величину, относительно которой будем изменять размеры
                if abs(h - new_img.height) < abs(w - new_img.width):
                    new_img = new_img.resize((int(h / new_img.height * new_img.width), h))
                else:
                    new_img = new_img.resize((w, int(w / new_img.width * new_img.height)))
            elif h:
                new_img = new_img.resize((int(h / new_img.height * new_img.width), h))
            elif w:
                new_img = new_img.resize((w, int(w / new_img.width * new_img.height)))

            buffer = BytesIO()
            new_img.save(buffer, "PNG")
            img_str = base64.b64encode(buffer.getvalue()).decode()
            return render(request, template_name='resizer/resize_image.html', context={'form': form, 'image': img, 'new_image': img_str})
    else:
        form = ResizeImageForm()
    return render(request, template_name='resizer/resize_image.html', context={'form': form, 'image': img})