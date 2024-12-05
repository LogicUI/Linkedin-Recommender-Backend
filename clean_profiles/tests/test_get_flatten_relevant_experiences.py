import sys
import os
import pytest
from datetime import date

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from clean_profiles import _get_flatten_relevant_experiences


class TestFlattenRelevantExperiences:
    def test_valid_experience_data(self):
        experiences = [
            {
                "ends_at": None,
                "title": "AI Engineer",
                "location": None,
                "starts_at": {"day": 1, "month": 5, "year": 2019},
                "company": "GovTech Singapore",
            },
            {
                "ends_at": {"day": 30, "month": 4, "year": 2019},
                "title": "Senior Software Engineer",
                "location": None,
                "starts_at": {"day": 1, "month": 1, "year": 2019},
                "company": "IHiS (Integrated Health Information Systems)",
            },
            {
                "ends_at": {"day": 31, "month": 12, "year": 2017},
                "title": "Senior Software Engineer",
                "location": "Singapore",
                "starts_at": {"day": 1, "month": 7, "year": 2017},
                "company": "IHiS (Integrated Health Information Systems)",
            },
            {
                "ends_at": {"day": 31, "month": 7, "year": 2017},
                "title": "Software Engineer",
                "location": None,
                "starts_at": {"day": 1, "month": 1, "year": 2015},
                "company": "IHiS (Integrated Health Information Systems)",
            },
        ]

        assert (
            _get_flatten_relevant_experiences(experiences)
            == "AI Engineer at GovTech Singapore from May 2019 to Dec 2024; Senior Software Engineer at IHiS (Integrated Health Information Systems) from Jan 2019 to Apr 2019; Senior Software Engineer at IHiS (Integrated Health Information Systems) from Jul 2017 to Dec 2017; Software Engineer at IHiS (Integrated Health Information Systems) from Jan 2015 to Jul 2017;"
        )

    def test_empty_experiences(self):
        experiences = []
        assert _get_flatten_relevant_experiences(experiences) == ""

    def test_single_experience_with_valid_start_and_end(self):
        experiences = [
            {
                "ends_at": {"day": 30, "month": 4, "year": 2019},
                "title": "Senior Software Engineer",
                "location": None,
                "starts_at": {"day": 1, "month": 1, "year": 2019},
                "company": "IHiS (Integrated Health Information Systems)",
            }
        ]

        assert (
            _get_flatten_relevant_experiences(experiences)
            == "Senior Software Engineer at IHiS (Integrated Health Information Systems) from Jan 2019 to Apr 2019;"
        )

    def test_multiple_experiences_with_valid_start_and_end(self):
        experiences = [
            {
                "title": "Software Engineer",
                "company": "TechCorp",
                "starts_at": {"year": 2022, "month": 5},
                "ends_at": {"year": 2023, "month": 8},
            },
            {
                "title": "Data Scientist",
                "company": "DataCo",
                "starts_at": {"year": 2019, "month": 2},
                "ends_at": {"year": 2021, "month": 10},
            },
        ]

        assert (
            _get_flatten_relevant_experiences(experiences)
            == "Software Engineer at TechCorp from May 2022 to Aug 2023; Data Scientist at DataCo from Feb 2019 to Oct 2021;"
        )

    def test_single_experience_with_valid_dates(self):
        experiences = [
            {
                "title": "Software Engineer",
                "company": "TechCorp",
                "starts_at": {"year": 2022, "month": 5},
                "ends_at": {"year": 2023, "month": 8},
            }
        ]
        expected = "Software Engineer at TechCorp from May 2022 to Aug 2023;"
        assert _get_flatten_relevant_experiences(experiences) == expected

    def test_multiple_experiences_with_valid_dates(self):
        experiences = [
            {
                "title": "Software Engineer",
                "company": "TechCorp",
                "starts_at": {"year": 2022, "month": 5},
                "ends_at": {"year": 2023, "month": 8},
            },
            {
                "title": "Data Scientist",
                "company": "DataCo",
                "starts_at": {"year": 2019, "month": 2},
                "ends_at": {"year": 2021, "month": 10},
            },
        ]
        expected = "Software Engineer at TechCorp from May 2022 to Aug 2023; Data Scientist at DataCo from Feb 2019 to Oct 2021;"
        assert _get_flatten_relevant_experiences(experiences) == expected

    def test_experience_with_missing_end_date(self):
        experiences = [
            {
                "title": "Software Engineer",
                "company": "TechCorp",
                "starts_at": {"year": 2022, "month": 5},
            }
        ]
        expected = f"Software Engineer at TechCorp from May 2022 to {date.today().strftime('%b %Y')};"
        assert _get_flatten_relevant_experiences(experiences) == expected

    def test_experience_with_missing_start_date(self):
        experiences = [{"title": "Software Engineer", "company": "TechCorp"}]
        # Adjust to the appropriate exception
        assert (
            _get_flatten_relevant_experiences(experiences)
            == "Software Engineer at TechCorp from Dec 2024 to Dec 2024;"
        )

    def test_experience_with_invalid_date_fields(self):
        experiences = [
            {
                "title": "Software Engineer",
                "company": "TechCorp",
                "starts_at": {"year": 2022, "month": 13},
                "ends_at": {"year": 2023, "month": 8},
            }
        ]
        with pytest.raises(ValueError):  # Adjust to the appropriate exception
            _get_flatten_relevant_experiences(experiences)

    def test_experience_with_start_date_after_end_date(self):
        experiences = [
            {
                "title": "Software Engineer",
                "company": "TechCorp",
                "starts_at": {"year": 2023, "month": 8},
                "ends_at": {"year": 2022, "month": 5},
            }
        ]
        # Depending on business logic, either assert an error or check for incorrect output
        with pytest.raises(ValueError):
            _get_flatten_relevant_experiences(experiences)

    def test_experience_with_unexpected_data_types(self):
        experiences = [
            {
                "title": "Software Engineer",
                "company": "TechCorp",
                "starts_at": "May 2022",
                "ends_at": "Aug 2023",
            }
        ]
        with pytest.raises(TypeError):  # Adjust to the appropriate exception
            _get_flatten_relevant_experiences(experiences)

    def test_experience_with_large_year_values(self):
        experiences = [
            {
                "title": "Software Engineer",
                "company": "TechCorp",
                "starts_at": {"year": 9999, "month": 12},
                "ends_at": {"year": 10000, "month": 1},
            }
        ]
        with pytest.raises(ValueError):
            _get_flatten_relevant_experiences(experiences) == expected

    def test_experience_with_null_values_in_dates(self):
        experiences = [
            {
                "title": "Software Engineer",
                "company": "TechCorp",
                "starts_at": {"year": None, "month": None},
            }
        ]
        with pytest.raises(TypeError):  # Adjust to the appropriate exception
            _get_flatten_relevant_experiences(experiences)

