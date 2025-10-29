from django.db import models
from django.utils import timezone


class ProcessedImage(models.Model):
    """Model to store processed image information"""
    original_image = models.ImageField(upload_to='original_images/')
    processed_image = models.ImageField(upload_to='processed_images/', null=True, blank=True)
    extracted_text = models.TextField(blank=True)
    product_attributes = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"ProcessedImage {self.id} - {self.original_image.name}"
