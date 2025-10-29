"""
Text extraction utilities for various text orientations and types
"""
import cv2
import numpy as np
import pytesseract
import easyocr
from PIL import Image
import os
from django.conf import settings


class TextExtractor:
    """Class for extracting text from images with different orientations"""
    
    def __init__(self):
        # Set tesseract path for Windows
        if hasattr(settings, 'TESSERACT_CMD'):
            pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD
        
        # Initialize EasyOCR reader
        self.easyocr_reader = easyocr.Reader(['en'])
    
    def preprocess_image(self, image_path):
        """Preprocess image for better OCR results"""
        # Read image
        img = cv2.imread(image_path)
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply denoising
        denoised = cv2.fastNlMeansDenoising(gray)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        return thresh
    
    def extract_horizontal_text(self, image_path):
        """Extract horizontal text using Tesseract"""
        try:
            # Preprocess image
            processed_img = self.preprocess_image(image_path)
            
            # Extract text with different configurations
            configs = [
                '--psm 6',  # Uniform block of text
                '--psm 3',  # Fully automatic page segmentation
                '--psm 4',  # Assume a single column of text
            ]
            
            all_text = []
            for config in configs:
                text = pytesseract.image_to_string(processed_img, config=config)
                if text.strip():
                    all_text.append(text.strip())
            
            return ' '.join(all_text)
        except Exception as e:
            print(f"Error in horizontal text extraction: {e}")
            return ""
    
    def extract_vertical_text(self, image_path):
        """Extract vertical text by rotating image"""
        try:
            # Read and preprocess image
            img = cv2.imread(image_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Try different rotations
            rotations = [90, 180, 270]
            all_text = []
            
            for angle in rotations:
                # Rotate image
                (h, w) = gray.shape[:2]
                center = (w // 2, h // 2)
                M = cv2.getRotationMatrix2D(center, angle, 1.0)
                rotated = cv2.warpAffine(gray, M, (w, h))
                
                # Extract text
                text = pytesseract.image_to_string(rotated, config='--psm 6')
                if text.strip():
                    all_text.append(text.strip())
            
            return ' '.join(all_text)
        except Exception as e:
            print(f"Error in vertical text extraction: {e}")
            return ""
    
    def extract_embossed_text(self, image_path):
        """Extract embossed/raised text using morphological operations"""
        try:
            # Read image
            img = cv2.imread(image_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Apply morphological operations to enhance embossed text
            kernel = np.ones((3,3), np.uint8)
            
            # Top hat operation to find bright regions
            tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, kernel)
            
            # Black hat operation to find dark regions
            blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, kernel)
            
            # Combine both
            enhanced = cv2.add(gray, tophat)
            enhanced = cv2.subtract(enhanced, blackhat)
            
            # Apply threshold
            _, thresh = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Extract text
            text = pytesseract.image_to_string(thresh, config='--psm 6')
            
            return text.strip()
        except Exception as e:
            print(f"Error in embossed text extraction: {e}")
            return ""
    
    def extract_text_easyocr(self, image_path):
        """Extract text using EasyOCR for better accuracy"""
        try:
            results = self.easyocr_reader.readtext(image_path)
            text_parts = []
            
            for (bbox, text, confidence) in results:
                if confidence > 0.5:  # Filter low confidence results
                    text_parts.append(text)
            
            return ' '.join(text_parts)
        except Exception as e:
            print(f"Error in EasyOCR text extraction: {e}")
            return ""
    
    def extract_all_text(self, image_path):
        """Extract all types of text from image"""
        results = {
            'horizontal_text': self.extract_horizontal_text(image_path),
            'vertical_text': self.extract_vertical_text(image_path),
            'embossed_text': self.extract_embossed_text(image_path),
            'easyocr_text': self.extract_text_easyocr(image_path),
        }
        
        # Combine all text
        all_text = []
        for text_type, text in results.items():
            if text.strip():
                all_text.append(text.strip())
        
        results['combined_text'] = ' '.join(all_text)
        return results
