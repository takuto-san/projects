import unittest
from unittest.mock import patch, MagicMock
import requests

from main import Request, send_api, run

class TestAPIExecution(unittest.TestCase):
    @patch("requests.request")
    def test_send_api(self, mock_request):
        mock_res = MagicMock()
        mock_res.status_code = 200
        mock_request.return_value = mock_res
        
        req = Request(
            base_url="https://api.github.com",
            method="get",
            path="/zen",
            params={"q": "test"}
        )

        res = send_api(req)
        
        mock_request.assert_called_once_with(
            "GET", 
            "https://api.github.com/zen", 
            params={"q": "test"}
        )
        self.assertEqual(res.status_code, 200)

    @patch("requests.request")
    @patch("builtins.print")
    def test_run_success(self, mock_print, mock_request):
        mock_res = MagicMock()
        mock_res.status_code = 200
        mock_request.return_value = mock_res

        test_data = [
            Request(base_url="https://api.github.com", method="get", path="/zen"),
            Request(base_url="https://api.github.com", method="get", path="/meta")
        ]

        run(test_data)

        self.assertEqual(mock_request.call_count, 2)
        self.assertEqual(mock_print.call_count, 2)

    @patch("requests.request")
    @patch("builtins.print")
    def test_run_failure_stops_loop(self, mock_print, mock_request):
        mock_success = MagicMock()
        mock_success.status_code = 200

        mock_fail = MagicMock()
        mock_fail.raise_for_status.side_effect = requests.exceptions.RequestException("Mock Error")

        mock_request.side_effect = [mock_success, mock_fail, mock_success]

        test_data = [
            Request(base_url="https://test.com", method="get", path="/1"),
            Request(base_url="https://test.com", method="get", path="/2"),
            Request(base_url="https://test.com", method="get", path="/3")
        ]

        run(test_data)

        self.assertEqual(mock_request.call_count, 2)
        self.assertEqual(mock_print.call_count, 2)

if __name__ == "__main__":
    unittest.main()