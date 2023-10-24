import os
from django.test import TestCase
from django.urls import reverse
from .models import Photo
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your tests here.
class PhotoTestCase(TestCase):

    def setUp(self):
        TESTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../tests')
        image_path = os.path.join(TESTS_DIR, 'image.jpg')

        self.image = SimpleUploadedFile(image_path, b"file_content")
        self.photo = Photo.objects.create(image=self.image)

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.photo.image.url)

    def test_upload_image_view(self):
        TESTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../tests')
        image_path = os.path.join(TESTS_DIR, 'temp_image.jpg')

        upload_url = reverse('upload')
        response = self.client.get(upload_url)
        self.assertEqual(response.status_code, 200)

        with open(image_path, 'rb') as temp_image_file:
            temp_image = SimpleUploadedFile(image_path, temp_image_file.read())
        
        response = self.client.post(upload_url, {'image': temp_image})
        self.assertEqual(response.status_code, 302) 

    def test_confirm_delete_view(self):
        confirm_delete_url = reverse('confirm_delete', args=[self.photo.pk])
        response = self.client.get(confirm_delete_url)
        self.assertEqual(response.status_code, 200)

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
