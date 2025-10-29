from django.contrib import admin
from .models import ProcessedImage


@admin.register(ProcessedImage)
class ProcessedImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'original_image', 'created_at', 'has_extracted_text', 'has_attributes']
    list_filter = ['created_at']
    search_fields = ['extracted_text']
    readonly_fields = ['created_at']
    
    def has_extracted_text(self, obj):
        return bool(obj.extracted_text)
    has_extracted_text.boolean = True
    has_extracted_text.short_description = 'Has Text'
    
    def has_attributes(self, obj):
        return bool(obj.product_attributes)
    has_attributes.boolean = True
    has_attributes.short_description = 'Has Attributes'
