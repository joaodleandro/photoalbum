from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.files.base import ContentFile
from myapp.models import Photo
from .serializers import PhotoSerializer
from rest_framework import status
import base64
from rest_framework.exceptions import ParseError

@api_view(['GET'])
def get_photos(request):
    photos = Photo.objects.all()
    serializer = PhotoSerializer(photos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_photo(request, pk):
    try:
        photo = Photo.objects.get(pk=pk)
    except Photo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PhotoSerializer(photo)
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_photo(request, pk):
    try:
        photo = Photo.objects.get(pk=pk)
    except Photo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    photo.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

