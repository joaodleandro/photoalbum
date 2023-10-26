from django.shortcuts import get_object_or_404, redirect, render
from django.core.files.storage import default_storage

from .forms import ImageUploadForm
from .models import Photo

# Create your views here.
def index(request):
    gallery = Photo.objects.all()
    return render(request, 'index.html', {'gallery': gallery}) 

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            Photo = form.save()
            Photo.save()
            return redirect('/')  
    else:
        form = ImageUploadForm()
        return render(request, 'upload_image.html', {'form': form}) 
    
def confirm_delete(request, pk):
    photo = get_object_or_404(Photo, pk=pk)

    if request.method == 'POST':
        default_storage.delete(photo.image.path)
        photo.delete()
        return redirect('/')
    else:
        return render(request, 'confirm_delete.html', {'pk': pk})

def view_image(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    return render(request, 'view_image.html', {'photo': photo})

def update_image(request, pk):
    photo = get_object_or_404(Photo, pk=pk)

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES, instance=photo)
        default_storage.delete(photo.image.path)
        if form.is_valid():
            form.save()
            return redirect('view_image', pk=photo.pk) 
    else:
        form = ImageUploadForm(instance=photo)
        return render(request, 'update_image.html', {'form': form})
    
    