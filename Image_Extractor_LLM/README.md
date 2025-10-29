# Image Text Extractor & Product Attribute Analyzer

A comprehensive ML-based automation system for extracting text from images (including vertical, horizontal, and embossed text) and analyzing product attributes using AI/LLM models.

## 🚀 Features

### Text Extraction
- **Horizontal Text**: Extract regular horizontal text using Tesseract OCR
- **Vertical Text**: Extract vertical text by rotating images and applying OCR
- **Embossed Text**: Extract raised/embossed text using morphological operations
- **Multi-language Support**: Uses EasyOCR for better accuracy across languages
- **Image Preprocessing**: Automatic denoising, thresholding, and enhancement

### Background Removal
- **AI-powered Background Removal**: Uses rembg library with multiple models
- **OpenCV Methods**: Alternative background removal using color-based segmentation
- **GrabCut Algorithm**: Advanced background removal using machine learning
- **Multiple Model Support**: u2net, u2netp, u2net_human_seg, u2net_cloth_seg

### Product Attribute Extraction
- **Basic Attributes**: Price, dimensions, weight, color, material, brand
- **ML-based Categorization**: Product categorization using transformer models
- **Advanced Features**: Technical specifications, product features
- **Keyword Extraction**: Automatic keyword extraction from text
- **Confidence Scoring**: Attribute extraction with confidence levels

### Web Interface
- **Drag & Drop Upload**: Easy image upload with drag-and-drop support
- **Real-time Processing**: Live processing status and results display
- **History Management**: View and manage processing history
- **Responsive Design**: Mobile-friendly Bootstrap interface

## 🛠️ Installation

### Prerequisites

1. **Python 3.8+**
2. **Tesseract OCR**
   - **Windows**: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
   - **macOS**: `brew install tesseract`
   - **Linux**: `sudo apt-get install tesseract-ocr`

3. **Git** (for cloning the repository)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd Image_Extractor_LLM
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Django**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser  # Optional: for admin access
   ```

5. **Configure Tesseract path** (if needed)
   - Edit `image_extractor/settings.py`
   - Update `TESSERACT_CMD` with your Tesseract installation path

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Open your browser and go to `http://127.0.0.1:8000`
   - Admin panel: `http://127.0.0.1:8000/admin`

## 📖 Usage

### Web Interface

1. **Upload Image**
   - Drag and drop an image onto the upload area
   - Or click "Choose File" to browse for an image
   - Supported formats: JPEG, PNG, GIF, BMP

2. **View Results**
   - Original and processed images will be displayed
   - Extracted text will be shown in different categories
   - Background removal results will be available

3. **Extract Attributes**
   - Optionally enter product title and description
   - Click "Extract Attributes" to analyze product attributes
   - View extracted attributes like price, dimensions, materials, etc.

4. **View History**
   - Access processing history to view previously processed images
   - Click "Refresh" to update the history list

### API Endpoints

#### Process Image
```http
POST /api/process-image/
Content-Type: multipart/form-data

{
  "image": <image_file>
}
```

**Response:**
```json
{
  "success": true,
  "image_id": 1,
  "extracted_text": {
    "horizontal_text": "...",
    "vertical_text": "...",
    "embossed_text": "...",
    "easyocr_text": "...",
    "combined_text": "..."
  },
  "processed_image_url": "/media/processed_images/...",
  "original_image_url": "/media/original_images/..."
}
```

#### Extract Attributes
```http
POST /api/extract-attributes/
Content-Type: application/json

{
  "title": "Product Title",
  "description": "Product Description",
  "image_id": 1
}
```

**Response:**
```json
{
  "success": true,
  "attributes": {
    "price": "$99.99",
    "dimensions": "10x5x3",
    "weight": "2.5 kg",
    "colors": ["red", "blue"],
    "materials": ["plastic", "metal"],
    "brand": "Example Brand",
    "category": "Electronics",
    "features": ["waterproof", "wireless"],
    "keywords": ["product", "example", "quality"]
  },
  "image_id": 1
}
```

#### Get Processing History
```http
GET /api/history/
```

**Response:**
```json
{
  "success": true,
  "history": [
    {
      "id": 1,
      "original_image_url": "/media/original_images/...",
      "processed_image_url": "/media/processed_images/...",
      "extracted_text": "...",
      "product_attributes": {...},
      "created_at": "2024-01-01T12:00:00Z"
    }
  ]
}
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Tesseract Path (if different from default)
TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe

# Optional: API Keys for external services
OPENAI_API_KEY=your-openai-key
```

### Model Configuration

The system uses several AI models that can be configured:

1. **Text Extraction Models**:
   - Tesseract OCR (configurable via `TESSERACT_CMD`)
   - EasyOCR (automatically downloads models on first use)

2. **Background Removal Models**:
   - u2net (default)
   - u2netp (faster)
   - u2net_human_seg (for human subjects)
   - u2net_cloth_seg (for clothing)

3. **Attribute Extraction Models**:
   - Microsoft DialoGPT (for text classification)
   - Custom regex patterns for attribute extraction

## 📁 Project Structure

```
Image_Extractor_LLM/
├── image_extractor/          # Django project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── image_processing/         # Main application
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   ├── text_extractor.py     # OCR and text extraction
│   ├── background_remover.py # Background removal
│   └── attribute_extractor.py # Product attribute extraction
├── templates/                # HTML templates
│   └── image_processing/
│       └── home.html
├── media/                    # Uploaded files (created automatically)
├── static/                   # Static files (created automatically)
├── requirements.txt          # Python dependencies
├── manage.py                 # Django management script
└── README.md                # This file
```

## 🧪 Testing

### Test the Installation

1. **Start the server**:
   ```bash
   python manage.py runserver
   ```

2. **Test image upload**:
   - Go to `http://127.0.0.1:8000`
   - Upload a test image
   - Verify text extraction and background removal

3. **Test API endpoints**:
   ```bash
   # Test image processing
   curl -X POST -F "image=@test_image.jpg" http://127.0.0.1:8000/api/process-image/
   
   # Test attribute extraction
   curl -X POST -H "Content-Type: application/json" \
        -d '{"title":"Test Product","description":"Test Description"}' \
        http://127.0.0.1:8000/api/extract-attributes/
   ```

### Sample Test Images

For best results, test with images containing:
- Clear, readable text
- Various text orientations
- Different backgrounds
- Product images with labels/descriptions

---

**Ready to use! 🚀**
