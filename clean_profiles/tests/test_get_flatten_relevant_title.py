import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from clean_profiles import _get_flatten_relevant_fields

class TestFlattenRelevantTitle:
    def test_flatten_relevant_fields_title(self):
        experiences = [
            {
                "starts_at": {"day": 1, "month": 9, "year": 2024},
                "ends_at": None,
                "company": "GovTech Singapore",
                "title": "Senior Software Engineer",
            },
            {
                "starts_at": {"day": 1, "month": 10, "year": 2023},
                "ends_at": {"day": 31, "month": 7, "year": 2024},
                "company": "ASUS",
                "title": "Senior Software Engineer",
            },
            {
                "starts_at": {"day": 1, "month": 3, "year": 2022},
                "ends_at": {"day": 31, "month": 5, "year": 2023},
                "company": "Indeed.com",
                "title": "Software Engineer II",
            },
            {
                "starts_at": {"day": 1, "month": 2, "year": 2021},
                "ends_at": {"day": 28, "month": 2, "year": 2022},
                "company": "Garena",
                "title": "Senior Software Engineer",
            },
            {
                "starts_at": {"day": 1, "month": 2, "year": 2020},
                "ends_at": {"day": 28, "month": 2, "year": 2021},
                "company": "Garena",
                "title": "Software Engineer",
            },
            {
                "starts_at": {"day": 1, "month": 11, "year": 2017},
                "ends_at": {"day": 31, "month": 1, "year": 2020},
                "company": "Upwork",
                "title": "Software Engineer",
            },
            {
                "starts_at": {"day": 1, "month": 9, "year": 2016},
                "ends_at": {"day": 30, "month": 11, "year": 2017},
                "company": "Autodesk",
                "title": "Software Engineer",
            },
            {
                "starts_at": {"day": 1, "month": 10, "year": 2015},
                "ends_at": {"day": 31, "month": 8, "year": 2016},
                "company": "Baixing Co., Ltd.",
                "title": "Front End Engineer",
            },
            {
                "starts_at": {"day": 1, "month": 7, "year": 2014},
                "ends_at": {"day": 30, "month": 6, "year": 2015},
                "company": "D.G.Z - GitCafe",
                "title": "Front End Engineer",
            },
        ]

        result = _get_flatten_relevant_fields(
            dict_list=experiences,
            between_words=" ",
            title="title",
        )

        assert (
            result
            == "Senior Software Engineer; Software Engineer II; Software Engineer; Front End Engineer;"
        )

    def test_flatten_relevant_fields_empty_list(self):
        experiences = []

        result = _get_flatten_relevant_fields(
            dict_list=experiences,
            between_words=" ",
            title="title",
        )

        assert result == ""

    def test_flatten_relevant_fields_missing_title(self):
        experiences = [
            {
                "starts_at": {"day": 1, "month": 9, "year": 2024},
                "ends_at": None,
                "company": "GovTech Singapore",
            },
            {
                "starts_at": {"day": 1, "month": 3, "year": 2022},
                "ends_at": {"day": 31, "month": 5, "year": 2023},
                "company": "Indeed.com",
                "title": "Software Engineer II",
            },
        ]

        result = _get_flatten_relevant_fields(
            dict_list=experiences,
            between_words=" ",
            title="title",
        )

        assert result == "Software Engineer II;"

    def test_flatten_relevant_fields_duplicates_title(self):
        experiences = [
            {
                "starts_at": {"day": 1, "month": 9, "year": 2024},
                "ends_at": None,
                "company": "GovTech Singapore",
                "title": "Senior Software Engineer",
            },
            {
                "starts_at": {"day": 1, "month": 10, "year": 2023},
                "ends_at": {"day": 31, "month": 7, "year": 2024},
                "company": "ASUS",
                "title": "Senior Software Engineer",
            },
        ]

        result = _get_flatten_relevant_fields(
            dict_list=experiences,
            between_words=" ",
            title="title",
        )

        assert result == "Senior Software Engineer;"

    def test_flatten_relevant_fields_mixed_entries_title(self):
        experiences = [
            {
                "starts_at": {"day": 1, "month": 9, "year": 2024},
                "ends_at": None,
                "company": "GovTech Singapore",
                "title": "Senior Software Engineer",
            },
            {
                "starts_at": {"day": 1, "month": 3, "year": 2022},
                "ends_at": {"day": 31, "month": 5, "year": 2023},
                "company": "Indeed.com",
            },
            {
                "starts_at": {"day": 1, "month": 10, "year": 2015},
                "ends_at": {"day": 31, "month": 8, "year": 2016},
                "company": "Baixing Co., Ltd.",
                "title": "Front End Engineer",
            },
        ]

        result = _get_flatten_relevant_fields(
            dict_list=experiences,
            between_words=" ",
            title="title",
        )

        assert result == "Senior Software Engineer; Front End Engineer;"

    def test_flatten_relevant_fields_mixed_entries_titles(self):
        experiences = [
            {
                "starts_at": {"day": 1, "month": 9, "year": 2024},
                "ends_at": None,
                "company": "GovTech Singapore",
                "title": "Senior Software Engineer",
            },
            {
                "starts_at": {"day": 1, "month": 3, "year": 2022},
                "ends_at": {"day": 31, "month": 5, "year": 2023},
                "company": "Indeed.com",
            },
            {
                "starts_at": {"day": 1, "month": 10, "year": 2015},
                "ends_at": {"day": 31, "month": 8, "year": 2016},
                "company": "Baixing Co., Ltd.",
                "title": "Front End Engineer",
            },
        ]

        result = _get_flatten_relevant_fields(
            dict_list=experiences,
            between_words=" ",
            title="title",
        )

        assert result == "Senior Software Engineer; Front End Engineer;"

    def test_flatten_relevant_fields_irrelevant_fields(self):
        experiences = [
            {
                "starts_at": {"day": 1, "month": 9, "year": 2024},
                "ends_at": None,
                "company": "GovTech Singapore",
                "title": "Senior Software Engineer",
                "location": "Singapore",
            },
            {
                "starts_at": {"day": 1, "month": 3, "year": 2022},
                "ends_at": {"day": 31, "month": 5, "year": 2023},
                "company": "Indeed.com",
                "title": "Software Engineer II",
                "department": "Engineering",
            },
        ]

        result = _get_flatten_relevant_fields(
            dict_list=experiences,
            between_words=" ",
            title="title",
        )

        assert result == "Senior Software Engineer; Software Engineer II;"

    def test_flatten_relevant_fields_no_titles(self):
        experiences = [
            {
                "starts_at": {"day": 1, "month": 9, "year": 2024},
                "ends_at": None,
                "company": "GovTech Singapore",
                "location": "Singapore",
            },
            {
                "starts_at": {"day": 1, "month": 3, "year": 2022},
                "ends_at": {"day": 31, "month": 5, "year": 2023},
                "company": "Indeed.com",
                "department": "Engineering",
            },
        ]

        result = _get_flatten_relevant_fields(
            dict_list=experiences,
            between_words=" ",
            title="title",
        )

        assert result == ""

    def test_flatten_relevant_fields_with_delimiter(self):
        experiences = [
            {
                "starts_at": {"day": 1, "month": 9, "year": 2024},
                "ends_at": None,
                "company": "GovTech Singapore",
                "title": "Senior Software Engineer",
            },
            {
                "starts_at": {"day": 1, "month": 3, "year": 2022},
                "ends_at": {"day": 31, "month": 5, "year": 2023},
                "company": "Indeed.com",
                "title": "Software Engineer II",
            },
        ]

        result = _get_flatten_relevant_fields(
            dict_list=experiences,
            between_words=", ",
            title="title",
        )

        assert result == "Senior Software Engineer; Software Engineer II;"
