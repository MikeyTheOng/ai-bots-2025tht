from typing import Tuple
import tiktoken


class TokenManager:
    """
    A class to manage token counting and token limits for large language models.
    """
    
    def __init__(self, max_tokens: int = 120000, encoding_name: str = "cl100k_base"):
        """
        Initialize the TokenManager.
        
        Args:
            max_tokens (int): Maximum number of tokens allowed. Default is 120,000.
            encoding_name (str): The name of the tiktoken encoding to use.
                Default is "cl100k_base" which is used for GPT-4 models.
        """
        self.max_tokens = max_tokens
        self.encoding = tiktoken.get_encoding(encoding_name)
    
    def count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in a text using tiktoken.
        
        Args:
            text (str): The text to tokenize.
        
        Returns:
            int: Number of tokens.
        """
        return len(self.encoding.encode(text))
    
    def check_token_limit(self, current_tokens: int, additional_tokens: int) -> Tuple[bool, int]:
        """
        Check if adding additional tokens would exceed the token limit.
        
        Args:
            current_tokens (int): Current number of tokens.
            additional_tokens (int): Number of additional tokens to add.
            
        Returns:
            Tuple[bool, int]: A tuple containing:
                - bool: True if adding would exceed the limit, False otherwise.
                - int: The total tokens that would result from the addition.
        """
        total_tokens = current_tokens + additional_tokens
        would_exceed = total_tokens > self.max_tokens
        return would_exceed, total_tokens
