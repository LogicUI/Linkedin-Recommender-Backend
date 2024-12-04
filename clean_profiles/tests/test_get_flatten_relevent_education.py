import sys
import os
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from clean_profiles import get_flattten_relevent_education

class TestGetFlattenReleventEducation:
    def test_get_flatten_relevent_education_valid(self):
        education = [
            {"degree_name": "Bachelor of Science", "school": "XYZ University", "year": 2020},
            {"degree_name": "Master of Arts", "school": "ABC College", "year": 2022},
        ]
        expected = "Bachelor of Science at XYZ University; Master of Arts at ABC College;"
        assert get_flattten_relevent_education(education) == expected

    def test_empty_list(self):
        education = []
        expected = ""
        assert get_flattten_relevent_education(education) == expected

    def test_missing_fields(self):
        education = [
            {"degree_name": "Bachelor of Science", "school": "XYZ University"},
            {"school": "ABC College", "year": 2022},
            {"degree_name": "PhD", "year": 2025},
        ]
        expected = "Bachelor of Science at XYZ University;"
        assert get_flattten_relevent_education(education) == expected

    def test_non_list_input(self):
        education = "Not a list"
        assert get_flattten_relevent_education(education) == ""

    def test_mixed_data_types(self):
        education = [
            {"degree_name": "Bachelor of Science", "school": "XYZ University", "year": 2020},
            "Invalid Entry",
            42,
            None,
        ]
        expected = "Bachelor of Science at XYZ University;"
        assert get_flattten_relevent_education(education) == expected

    def test_extra_fields(self):
    
        education = [
            {"degree_name": "Bachelor of Science", "school": "XYZ University", "year": 2020, "field": "Computer Science"},
            {"degree_name": "Master of Arts", "school": "ABC College", "year": 2022, "field": "Philosophy"},
        ]
        expected = "Bachelor of Science at XYZ University; Master of Arts at ABC College;"
        assert get_flattten_relevent_education(education) == expected

    def test_duplicate_entries(self):
        education = [
            {"degree_name": "Bachelor of Science", "school": "XYZ University", "year": 2020},
            {"degree_name": "Bachelor of Science", "school": "XYZ University", "year": 2020},
        ]
        expected = "Bachelor of Science at XYZ University;"
        assert get_flattten_relevent_education(education) == expected

    def test_all_invalid_entries(self):
        education = ["Invalid Entry", 42, None]
        expected = ""
        assert get_flattten_relevent_education(education) == expected

    def test_partial_valid_entries(self):
        education = [
            {"degree_name": "Bachelor of Science", "school": "XYZ University", "year": 2020},
            "Invalid Entry",
            {"school": "ABC College", "year": 2022},
            None,
        ]
        expected = "Bachelor of Science at XYZ University;"
        assert get_flattten_relevent_education(education) == expected