"""
OCR Service using Google Cloud Vision API
Extracts text from images, especially math calculations and numbers
"""

import os
import io
import asyncio
from typing import Optional, Tuple
from PIL import Image
import tempfile
import aiofiles

from config import Config

# Try to import Google Cloud Vision - make it optional
try:
    from google.cloud import vision
    GOOGLE_VISION_AVAILABLE = True
except ImportError:
    GOOGLE_VISION_AVAILABLE = False
    vision = None

class OCRService:
    def __init__(self):
        """Initialize OCR service with Google Cloud Vision API"""
        self.client = None
        self.is_enabled = False
        self._setup_client()
    
    def _setup_client(self):
        """Setup Google Cloud Vision client"""
        try:
            # Check if Google Cloud Vision library is available
            if not GOOGLE_VISION_AVAILABLE:
                print("⚠️ Google Cloud Vision library not installed - OCR disabled")
                print("   To enable OCR, install: pip install google-cloud-vision")
                self.is_enabled = False
                return

            # Check if Google Cloud credentials are available
            credentials_path = getattr(Config, 'GOOGLE_CLOUD_CREDENTIALS_PATH', None)

            if credentials_path and os.path.exists(credentials_path):
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
                self.client = vision.ImageAnnotatorClient()
                self.is_enabled = True
                print("✅ Google Cloud Vision OCR enabled")
            else:
                print("⚠️ Google Cloud Vision credentials not found - OCR disabled")
                print("   To enable OCR, set GOOGLE_CLOUD_CREDENTIALS_PATH in your .env file")
                self.is_enabled = False

        except Exception as e:
            print(f"⚠️ Failed to initialize Google Cloud Vision: {e}")
            self.is_enabled = False
    
    async def extract_text_from_image(self, image_data: bytes) -> Tuple[bool, str, str]:
        """
        Extract text from image data
        
        Args:
            image_data: Raw image bytes
            
        Returns:
            Tuple of (success, extracted_text, error_message)
        """
        if not self.is_enabled:
            return False, "", "OCR service is not available. Google Cloud Vision API not configured."
        
        try:
            # Create Vision API image object
            image = vision.Image(content=image_data)
            
            # Perform text detection
            response = self.client.text_detection(image=image)
            
            # Check for errors
            if response.error.message:
                return False, "", f"Vision API error: {response.error.message}"
            
            # Extract text annotations
            texts = response.text_annotations
            
            if not texts:
                return False, "", "No text detected in the image."
            
            # Get the full text (first annotation contains all detected text)
            extracted_text = texts[0].description.strip()
            
            if not extracted_text:
                return False, "", "No readable text found in the image."
            
            return True, extracted_text, ""
            
        except Exception as e:
            return False, "", f"Error processing image: {str(e)}"
    
    async def process_telegram_photo(self, photo_file) -> Tuple[bool, str, str]:
        """
        Process a photo from Telegram and extract text
        
        Args:
            photo_file: Telegram photo file object
            
        Returns:
            Tuple of (success, extracted_text, error_message)
        """
        try:
            # Download the photo to memory
            photo_bytes = await photo_file.download_as_bytearray()
            
            # Extract text from the image
            return await self.extract_text_from_image(bytes(photo_bytes))
            
        except Exception as e:
            return False, "", f"Error downloading or processing photo: {str(e)}"
    
    def is_math_related(self, text: str) -> bool:
        """
        Check if extracted text contains math-related content
        
        Args:
            text: Extracted text from image
            
        Returns:
            True if text appears to contain math content
        """
        # Math indicators
        math_indicators = [
            '+', '-', '*', '/', '=', '×', '÷', '^', '²', '³',
            'sin', 'cos', 'tan', 'log', 'ln', 'sqrt', 'exp',
            'π', 'pi', 'e', '∫', '∑', '∆', '∂',
            'solve', 'calculate', 'find', 'x', 'y', 'f(x)',
            '(', ')', '[', ']', '{', '}',
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
        ]
        
        text_lower = text.lower()
        
        # Check if text contains math indicators
        math_count = sum(1 for indicator in math_indicators if indicator in text_lower)
        
        # If more than 2 math indicators found, likely math content
        return math_count >= 2
    
    def clean_math_text(self, text: str) -> str:
        """
        Clean and format extracted text for math processing
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned text suitable for math processing
        """
        # Remove extra whitespace and newlines
        cleaned = ' '.join(text.split())
        
        # Common OCR corrections for math symbols
        replacements = {
            'x': '*',  # Only replace standalone x that might be multiplication
            '×': '*',
            '÷': '/',
            '−': '-',  # Unicode minus to ASCII minus
            '–': '-',  # En dash to minus
            '—': '-',  # Em dash to minus
            '²': '^2',
            '³': '^3',
            'π': 'pi',
            '∞': 'infinity',
        }
        
        # Apply replacements carefully
        for old, new in replacements.items():
            if old in cleaned:
                cleaned = cleaned.replace(old, new)
        
        return cleaned.strip()

# Global OCR service instance
ocr_service = OCRService()
