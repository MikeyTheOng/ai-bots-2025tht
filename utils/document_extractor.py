from typing import Tuple, Dict, List, Optional
import os
from unstructured.partition.auto import partition
from unstructured.partition.doc import partition_doc
from unstructured.partition.docx import partition_docx
from unstructured.partition.pdf import partition_pdf
from unstructured.partition.ppt import partition_ppt
from unstructured.partition.pptx import partition_pptx
from unstructured.partition.xlsx import partition_xlsx
from .token_manager import TokenManager

class DocumentExtractor:
    """
    A class for extracting text from various document types and counting tokens.
    
    Supported file types:
    - PDF (.pdf)
    - Microsoft Word (.docx, .doc)
    - Microsoft Excel (.xlsx, .xls)
    - Microsoft PowerPoint (.pptx, .ppt)
    """
    
    SUPPORTED_EXTENSIONS = {
        '.pdf': 'application/pdf',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.doc': 'application/msword',
        '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        '.xls': 'application/vnd.ms-excel',
        '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        '.ppt': 'application/vnd.ms-powerpoint'
    }
    
    def __init__(self, token_manager: Optional[TokenManager] = None):
        """
        Initialize the DocumentExtractor.
        
        Args:
            token_manager (Optional[TokenManager]): A TokenManager instance.
                If None, a new instance will be created.
        """
        self.token_manager = token_manager or TokenManager()
    
    def is_supported_file(self, file_path: str) -> bool:
        """
        Check if the file type is supported.
        
        Args:
            file_path (str): Path to the file.
            
        Returns:
            bool: True if the file type is supported, False otherwise.
        """
        _, ext = os.path.splitext(file_path.lower())
        return ext in self.SUPPORTED_EXTENSIONS
    
    def get_file_mime_type(self, file_path: str) -> Optional[str]:
        """
        Get the MIME type of a file based on its extension.
        
        Args:
            file_path (str): Path to the file.
            
        Returns:
            Optional[str]: MIME type if supported, None otherwise.
        """
        _, ext = os.path.splitext(file_path.lower())
        return self.SUPPORTED_EXTENSIONS.get(ext)
    
    def extract_from_file(self, file_path: str) -> Tuple[str, int]:
        """
        Extract text from a file using the appropriate Unstructured partition function.
        
        Args:
            file_path (str): Path to the file.
        
        Returns:
            Tuple[str, int]: Extracted text and token count.
            
        Raises:
            ValueError: If the file type is not supported.
            Exception: If there's an error during text extraction.
        """
        if not self.is_supported_file(file_path):
            _, ext = os.path.splitext(file_path.lower())
            raise ValueError(f"Unsupported file extension: {ext}. Supported types are: {', '.join(self.SUPPORTED_EXTENSIONS.keys())}")
        
        try:
            _, ext = os.path.splitext(file_path.lower())
            
            match ext:
                case '.pdf':
                    elements = partition_pdf(file_path)
                case '.docx':
                    elements = partition_docx(file_path)
                case '.doc':
                    elements = partition_doc(file_path)
                case '.xlsx' | '.xls':
                    elements = partition_xlsx(file_path)
                case '.pptx':
                    elements = partition_pptx(file_path)
                case '.ppt':
                    elements = partition_ppt(file_path)
                case _:
                    elements = partition(file_path)

            text = "\n\n".join([str(element) for element in elements])
            
            tokens = self.token_manager.count_tokens(text)
            
            return text, tokens
            
        except Exception as e:
            raise Exception(f"Error extracting text from {file_path}: {str(e)}")
    
    def extract_batch(self, file_paths: List[str]) -> Dict[str, Tuple[str, int]]:
        """
        Extract text from multiple files.
        
        Args:
            file_paths (List[str]): List of file paths.
        
        Returns:
            Dict[str, Tuple[str, int]]: Dictionary mapping file paths to (text, token_count) tuples.
            
        Note:
            If extraction fails for any file, it will be skipped and not included in the result.
        """
        results = {}
        errors = {}
        
        for file_path in file_paths:
            try:
                if self.is_supported_file(file_path):
                    text, tokens = self.extract_from_file(file_path)
                    results[file_path] = (text, tokens)
                else:
                    _, ext = os.path.splitext(file_path.lower())
                    errors[file_path] = f"Unsupported file extension: {ext}"
            except Exception as e:
                errors[file_path] = str(e)
        
        if errors:
            print(f"Warning: Failed to extract text from {len(errors)} files:")
            for file_path, error in errors.items():
                print(f"  - {file_path}: {error}")
        
        return results