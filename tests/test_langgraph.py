import pytest
from unittest.mock import patch, MagicMock
import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from langgraph_setup import LangGraphSetup
from llm_setup import LLMSetup
from tool_setup import ToolSetup, search_wikipedia, search_web_with_duckduckgo, search_duckduckgo_news

class TestLLMSetup:
    @patch('llm_setup.os')
    @patch('llm_setup.load_dotenv')
    @patch('llm_setup.ChatOpenAI')
    def test_init_success(self, mock_chat_openai, mock_load_dotenv, mock_os):
        mock_os.getenv.return_value = "fake-api-key"
        mock_chat_openai.return_value = "fake-model"
        
        llm = LLMSetup()
        
        mock_load_dotenv.assert_called_once()
        mock_os.getenv.assert_called_once_with("OPENAI_API_KEY")
        mock_chat_openai.assert_called_once_with(
            model="gpt-4o-mini",
            temperature=0,
            api_key="fake-api-key"
        )
        assert llm.get_model() == "fake-model"
    
    @patch('llm_setup.os')
    @patch('llm_setup.load_dotenv')
    def test_init_missing_api_key(self, mock_load_dotenv, mock_os):
        mock_os.getenv.return_value = None
        with pytest.raises(AssertionError) as e:
            LLMSetup()
        
        assert "OPENAI_API_KEY is not set" in str(e.value)

class TestToolSetup:
    def test_init(self):
        tool_setup = ToolSetup()
        
        assert tool_setup.tools == [search_wikipedia, search_web_with_duckduckgo, search_duckduckgo_news]
    
    def test_get_tools(self):
        tool_setup = ToolSetup()
        
        tools = tool_setup.get_tools()
        
        assert tools == [search_wikipedia, search_web_with_duckduckgo, search_duckduckgo_news]

class TestLangGraphSetup:
    @patch('langgraph_setup.create_react_agent')
    def test_init_with_defaults(self, mock_create_react_agent):
        setup = LangGraphSetup()
        
        assert isinstance(setup.llm_setup, LLMSetup)
        assert isinstance(setup.tool_setup, ToolSetup)
        mock_create_react_agent.assert_called_once()
    
    def test_extract_message_content_simple(self):
        setup = LangGraphSetup()
        mock_message = MagicMock()
        mock_message.type = "user"
        mock_message.content = "test message"
        
        with patch.object(setup, '_log_message') as mock_log:
            result = setup._extract_message_content(mock_message)
        
        assert result == {"role": "user", "content": "test message"}
        mock_log.assert_called_once_with(mock_message, truncate=True)
    
    def test_extract_message_content_with_tool_calls(self):
        setup = LangGraphSetup()
        mock_message = MagicMock()
        mock_message.type = "ai"
        mock_message.content = None
        mock_message.additional_kwargs = {
            "tool_calls": [
                {
                    "function": {
                        "name": "test_tool",
                        "arguments": '{"arg1": "value1"}'
                    }
                }
            ]
        }
        
        with patch.object(setup, '_log_message') as mock_log:
            result = setup._extract_message_content(mock_message)
        
        assert result == {
            "role": "ai", 
            "content": None,
            "tool_calls": [
                {
                    "name": "test_tool",
                    "arguments": '{"arg1": "value1"}'
                }
            ]
        }
        mock_log.assert_called_once_with(mock_message, truncate=True)
    
    def test_log_message_content(self):
        setup = LangGraphSetup()
        mock_message = MagicMock()
        mock_message.type = "user"
        mock_message.content = "short message"
        
        with patch('builtins.print') as mock_print:
            setup._log_message(mock_message)
            mock_print.assert_called_once_with("\n[USER]: short message")
    
    def test_log_message_truncate(self):
        setup = LangGraphSetup()
        mock_message = MagicMock()
        mock_message.type = "user"
        mock_message.content = "x" * 150
        
        with patch('builtins.print') as mock_print:
            setup._log_message(mock_message, truncate=True)
            
        mock_print.assert_called_once()
        call_args = mock_print.call_args[0][0]
        assert call_args.endswith("...")
        assert len(call_args) < 150
    
    def test_log_message_tool_calls(self):
        setup = LangGraphSetup()
        mock_message = MagicMock()
        mock_message.type = "ai"
        mock_message.content = None
        mock_message.additional_kwargs = {
            "tool_calls": [
                {
                    "function": {
                        "name": "test_tool",
                        "arguments": '{"arg1": "value1"}'
                    }
                }
            ]
        }
        
        with patch('builtins.print') as mock_print:
            setup._log_message(mock_message)
            
        mock_print.assert_called_once()
        assert "TOOL REQUEST" in mock_print.call_args[0][0]
        assert "test_tool" in mock_print.call_args[0][0]
    
    def test_research(self):
        setup = LangGraphSetup()
        setup.graph = MagicMock()
        
        mock_message1 = MagicMock()
        mock_message1.type = "user"
        mock_message1.content = "test query"
        
        mock_message2 = MagicMock()
        mock_message2.type = "ai"
        mock_message2.content = "test response"
        
        setup.graph.stream.return_value = [
            {"messages": [mock_message1]},
            {"messages": [mock_message1, mock_message2]}
        ]
        
        with patch.object(setup, '_extract_message_content') as mock_extract:
            mock_extract.side_effect = [
                {"role": "user", "content": "test query"},
                {"role": "ai", "content": "test response"}
            ]
            results = setup.research("test query")
        
        assert len(results) == 2
        setup.graph.stream.assert_called_once()
        formatted_input = setup.graph.stream.call_args[0][0]
        assert formatted_input == {"messages": [{"role": "user", "content": "test query"}]}

