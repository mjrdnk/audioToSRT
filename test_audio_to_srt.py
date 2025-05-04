import unittest
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock
import numpy as np
import torch

from audio_to_srt import (
    format_time,
    build_srt_file_line,
    get_srt_path,
    identify_top_languages,
    transcribe_one
)

class TestAudioToSRT(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        self.test_audio_file = os.path.join(self.test_dir, "test_audio.mp3")
        with open(self.test_audio_file, 'w') as f:
            f.write("dummy content")

    def tearDown(self):
        # Clean up temporary directory and its contents
        try:
            shutil.rmtree(self.test_dir)
        except Exception:
            pass

    def test_format_time(self):
        # Test various time formats
        self.assertEqual(format_time(0), "00:00:00,000")
        self.assertEqual(format_time(61.5), "00:01:01,500")
        self.assertEqual(format_time(3661.999), "01:01:01,999")
        self.assertEqual(format_time(123.456), "00:02:03,456")

    def test_build_srt_file_line(self):
        segment = {
            "start": 1.5,
            "end": 3.2,
            "text": "Hello world",
            "language": "en"
        }
        expected = "1\n00:00:01,500 --> 00:00:03,200\n[en] Hello world\n\n"
        result = build_srt_file_line(segment, 0, "en")
        self.assertEqual(result, expected)

    def test_get_srt_path(self):
        # Test with a simple path
        path = get_srt_path(self.test_audio_file, "en")
        expected = os.path.join(
            os.path.splitext(self.test_audio_file)[0],  # directory_name
            os.path.basename(os.path.splitext(self.test_audio_file)[0]) + ".en.srt"  # file_name
        )
        self.assertEqual(path, expected)

        # Test with a path containing spaces
        spaced_file = os.path.join(self.test_dir, "test audio file.mp3")
        path = get_srt_path(spaced_file, "en")
        expected = os.path.join(
            os.path.splitext(spaced_file)[0],  # directory_name
            os.path.basename(os.path.splitext(spaced_file)[0]) + ".en.srt"  # file_name
        )
        self.assertEqual(path, expected)

    @patch('whisper.load_audio')
    @patch('whisper.pad_or_trim')
    @patch('whisper.log_mel_spectrogram')
    def test_identify_top_languages(self, mock_log_mel, mock_pad, mock_load):
        # Mock the model and its methods
        mock_model = MagicMock()
        mock_model.dims.n_mels = 80
        mock_model.device = "cpu"
        
        # Mock the language detection results
        mock_probs = {
            "en": 0.6,
            "es": 0.3,
            "fr": 0.1
        }
        mock_model.detect_language.return_value = (None, mock_probs)
        
        # Mock the audio processing chain with proper tensor objects
        mock_load.return_value = np.zeros(16000)  # 1 second of audio at 16kHz
        mock_pad.return_value = np.zeros(16000)
        mock_mel = torch.zeros((80, 3000))  # Mock mel spectrogram
        mock_log_mel.return_value = mock_mel
        
        # Replace the global model with our mock
        with patch('audio_to_srt.model', mock_model):
            languages = identify_top_languages(self.test_audio_file)
            self.assertEqual(languages, ["en", "es", "fr"])

    @patch('whisper.load_model')
    def test_transcribe_one(self, mock_load_model):
        # Mock the model and its transcribe method
        mock_model = MagicMock()
        mock_model.transcribe.return_value = {
            "segments": [
                {
                    "start": 0,
                    "end": 1,
                    "text": "Test transcription",
                    "language": "en"
                }
            ]
        }
        mock_load_model.return_value = mock_model

        # Test transcription
        with patch('audio_to_srt.model', mock_model):
            transcribe_one(self.test_audio_file, "en")
            
            # Verify the model was called correctly
            mock_model.transcribe.assert_called_once_with(
                self.test_audio_file,
                verbose=True,
                task='transcribe',
                language="en"
            )

if __name__ == '__main__':
    unittest.main()
