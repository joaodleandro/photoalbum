from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages

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
        return render(request, 'upload.html', {'form': form}) 
    
def confirm_delete(request, pk):
    photo = get_object_or_404(Photo, pk=pk)

    if request.method == 'POST':
        photo.delete()
        return redirect('/')
    else:
        return render(request, 'confirm_delete.html', {'pk': pk})