# chatbot
 🤖 The Q&A Chatbot 

 

A document-based question-answering chatbot built with Streamlit and powered by advanced NLP models. Upload documents in various formats (PDF, Word, PowerPoint, Excel, images, text files) and ask questions to get answers. 

 

 🚀 Features 

 

Multi-Format Document Support 

- PDF Documents - Text extraction using PyMuPDF 

- Word Documents - Support for `.doc` and `.docx` files 

- PowerPoint Presentations - Extract text from `.ppt` and `.pptx` slides 

- Excel Spreadsheets - Process data from `.xls` and `.xlsx` files 

- Images - OCR text extraction from `.png`, `.jpg`, `.jpeg`, `.bmp`, `.tiff` 

- Text Files - Direct processing of `.txt` and `.csv` files 

 

  Capabilities 

- Semantic Search - Uses SentenceTransformers for intelligent document retrieval 

- Context-Aware Q&A - Powered by Google's FLAN-T5-XL model 

- Cosine Similarity Matching - Finds most relevant document sections 

- Token Management - Efficient text chunking with tiktoken 

 

 Document Processing 

- PyMuPDF (fitz) - Advanced PDF text extraction 

- python-docx - Microsoft Word document processing 

- python-pptx - PowerPoint presentation handling 

- Pandas - Excel file processing and data manipulation 

- Pytesseract - OCR for image text extraction 

- Pillow (PIL) - Image processing and manipulation 

 

 Web Framework & UI 

- Streamlit - Interactive web application framework 

- Custom CSS - Responsive chat-style interface design 

 

 Utilities 

- tiktoken - OpenAI's tokenizer for text chunking 

- OS Operations - File handling and path management 

 

 📦 Installation & Setup 

 

 Prerequisites 

- Python 3.8 or higher 

- Tesseract OCR (for image text extraction) 

 

 Installation Steps 

 

1. Clone the repository 

   ```bash 

   git clone <repository-url> 

   cd qa-chatbot 

   ``` 

 

2. Install dependencies 

   ```bash 

   pip install -r requirements.txt 

   ``` 

 

3. Install Tesseract OCR (for image processing) 

   - Windows: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki) 

   - macOS: `brew install tesseract` 

   - Ubuntu: `sudo apt install tesseract-ocr` 

 

4. Run the application 

   ```bash 

   streamlit run main.py 

   ``` 

 

5. Open your browser to `http://localhost:8501` 

 

how to Use 

 Step 1: Upload Documents 

- Click "Choose files" to upload one or multiple documents 

- Supported formats: PDF, Word, PowerPoint, Excel, Images, Text files 

- Wait for processing confirmation 

 

 Step 2: Start Asking Questions 

- Type your question in the chat input 

- The AI will search through your uploaded documents 

- Get contextually relevant answers based on document content 

 

 Step 3: Continue the Conversation 

- Ask follow-up questions 

- Reference previous answers in the chat history 

- Upload additional documents as needed 

 

 Key Components 
  main.py 

- Streamlit Interface - Chat UI and file upload handling 

- Model Loading - FLAN-T5-XL and SentenceTransformer initialization 

- Question Processing - Semantic search and answer generation 

- Session Management - Chat history and state persistence 

 

 file_utils.py 

- Multi-format Support - Unified text extraction interface 

- Error Handling - Robust processing with fallback mechanisms 

- Modular Design - Separate functions for each file type 

 

 🎨 Features Deep Dive 

 

 Intelligent Document Processing 

```python 

 Automatic format detection and processing 

def extract_text(file_path): 

    ext = os.path.splitext(file_path)[1].lower() 

     Route to appropriate extraction function 

``` 

 

 Advanced Semantic Search 

```python 

 Find most relevant document chunks 

similarity_scores = cosine_similarity([question_embedding], chunk_embeddings) 

best_chunks = get_top_k_chunks(similarity_scores) 

``` 

 

 Context-Aware Answer Generation 

python 

 Generate answers using document context 

prompt = f"Context: {context}\nQuestion: {question}\nAnswer:" 

answer = qa_pipeline(prompt) 

 Performance Optimizations 

  Model Caching - `@st.cache_resource` for efficient model loading 

- Chunked Processing - Smart text segmentation for large documents 

- Memory Management - Efficient embedding storage and retrieval 

- Lazy Loading - On-demand model initialization 

 

  Error Handling & Reliability 

- Format Validation - Comprehensive file type checking 

- Graceful Degradation - Fallback mechanisms for processing failures 

- User Feedback - Clear error messages and processing status 

- Exception Safety - Robust error catching throughout the pipeline 

 

  System Requirements 

  Minimum Requirements 

- RAM: 8GB (16GB recommended for large documents) 

- Storage: 2GB free space for models 

- Python: 3.8+ 

- Internet: Required for initial model download 

 

 Supported File Formats 

- Documents: PDF, DOC, DOCX, TXT, CSV 

- Presentations: PPT, PPTX 

- Spreadsheets: XLS, XLSX 

- Images: PNG, JPG, JPEG, BMP, TIFF 

 

 🔮 Future Enhancements 

 

- Multi-language Support - International document processing 

- Advanced OCR - Improved image text extraction 

- Cloud Integration - Support for cloud storage services 

- Batch Processing - Handle multiple documents simultaneously 

- Export Features - Save chat history and answers 

- Custom Models - Integration with domain-specific AI models 

 



 
