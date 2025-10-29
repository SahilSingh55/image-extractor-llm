"""
Background removal utilities using AI models
"""
import os
import numpy as np
from PIL import Image
import cv2
from rembg import remove, new_session
import torch


class BackgroundRemover:
    """Class for removing backgrounds from images using AI models"""
    
    def __init__(self):
        # Initialize rembg session with different models
        self.models = {
            'u2net': new_session('u2net'),
            'u2netp': new_session('u2netp'),
            'u2net_human_seg': new_session('u2net_human_seg'),
            'u2net_cloth_seg': new_session('u2net_cloth_seg'),
        }
    
    def remove_background_rembg(self, image_path, model_name='u2net'):
        """Remove background using rembg library"""
        try:
            # Load image
            with open(image_path, 'rb') as input_file:
                input_data = input_file.read()
            
            # Remove background
            output_data = remove(input_data, session=self.models[model_name])
            
            # Save result
            output_path = image_path.replace('.', '_no_bg.')
            with open(output_path, 'wb') as output_file:
                output_file.write(output_data)
            
            return output_path
        except Exception as e:
            print(f"Error in background removal: {e}")
            return None
    
    def remove_background_opencv(self, image_path):
        """Remove background using OpenCV techniques"""
        try:
            # Read image
            img = cv2.imread(image_path)
            original = img.copy()
            
            # Convert to HSV
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            
            # Create mask for background (assuming white/light background)
            lower_white = np.array([0, 0, 200])
            upper_white = np.array([180, 30, 255])
            mask = cv2.inRange(hsv, lower_white, upper_white)
            
            # Invert mask
            mask_inv = cv2.bitwise_not(mask)
            
            # Apply mask
            result = cv2.bitwise_and(original, original, mask=mask_inv)
            
            # Save result
            output_path = image_path.replace('.', '_no_bg_opencv.')
            cv2.imwrite(output_path, result)
            
            return output_path
        except Exception as e:
            print(f"Error in OpenCV background removal: {e}")
            return None
    
    def remove_background_grabcut(self, image_path):
        """Remove background using GrabCut algorithm"""
        try:
            # Read image
            img = cv2.imread(image_path)
            height, width = img.shape[:2]
            
            # Initialize mask
            mask = np.zeros((height, width), np.uint8)
            
            # Define rectangle (assuming object is in center)
            rect = (50, 50, width-100, height-100)
            
            # Initialize background and foreground models
            bgd_model = np.zeros((1, 65), np.float64)
            fgd_model = np.zeros((1, 65), np.float64)
            
            # Apply GrabCut
            cv2.grabCut(img, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
            
            # Create final mask
            mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
            
            # Apply mask
            result = img * mask2[:, :, np.newaxis]
            
            # Save result
            output_path = image_path.replace('.', '_no_bg_grabcut.')
            cv2.imwrite(output_path, result)
            
            return output_path
        except Exception as e:
            print(f"Error in GrabCut background removal: {e}")
            return None
    
    def remove_background(self, image_path, method='rembg'):
        """Remove background using specified method"""
        if method == 'rembg':
            return self.remove_background_rembg(image_path)
        elif method == 'opencv':
            return self.remove_background_opencv(image_path)
        elif method == 'grabcut':
            return self.remove_background_grabcut(image_path)
        else:
            # Try all methods and return the best result
            results = []
            for method_name in ['rembg', 'opencv', 'grabcut']:
                result = self.remove_background(image_path, method_name)
                if result:
                    results.append(result)
            return results[0] if results else None
