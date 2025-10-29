"""
Views for image processing and attribute extraction
"""
import os
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from .models import ProcessedImage
from .text_extractor import TextExtractor
from .background_remover import BackgroundRemover
from .attribute_extractor import ProductAttributeExtractor
import logging

logger = logging.getLogger(__name__)


def home(request):
    """Home page with image upload interface"""
    return render(request, 'image_processing/home.html')


@csrf_exempt
def process_image_api(request):
    """API endpoint for processing images"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)
    
    try:
        # Check if image file is provided
        if 'image' not in request.FILES:
            return JsonResponse({'error': 'No image file provided'}, status=400)
        
        image_file = request.FILES['image']
        
        # Validate file type
        allowed_types = ['image/jpeg', 'image/png', 'image/jpg', 'image/gif', 'image/bmp']
        if image_file.content_type not in allowed_types:
            return JsonResponse({'error': 'Invalid file type. Only images are allowed.'}, status=400)
        
        # Save original image
        processed_image = ProcessedImage(original_image=image_file)
        processed_image.save()
        
        # Get file path
        image_path = processed_image.original_image.path
        
        # Initialize extractors
        text_extractor = TextExtractor()
        background_remover = BackgroundRemover()
        
        # Extract text from image
        logger.info("Starting text extraction...")
        text_results = text_extractor.extract_all_text(image_path)
        
        # Remove background
        logger.info("Starting background removal...")
        processed_image_path = background_remover.remove_background(image_path)
        
        # Update processed image
        if processed_image_path and os.path.exists(processed_image_path):
            with open(processed_image_path, 'rb') as f:
                processed_image.processed_image.save(
                    os.path.basename(processed_image_path),
                    ContentFile(f.read()),
                    save=True
                )
        
        # Save extracted text
        processed_image.extracted_text = text_results.get('combined_text', '')
        processed_image.save()
        
        # Prepare response
        response_data = {
            'success': True,
            'image_id': processed_image.id,
            'extracted_text': text_results,
            'processed_image_url': processed_image.processed_image.url if processed_image.processed_image else None,
            'original_image_url': processed_image.original_image.url
        }
        
        return JsonResponse(response_data)
        
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        return JsonResponse({'error': f'Error processing image: {str(e)}'}, status=500)


@csrf_exempt
def extract_attributes_api(request):
    """API endpoint for extracting product attributes"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        
        # Get parameters
        title = data.get('title', '')
        description = data.get('description', '')
        image_id = data.get('image_id')
        image_path = None
        
        # Get image path if image_id is provided
        if image_id:
            try:
                processed_image = ProcessedImage.objects.get(id=image_id)
                image_path = processed_image.original_image.path
                # Use extracted text if available
                if processed_image.extracted_text:
                    description = f"{description} {processed_image.extracted_text}".strip()
            except ProcessedImage.DoesNotExist:
                return JsonResponse({'error': 'Image not found'}, status=404)
        
        # Initialize attribute extractor
        attribute_extractor = ProductAttributeExtractor()
        
        # Extract attributes
        logger.info("Starting attribute extraction...")
        attributes = attribute_extractor.extract_all_attributes(
            title=title,
            description=description,
            image_path=image_path
        )
        
        # Update processed image if image_id is provided
        if image_id:
            processed_image.product_attributes = attributes
            processed_image.save()
        
        # Prepare response
        response_data = {
            'success': True,
            'attributes': attributes,
            'image_id': image_id
        }
        
        return JsonResponse(response_data)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        logger.error(f"Error extracting attributes: {str(e)}")
        return JsonResponse({'error': f'Error extracting attributes: {str(e)}'}, status=500)


def get_processing_history(request):
    """API endpoint for getting processing history"""
    try:
        # Get all processed images
        processed_images = ProcessedImage.objects.all()[:50]  # Limit to last 50
        
        history = []
        for img in processed_images:
            history.append({
                'id': img.id,
                'original_image_url': img.original_image.url,
                'processed_image_url': img.processed_image.url if img.processed_image else None,
                'extracted_text': img.extracted_text,
                'product_attributes': img.product_attributes,
                'created_at': img.created_at.isoformat()
            })
        
        return JsonResponse({'success': True, 'history': history})
        
    except Exception as e:
        logger.error(f"Error getting processing history: {str(e)}")
        return JsonResponse({'error': f'Error getting processing history: {str(e)}'}, status=500)
