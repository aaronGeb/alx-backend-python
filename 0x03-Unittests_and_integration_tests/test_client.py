#!/usr/bin/env python3
"""
Unittests for client module.
"""
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """TestGithubOrgClient class to test GithubOrgClient class."""

    @parameterized.expand(
        [
            ("google", {"login": "google"}),
            ("abc", {"login": "abc"}),
        ]
    )
    @patch("client.get_json")
    def test_org(self, org_name, org_payload, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value."""
        mock_get_json.return_value = org_payload
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, org_payload)
        mock_get_json.assert_called_once()

    @parameterized.expand(
        [
            ("google", {"repos_url":
             "https://api.github.com/orgs/google/repos"}),
            ("abc", {"repos_url": "https://api.github.com/orgs/abc/repos"}),
        ]
    )
    @patch("client.get_json")
    def test_public_repos_url(self, org_name, org_payload, mock_get_json):
        """Test that the _public_repos_url property"""
        mock_get_json.return_value = org_payload
        client = GithubOrgClient(org_name)
        self.assertEqual(client._public_repos_url, org_payload["repos_url"])
        mock_get_json.assert_called_once()
