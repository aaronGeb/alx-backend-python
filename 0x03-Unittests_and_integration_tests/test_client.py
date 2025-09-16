#!/usr/bin/env python3
"""
Unittests for client module.
"""
import unittest
from unittest.mock import patch, Mock, MagicMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


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
            ("google",
                {"repos_url": "https://api.github.com/orgs/google/repos"}),
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
            {"name": "repo1", "license": {"key": "my_license"}},
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
        self.assertEqual(client.public_repos(license="my_license"), ["repo1"])
        self.assertEqual(client.public_repos(license="apache-2.0"), ["repo2"])
        self.assertEqual(client.public_repos(license="gpl"), [])
        self.assertEqual(mock_get_json.call_count, 2)

        @parameterized.expand(
            [
                ({"license": {"key": "my_license"}}, "my_license", True),
                ({"license": {"key": "apache-2.0"}}, "my_license", False),
            ]
        )
        def test_has_license(self, repo, license_key, expected):
            """Test that the has_license static method
            returns the correct boolean value.
            """
            client = GithubOrgClient("google")
            self.assertEqual(client.has_license(repo, license_key), expected)


@parameterized_class([
  {
    "org_payload": org_payload,
    "repos_payload": repos_payload,
    "expected_repos": expected_repos,
    "apache2_repos": apache2_repos
  }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class to test GithubOrgClient.public_repos class."""
    @classmethod
    def setUpClass(cls):
        """Set up the class for integration tests."""
        route_payload = {
            "https://api.github.com/orgs/google": cls.org_payload,
            "https://api.github.com/orgs/google/repos": cls.repos_payload,
        }

        def get_json_side_effect(url):
            """Side effect function for get_json mock."""
            return route_payload[url]

        cls.get_patcher = patch("client.get_json", side_effect=get_json_side_effect)
        cls.mock_get_json = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Tear down the class after integration tests."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that the public_repos method
        returns the expected list of repos.
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test that the public_repos method
        returns the expected list of repos with a specific license.
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)
