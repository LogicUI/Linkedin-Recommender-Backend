import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from datetime import date
from clean_profiles import _merge_date_ranges


class TestDateRanges:
    def test_date_ranges(self):
        from clean_profiles import _merge_date_ranges
        from datetime import date

        date_ranges = [
            (date(2020, 1, 1), date(2020, 1, 10)),
            (date(2020, 1, 11), date(2020, 1, 20)),
            (date(2020, 1, 21), date(2020, 1, 30)),
            (date(2020, 2, 1), date(2020, 2, 10)),
            (date(2020, 2, 11), date(2020, 2, 20)),
            (date(2020, 2, 21), date(2020, 2, 29)),
        ]
        assert _merge_date_ranges(date_ranges) == [
            (date(2020, 1, 1), date(2020, 1, 30)),
            (date(2020, 2, 1), date(2020, 2, 29)),
        ]

    def test_empty_input(self):
        assert _merge_date_ranges([]) == []

    def test_single_range(self):
        date_ranges = [(date(2023, 1, 1), date(2023, 1, 5))]
        assert _merge_date_ranges(date_ranges) == [(date(2023, 1, 1), date(2023, 1, 5))]

    def test_overlapping_ranges(self):
        date_ranges = [
            (date(2023, 1, 1), date(2023, 1, 10)),
            (date(2023, 1, 5), date(2023, 1, 15)),
        ]
        assert _merge_date_ranges(date_ranges) == [
            (date(2023, 1, 1), date(2023, 1, 15))
        ]

    def test_invalid_ranges(self):
        date_ranges = [
            (date(2023, 1, 10), date(2023, 1, 5)), 
            (date(2023, 1, 15), date(2023, 1, 20)),
        ]
        assert _merge_date_ranges(date_ranges) == [
            (date(2023, 1, 15), date(2023, 1, 20))
        ]

    def test_mixed_ranges(self):
        date_ranges = [
            (date(2023, 1, 1), date(2023, 1, 5)),
            (date(2023, 1, 10), date(2023, 1, 15)),
            (date(2023, 1, 5), date(2023, 1, 10)),
            (date(2023, 2, 1), date(2023, 2, 5)),
            (date(2023, 2, 3), date(2023, 2, 8)),
        ]
        assert _merge_date_ranges(date_ranges) == [
            (date(2023, 1, 1), date(2023, 1, 15)),
            (date(2023, 2, 1), date(2023, 2, 8)),
        ]

    def test_duplicate_ranges(self):
        date_ranges = [
            (date(2023, 1, 1), date(2023, 1, 5)),
            (date(2023, 1, 1), date(2023, 1, 5)),
            (date(2023, 1, 6), date(2023, 1, 10)),
        ]
        assert _merge_date_ranges(date_ranges) == [
            (date(2023, 1, 1), date(2023, 1, 10))
        ]

    def test_large_date_range(self):
        date_ranges = [
            (date(2020, 1, 1), date(2020, 12, 31)),
            (date(2020, 6, 1), date(2021, 6, 1)),
        ]
        assert _merge_date_ranges(date_ranges) == [(date(2020, 1, 1), date(2021, 6, 1))]

    def test_single_day_ranges(self):
        date_ranges = [
            (date(2023, 1, 1), date(2023, 1, 1)),
            (date(2023, 1, 2), date(2023, 1, 2)),
        ]
        assert _merge_date_ranges(date_ranges) == [(date(2023, 1, 1), date(2023, 1, 2))]

    def test_back_to_back_ranges(self):
        date_ranges = [
            (date(2023, 1, 1), date(2023, 1, 5)),
            (date(2023, 1, 6), date(2023, 1, 10)),
        ]
        assert _merge_date_ranges(date_ranges) == [
            (date(2023, 1, 1), date(2023, 1, 10))
        ]

    def test_unsorted_ranges(self):
        date_ranges = [
            (date(2023, 1, 10), date(2023, 1, 15)),
            (date(2023, 1, 1), date(2023, 1, 5)),
            (date(2023, 1, 5), date(2023, 1, 10)),
        ]

        assert _merge_date_ranges(date_ranges) == [
            (date(2023, 1, 1), date(2023, 1, 15))
        ]
