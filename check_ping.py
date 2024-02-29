import unittest
from unittest.mock import patch
from ss1 import check_ping

class TestCheckPing(unittest.TestCase):
    @patch('subprocess.check_output')
    def test_check_ping_success(self, mock_subprocess):
        mock_subprocess.return_value = True
        result = check_ping('google.com')
        self.assertTrue(result)

    @patch('subprocess.check_output', side_effect=Exception('ping failed'))
    def test_check_ping_failure(self, mock_subprocess):
        result = check_ping('nonexistentdomain.com')
        self.assertFalse(result)

if __name__ == '_main_':
    unittest.main()