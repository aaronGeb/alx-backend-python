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

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that the public_repos method
            returns the correct list of repo
            names.
        """
        org_name = "google"
        repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": None},
        ]
        expected_repos = ["repo1", "repo2", "repo3"]

        mock_get_json.side_effect = [
            {"repos_url": f"https://api.github.com/orgs/{org_name}/repos"},
            repos_payload,
        ]

        client = GithubOrgClient(org_name)
        self.assertEqual(client.public_repos(), expected_repos)
        self.assertEqual(client.public_repos(license="mit"), ["repo1"])
        self.assertEqual(client.public_repos(license="apache-2.0"), ["repo2"])
        self.assertEqual(client.public_repos(license="gpl"), [])
        self.assertEqual(mock_get_json.call_count, 2)
