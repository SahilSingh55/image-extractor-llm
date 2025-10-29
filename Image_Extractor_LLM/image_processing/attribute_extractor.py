"""
ML/LLM based product attribute extraction
"""
import json
import re
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import Dict, List, Any


class ProductAttributeExtractor:
    """Class for extracting product attributes using ML/LLM models"""
    
    def __init__(self):
        # Initialize text classification pipeline for product categorization
        self.classifier = pipeline(
            "text-classification",
            model="microsoft/DialoGPT-medium",
            return_all_scores=True
        )
        
        # Initialize tokenizer for text processing
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
    
    def extract_basic_attributes(self, text: str) -> Dict[str, Any]:
        """Extract basic attributes using regex patterns"""
        attributes = {}
        
        # Extract price information
        price_patterns = [
            r'\$[\d,]+\.?\d*',
            r'USD\s*[\d,]+\.?\d*',
            r'Price:\s*[\d,]+\.?\d*',
            r'Cost:\s*[\d,]+\.?\d*'
        ]
        
        prices = []
        for pattern in price_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            prices.extend(matches)
        
        if prices:
            attributes['price'] = prices[0]
        
        # Extract dimensions
        dimension_patterns = [
            r'(\d+(?:\.\d+)?)\s*x\s*(\d+(?:\.\d+)?)\s*x\s*(\d+(?:\.\d+)?)',
            r'(\d+(?:\.\d+)?)\s*cm\s*x\s*(\d+(?:\.\d+)?)\s*cm',
            r'(\d+(?:\.\d+)?)\s*inch\s*x\s*(\d+(?:\.\d+)?)\s*inch',
            r'Size:\s*(\d+(?:\.\d+)?)\s*x\s*(\d+(?:\.\d+)?)'
        ]
        
        dimensions = []
        for pattern in dimension_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            dimensions.extend(matches)
        
        if dimensions:
            attributes['dimensions'] = dimensions[0]
        
        # Extract weight
        weight_patterns = [
            r'(\d+(?:\.\d+)?)\s*kg',
            r'(\d+(?:\.\d+)?)\s*lb',
            r'Weight:\s*(\d+(?:\.\d+)?)\s*kg',
            r'Weight:\s*(\d+(?:\.\d+)?)\s*lb'
        ]
        
        weights = []
        for pattern in weight_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            weights.extend(matches)
        
        if weights:
            attributes['weight'] = weights[0]
        
        # Extract color information
        color_keywords = [
            'red', 'blue', 'green', 'yellow', 'black', 'white', 'gray', 'grey',
            'brown', 'purple', 'pink', 'orange', 'silver', 'gold', 'bronze'
        ]
        
        colors = []
        for color in color_keywords:
            if re.search(rf'\b{color}\b', text, re.IGNORECASE):
                colors.append(color)
        
        if colors:
            attributes['colors'] = colors
        
        # Extract material information
        material_keywords = [
            'wood', 'metal', 'plastic', 'glass', 'fabric', 'leather', 'cotton',
            'steel', 'aluminum', 'ceramic', 'rubber', 'silk', 'wool', 'nylon'
        ]
        
        materials = []
        for material in material_keywords:
            if re.search(rf'\b{material}\b', text, re.IGNORECASE):
                materials.append(material)
        
        if materials:
            attributes['materials'] = materials
        
        # Extract brand information
        brand_patterns = [
            r'Brand:\s*([A-Za-z0-9\s]+)',
            r'Manufacturer:\s*([A-Za-z0-9\s]+)',
            r'Made by:\s*([A-Za-z0-9\s]+)'
        ]
        
        brands = []
        for pattern in brand_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            brands.extend(matches)
        
        if brands:
            attributes['brand'] = brands[0].strip()
        
        return attributes
    
    def extract_ml_attributes(self, text: str) -> Dict[str, Any]:
        """Extract attributes using ML models"""
        attributes = {}
        
        try:
            # Categorize the product
            categories = self.classifier(text)
            if categories:
                attributes['category'] = categories[0]['label']
                attributes['category_confidence'] = categories[0]['score']
            
            # Extract key phrases using simple NLP
            words = text.lower().split()
            
            # Count frequency of important words
            word_freq = {}
            for word in words:
                if len(word) > 3:  # Only consider words longer than 3 characters
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            # Get most frequent words as keywords
            keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
            attributes['keywords'] = [word for word, freq in keywords]
            
        except Exception as e:
            print(f"Error in ML attribute extraction: {e}")
        
        return attributes
    
    def extract_advanced_attributes(self, text: str, image_path: str = None) -> Dict[str, Any]:
        """Extract advanced attributes using more sophisticated methods"""
        attributes = {}
        
        # Extract product features
        feature_keywords = [
            'waterproof', 'durable', 'lightweight', 'portable', 'adjustable',
            'rechargeable', 'wireless', 'bluetooth', 'wifi', 'usb', 'hdmi',
            'touchscreen', 'backlit', 'ergonomic', 'antimicrobial', 'stainless'
        ]
        
        features = []
        for feature in feature_keywords:
            if re.search(rf'\b{feature}\b', text, re.IGNORECASE):
                features.append(feature)
        
        if features:
            attributes['features'] = features
        
        # Extract technical specifications
        tech_specs = {}
        
        # Extract resolution
        resolution_patterns = [
            r'(\d+)\s*x\s*(\d+)\s*pixels',
            r'(\d+)\s*x\s*(\d+)\s*resolution',
            r'(\d+)\s*MP',
            r'(\d+)\s*megapixel'
        ]
        
        for pattern in resolution_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                tech_specs['resolution'] = match.group(0)
                break
        
        # Extract storage capacity
        storage_patterns = [
            r'(\d+)\s*GB',
            r'(\d+)\s*TB',
            r'(\d+)\s*MB',
            r'Storage:\s*(\d+)\s*GB'
        ]
        
        for pattern in storage_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                tech_specs['storage'] = match.group(0)
                break
        
        if tech_specs:
            attributes['technical_specifications'] = tech_specs
        
        return attributes
    
    def extract_all_attributes(self, title: str = "", description: str = "", image_path: str = None) -> Dict[str, Any]:
        """Extract all possible product attributes"""
        # Combine title and description
        combined_text = f"{title} {description}".strip()
        
        if not combined_text:
            return {}
        
        # Extract different types of attributes
        basic_attrs = self.extract_basic_attributes(combined_text)
        ml_attrs = self.extract_ml_attributes(combined_text)
        advanced_attrs = self.extract_advanced_attributes(combined_text, image_path)
        
        # Combine all attributes
        all_attributes = {
            **basic_attrs,
            **ml_attrs,
            **advanced_attrs
        }
        
        # Add metadata
        all_attributes['extraction_metadata'] = {
            'text_length': len(combined_text),
            'has_title': bool(title.strip()),
            'has_description': bool(description.strip()),
            'has_image': bool(image_path)
        }
        
        return all_attributes
