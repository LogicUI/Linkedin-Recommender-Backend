import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from clean_profiles import _get_relevant_profile_files  

class TestRelevantProfiles: 
    def test_valid_profile_with_all_fields(self):
        profile = {
            "profile_url": "https://example.com",
            "full_name": "John Doe",
            "occupation": "Software Engineer",
            "country_full_name": "United States",
            "personal_emails": ["john.doe@example.com"],
        }
        expected = {
            "profile_url": "https://example.com",
            "full_name": "John Doe",
            "occupation": "Software Engineer",
            "country_full_name": "United States",
            "personal_emails": ["john.doe@example.com"],
        }
        assert _get_relevant_profile_files(profile) == expected

    def test_profile_missing_some_fields(self):
        profile = {
            "profile_url": "https://example.com",
            "full_name": "Jane Smith",
            "occupation": "Data Scientist",
        }
        expected = {
            "profile_url": "https://example.com",
            "full_name": "Jane Smith",
            "occupation": "Data Scientist",
            "personal_emails": [],
        }
        assert _get_relevant_profile_files(profile) == expected

    def test_profile_missing_all_fields(self):
        profile = {}
        expected = {
            "full_name": "Unknown",
            "personal_emails": [],
        }
        assert _get_relevant_profile_files(profile) == expected

    def test_invalid_profile_input(self):
        profile = "Not a dictionary"
        with pytest.raises(ValueError, match="Expected 'profile' to be a dictionary."):
            _get_relevant_profile_files(profile)

    def test_missing_full_name_field(self):
        profile = {
            "profile_url": "https://example.com",
            "occupation": "Project Manager",
            "personal_emails": ["manager@example.com"],
        }
        expected = {
            "profile_url": "https://example.com",
            "full_name": "Unknown",
            "occupation": "Project Manager",
            "personal_emails": ["manager@example.com"],
        }
        assert _get_relevant_profile_files(profile) == expected

    def test_personal_emails_not_a_list(self):
        profile = {
            "profile_url": "https://example.com",
            "full_name": "Alice Brown",
            "personal_emails": "alice@example.com",
        }
        expected = {
            "profile_url": "https://example.com",
            "full_name": "Alice Brown",
            "personal_emails": [],
        }
        assert _get_relevant_profile_files(profile) == expected

    def test_empty_string_for_full_name(self):
        profile = {
            "profile_url": "https://example.com",
            "full_name": "",
        }
        expected = {
            "profile_url": "https://example.com",
            "full_name": "Unknown",
            "personal_emails": [],
        }
        assert _get_relevant_profile_files(profile) == expected

    def test_no_personal_emails_field(self):
        profile = {
            "profile_url": "https://example.com",
            "full_name": "Bob",
            "occupation": "Developer",
        }
        expected = {
            "profile_url": "https://example.com",
            "full_name": "Bob",
            "occupation": "Developer",
            "personal_emails": [],
        }
        assert _get_relevant_profile_files(profile) == expected

        

