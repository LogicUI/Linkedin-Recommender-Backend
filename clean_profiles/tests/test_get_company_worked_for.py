import sys
import os
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from clean_profiles import _get_company_worked_for

class TestCompanyWorkedFor:
    def test_valid_input(self):
        experiences = [
            {"company": "Company A"},
            {"company": "Company B"},
            {"company": "Company C"},
        ]
        expected = ["Company A", "Company B", "Company C"]
        assert _get_company_worked_for(experiences) == expected

    def test_empty_list(self):
        experiences = []
        expected = []
        assert _get_company_worked_for(experiences) == expected

    def test_missing_company_key(self):
        experiences = [
            {"role": "Developer"},
            {"company": "Company A"},
            {"position": "Manager"},
        ]
        expected = ["Company A"]
        assert _get_company_worked_for(experiences) == expected

    def test_non_list_input(self):
        with pytest.raises(TypeError, match="Expected a list of experiences."):
            _get_company_worked_for("not a list")

    def test_non_dict_element(self):
        experiences = [
            {"company": "Company A"},
            ["not a dictionary"],
            {"company": "Company B"},
        ]
        with pytest.raises(TypeError, match="Each experience must be a dictionary."):
            _get_company_worked_for(experiences)

    def test_nested_structure_as_company_value(self):
        experiences = [
            {"company": {"nested": "value"}},
            {"company": "Company A"},
        ]
        with pytest.raises(TypeError, match="Expected 'company' to be a string, got <class 'dict'>."):
            _get_company_worked_for(experiences)

    def test_empty_dictionaries(self):
        experiences = [
            {},
            {"company": "Company A"},
            {},
        ]
        expected = ["Company A"]
        assert _get_company_worked_for(experiences) == expected

    def test_company_is_none(self):
        experiences = [
            {"company": None},
            {"company": "Company A"},
            {"company": "Company B"},
        ]
        expected = ["Company A", "Company B"]
        assert _get_company_worked_for(experiences) == expected

    def test_company_is_non_string_value(self):
        experiences = [
            {"company": 123},  
            {"company": "Company A"},
        ]
        with pytest.raises(TypeError, match="Expected 'company' to be a string, got <class 'int'>."):
            _get_company_worked_for(experiences)

    def test_company_is_empty_string(self):
        experiences = [
            {"company": ""},
            {"company": "Company A"},
        ]
        expected = ["Company A"]
        assert _get_company_worked_for(experiences) == expected
        
    def test_duplicate(self):
        experiences = [
            {"company": "CompanyA"},
            {"company": "CompanyB"},
            {"company": "CompanyA"},  
            {"company": " CompanyC "}, 
        ]
        expected = ["CompanyA", "CompanyB", "CompanyC"]
        assert _get_company_worked_for(experiences) ==  expected 
