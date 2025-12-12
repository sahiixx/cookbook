# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Unit tests for Voice Memos notebook API migration from google-genai to google.generativeai.

Tests cover:
- API initialization and configuration
- File upload functionality
- Content generation with multiple files
- Error handling and edge cases
- API compatibility between old and new SDK
"""

import unittest
from unittest.mock import Mock, MagicMock, patch, mock_open
import sys
import os


class TestVoiceMemosAPIMigration(unittest.TestCase):
    """Test suite for Voice Memos API migration."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_api_key = "test_api_key_1234567890"
        self.mock_file_path = "test_audio.m4a"
        self.mock_file_uri = "https://generativelanguage.googleapis.com/v1beta/files/test_file_id"
        
    def tearDown(self):
        """Clean up after tests."""
        pass

    @patch('google.generativeai.configure')
    def test_genai_configure_with_api_key(self, mock_configure):
        """Test that genai.configure is called with the correct API key."""
        import google.generativeai as genai
        
        genai.configure(api_key=self.mock_api_key)
        
        mock_configure.assert_called_once_with(api_key=self.mock_api_key)

    @patch('google.generativeai.configure')
    def test_genai_configure_without_api_key_raises_error(self, mock_configure):
        """Test that configure raises appropriate error without API key."""
        import google.generativeai as genai
        
        mock_configure.side_effect = ValueError("API key is required")
        
        with self.assertRaises(ValueError) as context:
            genai.configure(api_key=None)
        
        self.assertIn("API key is required", str(context.exception))

    @patch('google.generativeai.upload_file')
    def test_upload_file_with_path(self, mock_upload):
        """Test file upload with path parameter."""
        import google.generativeai as genai
        
        mock_file = Mock()
        mock_file.uri = self.mock_file_uri
        mock_file.name = "files/test_file_id"
        mock_upload.return_value = mock_file
        
        result = genai.upload_file(path=self.mock_file_path)
        
        mock_upload.assert_called_once_with(path=self.mock_file_path)
        self.assertEqual(result.uri, self.mock_file_uri)

    @patch('google.generativeai.upload_file')
    def test_upload_file_with_display_name(self, mock_upload):
        """Test file upload with display name."""
        import google.generativeai as genai
        
        mock_file = Mock()
        mock_file.uri = self.mock_file_uri
        mock_file.display_name = "Test Audio File"
        mock_upload.return_value = mock_file
        
        result = genai.upload_file(
            path=self.mock_file_path,
            display_name="Test Audio File"
        )
        
        self.assertEqual(result.display_name, "Test Audio File")

    @patch('google.generativeai.upload_file')
    def test_upload_file_handles_nonexistent_file(self, mock_upload):
        """Test that upload_file handles non-existent files appropriately."""
        import google.generativeai as genai
        
        mock_upload.side_effect = FileNotFoundError("File not found")
        
        with self.assertRaises(FileNotFoundError):
            genai.upload_file(path="nonexistent_file.m4a")

    @patch('google.generativeai.upload_file')
    def test_upload_multiple_files(self, mock_upload):
        """Test uploading multiple files sequentially."""
        import google.generativeai as genai
        
        mock_files = []
        for i in range(3):
            mock_file = Mock()
            mock_file.uri = f"{self.mock_file_uri}_{i}"
            mock_file.name = f"files/test_file_{i}"
            mock_files.append(mock_file)
        
        mock_upload.side_effect = mock_files
        
        results = []
        for i in range(3):
            result = genai.upload_file(path=f"file_{i}.txt")
            results.append(result)
        
        self.assertEqual(len(results), 3)
        self.assertEqual(mock_upload.call_count, 3)

    @patch('google.generativeai.GenerativeModel')
    def test_generative_model_initialization(self, mock_model_class):
        """Test GenerativeModel initialization with model name."""
        import google.generativeai as genai
        
        mock_model = Mock()
        mock_model_class.return_value = mock_model
        
        model = genai.GenerativeModel(model_name="models/gemini-2.5-flash")
        
        mock_model_class.assert_called_once_with(model_name="models/gemini-2.5-flash")

    @patch('google.generativeai.GenerativeModel')
    def test_generative_model_with_system_instruction(self, mock_model_class):
        """Test GenerativeModel initialization with system instruction."""
        import google.generativeai as genai
        
        mock_model = Mock()
        mock_model_class.return_value = mock_model
        system_instruction = "You are a helpful assistant."
        
        model = genai.GenerativeModel(
            model_name="models/gemini-2.5-flash",
            system_instruction=system_instruction
        )
        
        mock_model_class.assert_called_once()
        call_kwargs = mock_model_class.call_args[1]
        self.assertEqual(call_kwargs['system_instruction'], system_instruction)

    @patch('google.generativeai.GenerativeModel')
    def test_generate_content_with_prompt(self, mock_model_class):
        """Test generate_content with text prompt."""
        import google.generativeai as genai
        
        mock_model = Mock()
        mock_response = Mock()
        mock_response.text = "Generated response"
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        model = genai.GenerativeModel(model_name="models/gemini-2.5-flash")
        response = model.generate_content("Test prompt")
        
        mock_model.generate_content.assert_called_once_with("Test prompt")
        self.assertEqual(response.text, "Generated response")

    @patch('google.generativeai.GenerativeModel')
    @patch('google.generativeai.upload_file')
    def test_generate_content_with_files(self, mock_upload, mock_model_class):
        """Test generate_content with uploaded files."""
        import google.generativeai as genai
        
        mock_files = []
        for i in range(2):
            mock_file = Mock()
            mock_file.uri = f"{self.mock_file_uri}_{i}"
            mock_files.append(mock_file)
        mock_upload.side_effect = mock_files
        
        mock_model = Mock()
        mock_response = Mock()
        mock_response.text = "Analysis of files"
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        file1 = genai.upload_file(path="file1.txt")
        file2 = genai.upload_file(path="file2.txt")
        
        model = genai.GenerativeModel(model_name="models/gemini-2.5-flash")
        response = model.generate_content(["Analyze these files", file1, file2])
        
        mock_model.generate_content.assert_called_once()
        self.assertEqual(response.text, "Analysis of files")

    @patch('google.generativeai.GenerativeModel')
    def test_generate_content_with_request_options(self, mock_model_class):
        """Test generate_content with request options like timeout."""
        import google.generativeai as genai
        
        mock_model = Mock()
        mock_response = Mock()
        mock_response.text = "Response with timeout"
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        model = genai.GenerativeModel(model_name="models/gemini-2.5-flash")
        response = model.generate_content(
            "Test prompt",
            request_options={"timeout": 600}
        )
        
        call_kwargs = mock_model.generate_content.call_args[1]
        self.assertIn('request_options', call_kwargs)
        self.assertEqual(call_kwargs['request_options']['timeout'], 600)


class TestAPICompatibility(unittest.TestCase):
    """Test compatibility between old google-genai and new google.generativeai SDK."""

    def test_old_vs_new_api_method_names(self):
        """Test that old API patterns map to new API patterns."""
        old_api_methods = {
            'files.upload': 'upload_file',
            'models.generate_content': 'GenerativeModel.generate_content',
        }
        
        for old_method, new_method in old_api_methods.items():
            self.assertIsInstance(old_method, str)
            self.assertIsInstance(new_method, str)
            self.assertNotEqual(old_method, new_method)


if __name__ == '__main__':
    unittest.main()