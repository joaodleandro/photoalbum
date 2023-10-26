import os
from django.test import TestCase
from django.urls import reverse
from .models import Photo
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage

# Create your tests here.
class PhotoTestCase(TestCase):

    def setUp(self):
        TESTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../tests')
        image_path = os.path.join(TESTS_DIR, 'image.jpg')

        # Creates an object that's backed by Django to create archives to test
        self.image = SimpleUploadedFile(image_path, b"file_content")
        self.photo = Photo.objects.create(image=self.image)

    def test_index_view(self):
        # self.cliet is a Django test instance to make http req | reverse to get the name of view base on url
        response = self.client.get(reverse('index'))
        # if "website" opens and contains image url
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.photo.image.url)

    def test_upload_image_view(self):
        TESTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../tests')
        image_path = os.path.join(TESTS_DIR, 'temp_image.jpg')

        upload_url = reverse('upload')
        response = self.client.get(upload_url)
        self.assertEqual(response.status_code, 200)

        # open the image and reads content to create the django object to test
        with open(image_path, 'rb') as temp_image_file:
            temp_image = SimpleUploadedFile(image_path, temp_image_file.read())
        
        response = self.client.post(upload_url, {'image': temp_image})
        # if redirected sucess
        self.assertEqual(response.status_code, 302) 

    def test_confirm_delete_view(self):
        confirm_delete_url = reverse('confirm_delete', args=[self.photo.pk])
        response = self.client.get(confirm_delete_url)
        self.assertEqual(response.status_code, 200)

    def test_confirm_delete_view_with_confirmation(self):
        confirm_delete_url = reverse('confirm_delete', args=[self.photo.pk])
        response = self.client.post(confirm_delete_url)
        self.assertEqual(response.status_code, 302)

        # If was excluded from db
        with self.assertRaises(Photo.DoesNotExist):
            Photo.objects.get(pk=self.photo.pk)

        # If excluded from storage
        self.assertFalse(default_storage.exists(self.photo.image.path))

    def test_view_image_view(self):
        view_image_url = reverse('view_image', args=[self.photo.pk])
        response = self.client.get(view_image_url)
        self.assertEqual(response.status_code, 200)

    def test_update_image_view(self):
        TESTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../tests')
        image_path = os.path.join(TESTS_DIR, 'temp_updated_image.jpg')

        update_image_url = reverse('update_image', args=[self.photo.pk])
        response = self.client.get(update_image_url)
        self.assertEqual(response.status_code, 200)

        with open(image_path, 'rb') as temp_updated_image_file:
            temp_updated_image = SimpleUploadedFile(image_path, temp_updated_image_file.read())
        
        response = self.client.post(update_image_url, {'image': temp_updated_image})
        self.assertEqual(response.status_code, 302)
