import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from clean_profiles import _get_relevant_education  

class TestRelevantEducation:
    def test_valid_education_data(self):
        """Test with valid education data containing all relevant fields."""
        education = [
            {"degree_name": "Bachelor of Science", "school": "XYZ University", "year": 2020},
            {"degree_name": "Master of Arts", "school": "ABC College", "year": 2022},
        ]
        expected = [
            {"degree_name": "Bachelor of Science", "school": "XYZ University"},
            {"degree_name": "Master of Arts", "school": "ABC College"},
        ]
        assert _get_relevant_education(education) == expected

    def test_missing_fields_in_education_data(self):
        """Test with some items missing relevant fields."""
        education = [
            {"degree_name": "Bachelor of Science", "school": "XYZ University", "year": 2020},
            {"school": "ABC College", "year": 2022},
            {"degree_name": "PhD", "year": 2025},
        ]
        expected = [
            {"degree_name": "Bachelor of Science", "school": "XYZ University"},
            {"school": "ABC College"},
            {"degree_name": "PhD"},
        ]
        assert _get_relevant_education(education) == expected

    def test_empty_education_list(self):
        """Test with an empty list."""
        assert _get_relevant_education([]) == []

    def test_none_as_input(self):
        """Test with None as input."""
        assert _get_relevant_education(None) == []

    def test_non_list_input(self):
        """Test with a non-list input."""
        assert _get_relevant_education("not a list") == []
        assert _get_relevant_education(123) == []
        assert _get_relevant_education({"degree_name": "Bachelor"}) == []

    def test_non_dict_items_in_list(self):
        """Test with a list containing non-dictionary items."""
        education = [
            {"degree_name": "Bachelor of Science", "school": "XYZ University"},
            "not a dict",
            123,
            ["another", "list"],
        ]
        expected = [{"degree_name": "Bachelor of Science", "school": "XYZ University"}]
        assert _get_relevant_education(education) == expected

    def test_partial_data_and_empty_dicts(self):
        """Test with partial data and empty dictionaries."""
        education = [
            {"degree_name": "Bachelor of Science", "school": "XYZ University"},
            {"degree_name": "PhD"},
            {},
            {"school": "ABC College"},
        ]
        expected = [
            {"degree_name": "Bachelor of Science", "school": "XYZ University"},
            {"degree_name": "PhD"},
            {"school": "ABC College"},
        ]
        assert _get_relevant_education(education) == expected