import unittest
from unittest.mock import patch, MagicMock
import os
import requests
from integra_ai.ai.gemini import generate_code

class TestGeminiAI(unittest.TestCase):

    @patch('integra_ai.ai.gemini.log') # Mock the logger
    @patch('requests.post')
    @patch('os.getenv')
    def test_generate_code_success(self, mock_getenv, mock_post, mock_log):
        """Testa a geração de código bem-sucedida com uma resposta válida da API."""
        mock_getenv.return_value = "TEST_API_KEY"

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {"text": "print('Hello, Gemini!')"}
                        ]
                    }
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        prompt = "Write a Python hello world program."
        result = generate_code(prompt)

        self.assertEqual(result, "print('Hello, Gemini!')")
        mock_getenv.assert_called_with("GEMINI_API_KEY")
        mock_post.assert_called_once_with(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent",
            headers={"Content-Type": "application/json"},
            params={"key": "TEST_API_KEY"},
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=60
        )
        mock_log.info.assert_called_once()
        mock_log.error.assert_not_called()

    @patch('integra_ai.ai.gemini.log') # Mock the logger
    @patch('requests.post')
    @patch('os.getenv')
    def test_generate_code_http_error(self, mock_getenv, mock_post, mock_log):
        """Testa o tratamento de erro HTTP da API."""
        mock_getenv.return_value = "TEST_API_KEY"

        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_response.raise_for_status.side_effect = requests.HTTPError("400 Client Error: Bad Request for url: ...", response=mock_response)
        mock_post.return_value = mock_response

        prompt = "Invalid prompt"
        with self.assertRaises(requests.HTTPError):
            generate_code(prompt)

        mock_getenv.assert_called_with("GEMINI_API_KEY")
        mock_post.assert_called_once()
        mock_log.info.assert_called_once()
        mock_log.error.assert_called_once()

    @patch('integra_ai.ai.gemini.log') # Mock the logger
    @patch('os.getenv')
    def test_generate_code_no_api_key(self, mock_getenv, mock_log):
        """Testa o caso em que a chave da API não está definida."""
        mock_getenv.return_value = ""

        prompt = "Some prompt"
        with self.assertRaisesRegex(RuntimeError, "GEMINI_API_KEY not set in environment"):
            generate_code(prompt)

        mock_getenv.assert_called_with("GEMINI_API_KEY")
        mock_log.info.assert_not_called()
        mock_log.error.assert_not_called()

    @patch('integra_ai.ai.gemini.log') # Mock the logger
    @patch('requests.post')
    @patch('os.getenv')
    def test_generate_code_empty_candidates(self, mock_getenv, mock_post, mock_log):
        """Testa o caso em que a API retorna uma lista de candidatos vazia."""
        mock_getenv.return_value = "TEST_API_KEY"

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "candidates": []
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        prompt = "Test empty candidates"
        result = generate_code(prompt)
        self.assertEqual(result, str({"candidates": []}))
        mock_log.info.assert_called_once()
        mock_log.error.assert_not_called()

    @patch('integra_ai.ai.gemini.log') # Mock the logger
    @patch('requests.post')
    @patch('os.getenv')
    def test_generate_code_no_text_in_parts(self, mock_getenv, mock_post, mock_log):
        """Testa o caso em que a API retorna conteúdo sem a chave 'text'."""
        mock_getenv.return_value = "TEST_API_KEY"

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {"other_key": "some_value"}
                        ]
                    }
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        prompt = "Test no text in parts"
        result = generate_code(prompt)
        self.assertEqual(result, str({"candidates": [{"content": {"parts": [{"other_key": "some_value"}]}}]}))
        mock_log.info.assert_called_once()
        mock_log.error.assert_not_called()

    @patch('integra_ai.ai.gemini.log') # Mock the logger
    @patch('requests.post')
    @patch('os.getenv')
    def test_generate_code_api_key_from_arg(self, mock_getenv, mock_post, mock_log):
        """Testa o uso da chave da API fornecida como argumento da função."""
        mock_getenv.return_value = "ENV_API_KEY"

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {"text": "API key from arg"}
                        ]
                    }
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        prompt = "Test API key from arg"
        api_key_arg = "DIRECT_API_KEY"
        result = generate_code(prompt, api_key=api_key_arg)

        self.assertEqual(result, "API key from arg")
        mock_getenv.assert_called_with("GEMINI_API_KEY")
        mock_post.assert_called_once_with(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent",
            headers={"Content-Type": "application/json"},
            params={"key": api_key_arg},
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=60
        )
        mock_log.info.assert_called_once()
        mock_log.error.assert_not_called()

    @patch('integra_ai.ai.gemini.log') # Mock the logger
    @patch('requests.post')
    @patch('os.getenv')
    def test_generate_code_custom_model(self, mock_getenv, mock_post, mock_log):
        """Testa o uso de um modelo personalizado."""
        mock_getenv.return_value = "TEST_API_KEY"

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {"text": "Response from custom model"}
                        ]
                    }
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        prompt = "Test custom model"
        custom_model = "gemini-pro"
        result = generate_code(prompt, model=custom_model)

        self.assertEqual(result, "Response from custom model")
        mock_post.assert_called_once_with(
            f"https://generativelanguage.googleapis.com/v1beta/models/{custom_model}:generateContent",
            headers={"Content-Type": "application/json"},
            params={"key": "TEST_API_KEY"},
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=60
        )
        mock_log.info.assert_called_once()
        mock_log.error.assert_not_called()

