import unittest
from unittest.mock import patch, mock_open
from ss1 import find_subdomains, fuzz_urls, check_ping

class TestDomainTools(unittest.TestCase):
    
    def test_find_subdomains(self):
        domain = "example.com"
        wordlist_content = "sub1\nsub2\nsub3"
        with patch("builtins.open", mock_open(read_data=wordlist_content)), \
             patch("requests.get") as mocked_get:
            mocked_get.side_effect = [
                unittest.mock.Mock(status_code=200),
                unittest.mock.Mock(status_code=404),
                unittest.mock.Mock(status_code=200)
            ]
            result = find_subdomains(domain, "wordlist")
            self.assertEqual(len(result), 2)
            self.assertIn("http://sub1.example.com", result)
            self.assertIn("http://sub3.example.com", result)

    def test_fuzz_urls(self):
        domain = "example.com"
        wordlist_content = "page1\npage2\npage3"
        with patch("builtins.open", mock_open(read_data=wordlist_content)), \
             patch("requests.get") as mocked_get:
            mocked_get.side_effect = [
                unittest.mock.Mock(status_code=200),
                unittest.mock.Mock(status_code=404),
                unittest.mock.Mock(status_code=200)
            ]
            result = fuzz_urls(domain, "wordlist")
            self.assertEqual(len(result), 2)
            self.assertIn(f"http://{domain}/page1", result)
            self.assertIn(f"http://{domain}/page3", result)

    def test_check_ping(self):
        with patch("subprocess.check_output") as mocked_check_output:
            mocked_check_output.return_value = True
            result = check_ping("example.com")
            self.assertTrue(result)

            mocked_check_output.side_effect = Exception("Ping failed")
            result = check_ping("nonexistentdomain.com")
            self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
