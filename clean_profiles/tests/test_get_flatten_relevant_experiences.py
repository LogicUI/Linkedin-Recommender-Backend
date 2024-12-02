import sys
import os
import pytest

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

        assert _get_flatten_relevant_experiences(experiences) == "AI Engineer at GovTech Singapore from May 2019 to Dec 2024; Senior Software Engineer at IHiS (Integrated Health Information Systems) from Jan 2019 to Apr 2019; Senior Software Engineer at IHiS (Integrated Health Information Systems) from Jul 2017 to Dec 2017; Software Engineer at IHiS (Integrated Health Information Systems) from Jan 2015 to Jul 2017;"

  