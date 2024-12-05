import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from clean_profiles import _get_flatten_relevant_fields


class TestFlattenRelevantCertifications:
    def test_get_relevant_certification_field(self):
        certifications = [
            {
                "starts_at": {"day": 1, "month": 7, "year": 2021},
                "ends_at": None,
                "name": "Enhance Emotional Resilience at Work",
                "license_number": None,
                "display_source": "badgr.io",
                "authority": "Aventis Learning Group",
                "url": "https://api.au.badgr.io/public/assertions/zslWxXnPS5GFyBH1ksC2Nw?identity__email=ondrej.kollert%40merck.com",
            },
            {
                "starts_at": {"day": 1, "month": 10, "year": 2023},
                "ends_at": {"day": 31, "month": 10, "year": 2026},
                "name": "AWS Certified Cloud Practitioner",
                "license_number": None,
                "display_source": "credly.com",
                "authority": "Amazon Web Services (AWS)",
                "url": "https://www.credly.com/badges/04214075-324d-4ba4-8f11-cdb4bd19f6ce/linked_in_profile",
            },
        ]

        result = _get_flatten_relevant_fields(
            dict_list=certifications,
            between_words=" from ",
            name="name",
            authority="authority",
        )

        assert (
            result
            == "Enhance Emotional Resilience at Work from Aventis Learning Group; AWS Certified Cloud Practitioner from Amazon Web Services (AWS);"
        )

    def test_flatten_relevant_fields_empty_list(self):
        certifications = []

        result = _get_flatten_relevant_fields(
            dict_list=certifications,
            between_words=" from ",
            name="name",
            authority="authority",
        )

        assert result == ""

    def test_flatten_relevant_fields_duplicates(self):
        certifications = [
            {
                "name": "Enhance Emotional Resilience at Work",
                "authority": "Aventis Learning Group",
            },
            {
                "name": "Enhance Emotional Resilience at Work",
                "authority": "Aventis Learning Group",
            },
        ]

        result = _get_flatten_relevant_fields(
            dict_list=certifications,
            between_words=" from ",
            name="name",
            authority="authority",
        )

        assert (
            result
            == "Enhance Emotional Resilience at Work from Aventis Learning Group;"
        )

    def test_flatten_relevant_fields_mixed_entries(self):
        certifications = [
            {
                "name": "Enhance Emotional Resilience at Work",
                "authority": "Aventis Learning Group",
            },
            {
                "name": None,
                "authority": "Amazon Web Services (AWS)",
            },
            {
                "name": "AWS Certified Cloud Practitioner",
                "authority": "Amazon Web Services (AWS)",
            },
        ]
        result = _get_flatten_relevant_fields(
            dict_list=certifications,
            between_words=" from ",
            name="name",
            authority="authority",
        )

        assert (
            result
            == "Enhance Emotional Resilience at Work from Aventis Learning Group; AWS Certified Cloud Practitioner from Amazon Web Services (AWS);"
        )

    def test_flatten_relevant_fields_no_valid_keys(self):
        certifications = [
            {
                "starts_at": {"day": 1, "month": 7, "year": 2021},
                "ends_at": None,
                "license_number": None,
                "display_source": "badgr.io",
                "url": "https://api.au.badgr.io/public/assertions/zslWxXnPS5GFyBH1ksC2Nw?identity__email=ondrej.kollert%40merck.com",
            }
        ]

        result = _get_flatten_relevant_fields(
            dict_list=certifications,
            between_words=" from ",
            name="name",
            authority="authority",
        )

        assert result == ""
