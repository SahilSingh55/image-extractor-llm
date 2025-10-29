"""
Tests for image processing application
"""
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
import json
import os
from PIL import Image
import tempfile


class ImageProcessingTestCase(TestCase):
    """Test cases for image processing functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.test_image_path = self.create_test_image()
    
    def create_test_image(self):
        """Create a test image for testing"""
        # Create a simple test image
        img = Image.new('RGB', (100, 100), color='white')
        
        # Save to temporary file
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        img.save(temp_file.name, 'JPEG')
        return temp_file.name
    
    def tearDown(self):
        """Clean up test data"""
        if os.path.exists(self.test_image_path):
            os.unlink(self.test_image_path)
    
    def test_home_page_loads(self):
        """Test that home page loads successfully"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Image Text Extractor')
    
    def test_process_image_api(self):
        """Test image processing API"""
        with open(self.test_image_path, 'rb') as img_file:
            response = self.client.post('/api/process-image/', {
                'image': img_file
            })
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertIn('image_id', data)
    
    def test_process_image_api_no_file(self):
        """Test image processing API without file"""
        response = self.client.post('/api/process-image/', {})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn('error', data)
    
    def test_extract_attributes_api(self):
        """Test attribute extraction API"""
        data = {
            'title': 'Test Product',
            'description': 'A test product for testing purposes'
        }
        
        response = self.client.post(
            '/api/extract-attributes/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertIn('attributes', data)
    
    def test_extract_attributes_api_invalid_json(self):
        """Test attribute extraction API with invalid JSON"""
        response = self.client.post(
            '/api/extract-attributes/',
            data='invalid json',
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn('error', data)
    
    def test_get_history_api(self):
        """Test get history API"""
        response = self.client.get('/api/history/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertIn('history', data)
    
    def test_text_extractor_import(self):
        """Test that text extractor can be imported"""
        try:
            from image_processing.text_extractor import TextExtractor
            extractor = TextExtractor()
            self.assertIsNotNone(extractor)
        except ImportError as e:
            self.fail(f"Failed to import TextExtractor: {e}")
    
    def test_background_remover_import(self):
        """Test that background remover can be imported"""
        try:
            from image_processing.background_remover import BackgroundRemover
            remover = BackgroundRemover()
            self.assertIsNotNone(remover)
        except ImportError as e:
            self.fail(f"Failed to import BackgroundRemover: {e}")
    
    def test_attribute_extractor_import(self):
        """Test that attribute extractor can be imported"""
        try:
            from image_processing.attribute_extractor import ProductAttributeExtractor
            extractor = ProductAttributeExtractor()
            self.assertIsNotNone(extractor)
        except ImportError as e:
            self.fail(f"Failed to import ProductAttributeExtractor: {e}")


class TextExtractorTestCase(TestCase):
    """Test cases for text extraction functionality"""
    
    def setUp(self):
        """Set up test data"""
        from image_processing.text_extractor import TextExtractor
        self.extractor = TextExtractor()
    
    def test_extract_basic_attributes(self):
        """Test basic attribute extraction"""
        from image_processing.attribute_extractor import ProductAttributeExtractor
        extractor = ProductAttributeExtractor()
        
        test_text = "Red T-Shirt $29.99 Size: M 100% Cotton Brand: Nike"
        attributes = extractor.extract_basic_attributes(test_text)
        
        self.assertIn('price', attributes)
        self.assertIn('colors', attributes)
        self.assertIn('materials', attributes)
        self.assertIn('brand', attributes)
    
    def test_extract_ml_attributes(self):
        """Test ML-based attribute extraction"""
        from image_processing.attribute_extractor import ProductAttributeExtractor
        extractor = ProductAttributeExtractor()
        
        test_text = "This is a high-quality electronic device with advanced features"
        attributes = extractor.extract_ml_attributes(test_text)
        
        # Should have some attributes extracted
        self.assertIsInstance(attributes, dict)
