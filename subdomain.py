import unittest
from unittest.mock import patch, mock_open
from ss1 import find_subdomains  

class TestFindSubdomains(unittest.TestCase):
    @patch('requests.get')
    def test_find_subdomains(self, mock_get):
        
        mock_get.side_effect = [
            type('MockResponse', (object,), {'status_code': 200}),  
            type('MockResponse', (object,), {'status_code': 404})   
        ]

        with patch('builtins.open', mock_open(read_data='sub1\nsub2')) as mock_file:
            result = find_subdomains('example.com', 'wordlist.txt')
            self.assertIn('http://sub1.example.com', result)
            self.assertNotIn('http://sub2.example.com', result)
            mock_file.assert_called_with('wordlist.txt', 'r')

if __name__ == '_main_':
   unittest.main()