class TestToolFunctions:
    @patch('tool_setup.wikipedia')
    def test_search_wikipedia_success_function(self, mock_wikipedia):
        search_func = search_wikipedia.func
        
        mock_page = MagicMock()
        mock_page.title = "Test Title"
        mock_page.url = "https://en.wikipedia.org/wiki/Test_Title"
        
        mock_wikipedia.page.return_value = mock_page
        mock_wikipedia.summary.return_value = "Test summary"
        
        result = search_func("test topic")
        
        assert result["status"] == "success"
        assert result["title"] == "Test Title"
        assert result["url"] == "https://en.wikipedia.org/wiki/Test_Title"
        assert result["summary"] == "Test summary"
    
    @patch('tool_setup.wikipedia')
    def test_search_wikipedia_disambiguation_function(self, mock_wikipedia):
        search_func = search_wikipedia.func
        
        class DisambiguationError(Exception):
            def __init__(self, title, options):
                self.title = title
                self.options = options
        
        mock_wikipedia.exceptions.DisambiguationError = DisambiguationError
        mock_wikipedia.page.side_effect = DisambiguationError("test topic", ["Option 1", "Option 2"])
        
        def mock_summary(option, sentences=None):
            if option == "Option 1":
                return "Summary 1"
            elif option == "Option 2":
                return "Summary 2"
            raise Exception(f"Unexpected option: {option}")
            
        mock_wikipedia.summary.side_effect = mock_summary
        
        result = search_func("test topic")
        
        assert result["status"] == "disambiguation_error"
        assert result["query"] == "test topic"
        assert "message" in result
        assert len(result["options"]) == 2
    
    @patch('tool_setup.DDGS')
    def test_search_web_with_duckduckgo_function(self, mock_ddgs):
        search_func = search_web_with_duckduckgo.func
        
        mock_ddgs_instance = MagicMock()
        mock_ddgs.return_value = mock_ddgs_instance
        
        mock_results = [
            {"title": "Result 1", "body": "Content 1", "href": "url1"},
            {"title": "Result 2", "body": "Content 2", "href": "url2"}
        ]
        mock_ddgs_instance.text.return_value = mock_results
        
        result = search_func("test query")
        
        assert result["status"] == "success"
        assert result["query"] == "test query"
        assert len(result["results"]) == 2
        mock_ddgs_instance.text.assert_called_once_with(
            keywords="test query",
            region="wt-wt",
            safesearch="moderate",
            max_results=5
        )
    
    @patch('tool_setup.DDGS')
    def test_search_duckduckgo_news_function(self, mock_ddgs):
        search_func = search_duckduckgo_news.func
        
        mock_ddgs_instance = MagicMock()
        mock_ddgs.return_value = mock_ddgs_instance
        
        mock_results = [
            {"title": "News 1", "body": "Content 1", "url": "url1", "date": "2023-01-01", "source": "Source 1"},
            {"title": "News 2", "body": "Content 2", "url": "url2", "date": "2023-01-02", "source": "Source 2"}
        ]
        mock_ddgs_instance.news.return_value = mock_results
        
        result = search_func("test query", time_period="d")
        
        assert result["status"] == "success"
        assert result["query"] == "test query"
        assert result["time_period"] == "d"
        assert len(result["results"]) == 2
        mock_ddgs_instance.news.assert_called_once_with(
            keywords="test query",
            region="wt-wt",
            safesearch="moderate",
            timelimit="d",
            max_results=5
        )