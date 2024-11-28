import json
import os
from datetime import date, timedelta


def round_to_nearest_year(years, months, days):
    fractional_year = months / 12 + days / 365
    rounded_years = round(years + fractional_year)
    return rounded_years


def merge_date_ranges(date_ranges):
    date_ranges.sort()
    merged_ranges = []

    for start, end in date_ranges:
        if not merged_ranges or merged_ranges[-1][1] < start - timedelta(days=1):
            merged_ranges.append((start, end))
        else:
            merged_ranges[-1] = (merged_ranges[-1][0], max(merged_ranges[-1][1], end))

    return merged_ranges


def calculate_total_experience(experiences):
    total_days = 0
    today = date.today()
    date_ranges = []

    for experience in experiences:
        if "starts_at" not in experience or not all(
            key in experience["starts_at"] for key in ["day", "month", "year"]
        ):
            raise ValueError(
                "Missing or incomplete 'starts_at' property in experience."
            )

        start = experience["starts_at"]

        if not all(isinstance(start[key], int) for key in ["day", "month", "year"]):
            raise TypeError(
                "'starts_at' properties 'day', 'month', and 'year' must be integers."
            )

        start_date = date(start["year"], start["month"], start["day"])

        if experience["ends_at"] is not None:
            if not all(
                key in experience["ends_at"] for key in ["day", "month", "year"]
            ):
                raise ValueError(
                    "Missing or incomplete 'ends_at' property in experience."
                )

            end = experience["ends_at"]
            if not all(isinstance(end[key], int) for key in ["day", "month", "year"]):
                raise TypeError(
                    "'ends_at' properties 'day', 'month', and 'year' must be integers."
                )

            end_date = date(end["year"], end["month"], end["day"])
        else:
            end_date = today

        if start_date > end_date:
            raise ValueError("'starts_at' date must be earlier than 'ends_at' date.")

        date_ranges.append((start_date, end_date))

    merged_ranges = merge_date_ranges(date_ranges)

    total_days = sum((end - start).days + 1 for start, end in merged_ranges)

    total_years = round(total_days / 365, 0)

    return total_years


def get_relevant_experieinces(experiences):
    experience_fields_to_keep = {"starts_at", "ends_at", "company", "title", "location"}
    relevant_experiences = [
        {key: experience[key] for key in experience_fields_to_keep if key in experience}
        for experience in experiences
    ]
    return relevant_experiences


def get_relevant_profile_fields(profile):
    fields_to_keep = {
        "profile_url",
        "full_name",
        "current_occupation",
        "country_full_name",
        "certifications",
        "personal_emails",
    }
    return {key: profile[key] for key in fields_to_keep if key in profile}


def get_companies_worked_for(experiences: list[dict]) -> list[str]:
    return [experience["company"] for experience in experiences]


def get_relevant_educations(education: list[dict]) -> list[dict]:
    education_fields_to_keep = {"degree_name", "school"}
    return [
        {key: edu[key] for key in education_fields_to_keep if key in edu}
        for edu in education
    ]


def extract_relavant_profile_properties(profile_name: dict) -> dict:
    with open(profile_name, "r") as file:
        data = json.load(file)

        experiences = data.get("experiences", [])
        education = data.get("education", [])

        relevant_experiences = get_relevant_experieinces(experiences)
        relevant_profile_fields = get_relevant_profile_fields(data)
        companies_worked_for = get_companies_worked_for(relevant_experiences)
        total_experiences = calculate_total_experience(relevant_experiences)
        relevant_educations = get_relevant_educations(education)

        profile_details = {
            "experience_details": relevant_experiences,
            "companies_worked_for": companies_worked_for,
            "total_experieinces": total_experiences,
            "education": relevant_educations,
            **relevant_profile_fields,
        }

        return profile_details


if __name__ == "__main__":
    extract_relavant_profile_properties("profile_2.json")
