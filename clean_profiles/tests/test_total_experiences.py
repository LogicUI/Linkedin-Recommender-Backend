import sys
import os
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from clean_profiles import calculate_total_experience

class TestTotalExperience:
    def test_correct_experiences(self):
        experiences = [
            {
                "company": "GovTech Singapore",
                "title": "Senior Software Engineer",
                "location": "Singapore",
                "ends_at": None,
                "starts_at": {"day": 1, "month": 9, "year": 2024},
            },
            {
                "company": "ASUS",
                "title": "Senior Software Engineer",
                "location": "Singapore",
                "ends_at": {"day": 31, "month": 7, "year": 2024},
                "starts_at": {"day": 1, "month": 10, "year": 2023},
            },
            {
                "company": "Indeed.com",
                "title": "Software Engineer II",
                "location": "Singapore",
                "ends_at": {"day": 31, "month": 5, "year": 2023},
                "starts_at": {"day": 1, "month": 3, "year": 2022},
            },
            {
                "company": "Garena",
                "title": "Senior Software Engineer",
                "location": "Singapore",
                "ends_at": {"day": 28, "month": 2, "year": 2022},
                "starts_at": {"day": 1, "month": 2, "year": 2021},
            },
            {
                "company": "Garena",
                "title": "Software Engineer",
                "location": "Singapore",
                "ends_at": {"day": 28, "month": 2, "year": 2021},
                "starts_at": {"day": 1, "month": 2, "year": 2020},
            },
            {
                "company": "Upwork",
                "title": "Software Engineer",
                "location": "Remote",
                "ends_at": {"day": 31, "month": 1, "year": 2020},
                "starts_at": {"day": 1, "month": 11, "year": 2017},
            },
            {
                "company": "Autodesk",
                "title": "Software Engineer",
                "location": "Shanghai City, China",
                "ends_at": {"day": 30, "month": 11, "year": 2017},
                "starts_at": {"day": 1, "month": 9, "year": 2016},
            },
            {
                "company": "Baixing Co., Ltd.",
                "title": "Front End Engineer",
                "location": "Shanghai City, China",
                "ends_at": {"day": 31, "month": 8, "year": 2016},
                "starts_at": {"day": 1, "month": 10, "year": 2015},
            },
            {
                "company": "D.G.Z - GitCafe",
                "title": "Front End Engineer",
                "location": "Shanghai City, China",
                "ends_at": {"day": 30, "month": 6, "year": 2015},
                "starts_at": {"day": 1, "month": 7, "year": 2014},
            },
        ]
        assert calculate_total_experience(experiences) == 10
        
    def test_missing_property_raises_exception(self):
        incomplete_experiences = [
            {
                "company": "GovTech Singapore",
                "title": "Senior Software Engineer",
                "location": "Singapore",
                "ends_at": None,
                "starts_at": {"day": 1, "month": 9},  # Missing 'year'
            },
            {
                "company": "ASUS",
                "title": "Senior Software Engineer",
                "location": "Singapore",
                "ends_at": {"day": 31, "month": 7, "year": 2024},
                "starts_at": {"day": 1, "month": 10, "year": 2023},
            },
        ]

        with pytest.raises(ValueError, match="Missing or incomplete 'starts_at' property in experience."):
            calculate_total_experience(incomplete_experiences)

    def test_non_integer_property_raises_exception(self):
        invalid_experiences = [
            {
                "company": "GovTech Singapore",
                "title": "Senior Software Engineer",
                "location": "Singapore",
                "ends_at": None,
                "starts_at": {"day": 1, "month": "September", "year": 2024},  # Non-integer month
            },
            {
                "company": "ASUS",
                "title": "Senior Software Engineer",
                "location": "Singapore",
                "ends_at": {"day": 31, "month": 7, "year": 2024},
                "starts_at": {"day": 1, "month": 10, "year": 2023},
            },
        ]

        with pytest.raises(TypeError, match="'starts_at' properties 'day', 'month', and 'year' must be integers."):
            calculate_total_experience(invalid_experiences)
            
    def test_ends_at_none(self):
        experiences = [
            {
                "company": "GovTech Singapore",
                "title": "Senior Software Engineer",
                "location": "Singapore",
                "ends_at": None,
                "starts_at": {"day": 1, "month": 1, "year": 2022},
            }
        ]
        assert calculate_total_experience(experiences) >= 3  # Should calculate up to the current date

    def test_empty_experiences(self):
        experiences = []  # No experiences provided
        assert calculate_total_experience(experiences) == 0

    def test_overlapping_experiences(self):
        experiences = [
            {
                "company": "Company A",
                "title": "Engineer",
                "location": "Singapore",
                "ends_at": {"day": 31, "month": 12, "year": 2022},
                "starts_at": {"day": 1, "month": 1, "year": 2022},
            },
            {
                "company": "Company B",
                "title": "Engineer",
                "location": "Singapore",
                "ends_at": {"day": 31, "month": 12, "year": 2022},
                "starts_at": {"day": 1, "month": 6, "year": 2022},
            },
        ]
        assert calculate_total_experience(experiences) == 1  # Should count overlapping durations once

    def test_partial_dates(self):
        incomplete_experiences = [
            {
                "company": "Test Company",
                "title": "Engineer",
                "location": "Singapore",
                "starts_at": {"day": 1, "month": 1, "year": 2020},  
                "ends_at": {"month": 6, "year": 2022},  
            }
        ]

        with pytest.raises(ValueError, match="Missing or incomplete 'ends_at' property in experience."):
            calculate_total_experience(incomplete_experiences)

    def test_non_chronological_experiences(self):
        experiences = [
            {
                "company": "Company A",
                "title": "Engineer",
                "location": "Singapore",
                "ends_at": {"day": 31, "month": 12, "year": 2019},
                "starts_at": {"day": 1, "month": 1, "year": 2020},  # Invalid: starts after ends
            }
        ]

        with pytest.raises(ValueError, match="'starts_at' date must be earlier than 'ends_at' date."):
            calculate_total_experience(experiences)
