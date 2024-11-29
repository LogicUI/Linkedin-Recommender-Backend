import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from clean_profiles import _get_relevant_experiences
import pytest

class TestRelevantExperience:
    def test_correct_relevant_experiences(self):
        experiences =  [
                {
                    "starts_at": {"day": 1, "month": 12, "year": 2015},
                    "ends_at": None,
                    "company": "GovTech Singapore",
                    "company_linkedin_profile_url": "https://www.linkedin.com/company/govtech-singapore",
                    "company_facebook_profile_url": None,
                    "title": "Software Engineer",
                    "description": None,
                    "location": None,
                    "logo_url": "https://s3.us-west-000.backblazeb2.com/proxycurl/company/govtech-singapore/profile?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=0004d7f56a0400b0000000001%2F20241103%2Fus-west-000%2Fs3%2Faws4_request&X-Amz-Date=20241103T090328Z&X-Amz-Expires=1800&X-Amz-SignedHeaders=host&X-Amz-Signature=85e017b96339e08d86370acbcd20a0bb4accf1973656e8839e016c13924fa715",
                },
                {
                    "starts_at": {"day": 1, "month": 1, "year": 2015},
                    "ends_at": {"day": 31, "month": 7, "year": 2015},
                    "company": "Infocomm Development Authority of Singapore",
                    "company_linkedin_profile_url": "https://www.linkedin.com/company/govtech-singapore",
                    "company_facebook_profile_url": None,
                    "title": "Intern",
                    "description": None,
                    "location": None,
                    "logo_url": "https://s3.us-west-000.backblazeb2.com/proxycurl/company/govtech-singapore/profile?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=0004d7f56a0400b0000000001%2F20241103%2Fus-west-000%2Fs3%2Faws4_request&X-Amz-Date=20241103T090328Z&X-Amz-Expires=1800&X-Amz-SignedHeaders=host&X-Amz-Signature=85e017b96339e08d86370acbcd20a0bb4accf1973656e8839e016c13924fa715",
                }]
        
        
        assert _get_relevant_experiences(experiences) == [
            {
                "starts_at": {"day": 1, "month": 12, "year": 2015},
                "ends_at": None,
                "company": "GovTech Singapore",
                "title": "Software Engineer",
                "location": None,
            },
            {
                "starts_at": {"day": 1, "month": 1, "year": 2015},
                "ends_at": {"day": 31, "month": 7, "year": 2015},
                "company": "Infocomm Development Authority of Singapore",
                "title": "Intern",
                "location": None,
            },
        ]
        
        
    def test_no_experiences(self):
        experiences = []
        assert _get_relevant_experiences(experiences) == []

    def test_partial_information(self):
        experiences = [
            {
                "starts_at": {"day": 1, "month": 1, "year": 2020},
                "ends_at": None,
                "company": "Tech Co",
                "title": None,
                "description": None,
                "location": None,
            }
        ]
        assert _get_relevant_experiences(experiences) == [
            {
                "starts_at": {"day": 1, "month": 1, "year": 2020},
                "ends_at": None,
                "company": "Tech Co",
                "title": None,
                "location": None,
            }
        ]

    def test_missing_dates(self):
        experiences = [
            {
                "starts_at": None,
                "ends_at": None,
                "company": "Startup Inc",
                "title": "Developer",
                "description": None,
                "location": "Remote",
            }
        ]
        assert _get_relevant_experiences(experiences) == [
            {
                "starts_at": None,
                "ends_at": None,
                "company": "Startup Inc",
                "title": "Developer",
                "location": "Remote",
            }
        ]

    def test_experiences_with_duplicate_data(self):
        experiences = [
            {
                "starts_at": {"day": 1, "month": 6, "year": 2021},
                "ends_at": None,
                "company": "Duplicated Co",
                "title": "Engineer",
                "description": None,
                "location": "Singapore",
            },
            {
                "starts_at": {"day": 1, "month": 6, "year": 2021},
                "ends_at": None,
                "company": "Duplicated Co",
                "title": "Engineer",
                "description": None,
                "location": "Singapore",
            },
        ]
        assert _get_relevant_experiences(experiences) == [
            {
                "starts_at": {"day": 1, "month": 6, "year": 2021},
                "ends_at": None,
                "company": "Duplicated Co",
                "title": "Engineer",
                "location": "Singapore",
            },
            {
                "starts_at": {"day": 1, "month": 6, "year": 2021},
                "ends_at": None,
                "company": "Duplicated Co",
                "title": "Engineer",
                "location": "Singapore",
            },
        ]
        
    def test_get_relevant_experiences_raises_value_error(self):
        incomplete_experiences = [
            {
                "starts_at": {"day": 1, "month": 1, "year": 2020},
                "company": "Tech Co",
            }
        ]
        
        with pytest.raises(ValueError, match=r"Missing keys in experience: .*"):
            _get_relevant_experiences(incomplete_experiences)
