import json
from datetime import date, timedelta
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from logger_setup import setup_logger

logger = setup_logger(__name__)


def _merge_date_ranges(date_ranges: list[tuple[date, date]]) -> list[tuple[date, date]]:
    if not date_ranges:
        return []

    date_ranges = [(start, end) for start, end in date_ranges if start <= end]

    date_ranges.sort(key=lambda x: (x[0], x[1]))
    merged_ranges = []

    for start, end in date_ranges:
        if not merged_ranges or merged_ranges[-1][1] < start - timedelta(days=1):
            merged_ranges.append((start, end))
        else:
            merged_ranges[-1] = (merged_ranges[-1][0], max(merged_ranges[-1][1], end))

    return merged_ranges


def _calculate_total_experiences(experiences: list[dict]) -> int:
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

    merged_ranges = _merge_date_ranges(date_ranges)

    total_days = sum((end - start).days + 1 for start, end in merged_ranges)

    total_years = round(total_days / 365, 0)

    return total_years


def _get_relevant_experiences(experiences: list[dict]) -> list[dict]:
    experience_fields_to_keep = {"starts_at", "ends_at", "company", "title", "location"}
    relevant_experiences = []
    for experience in experiences:
        missing_keys = experience_fields_to_keep - experience.keys()
        if missing_keys:
            raise ValueError(f"Missing keys in experience: {missing_keys}")
        relevant_experiences.append(
            {key: experience[key] for key in experience_fields_to_keep}
        )

    return relevant_experiences


def _get_flatten_relevant_experiences(experiences: list[dict]) -> str:
    experiences_field = ""
    for experience in experiences:
        start_date = experience.get("starts_at", None)
        starting_date = (
            date.today()
            if start_date is None
            else date(start_date["year"], start_date["month"], 1)
        )
        start_date_format = starting_date.strftime("%b %Y")
        end_date = experience.get("ends_at", None)
        ending_date = (
            date.today()
            if end_date is None
            else date(end_date["year"], end_date["month"], 1)
        )
        end_date_format = ending_date.strftime("%b %Y")

        if starting_date > ending_date:
            raise ValueError("Start date must be earlier than end date.")

        experience_str = f"{experience['title']} at {experience['company']} from {start_date_format} to {end_date_format};"
        experiences_field += experience_str + " "
    logger.info(f"Experiences: {experiences_field}")
    return experiences_field.strip()


def _get_relevant_profile_files(profile: dict) -> dict:
    fields_to_keep = {
        "profile_url",
        "full_name",
        "current_occupation",
        "country_full_name",
        "certifications",
        "personal_emails",
    }

    if not isinstance(profile, dict):
        raise ValueError("Expected 'profile' to be a dictionary.")

    relevant_profile = {key: profile[key] for key in fields_to_keep if key in profile}

    if "full_name" not in relevant_profile or not relevant_profile["full_name"].strip():
        relevant_profile["full_name"] = "Unknown"

    if "personal_emails" not in relevant_profile or not isinstance(
        relevant_profile["personal_emails"], list
    ):
        relevant_profile["personal_emails"] = []

    return relevant_profile


def _get_company_worked_for(experiences: list[dict]) -> list[str]:
    if not isinstance(experiences, list):
        raise TypeError("Expected a list of experiences.")

    companies = set()
    for experience in experiences:
        if not isinstance(experience, dict):
            raise TypeError("Each experience must be a dictionary.")

        company = experience.get("company", None)
        if isinstance(company, str):
            if company.strip():
                companies.add(company.strip())
        elif company is not None:
            raise TypeError(f"Expected 'company' to be a string, got {type(company)}.")

    return sorted(companies)


def _get_relevant_education(education: list[dict]) -> list[dict]:
    education_fields_to_keep = {"degree_name", "school"}

    if not isinstance(education, list):
        return []

    relevant_education = []
    for edu in education:
        if isinstance(edu, dict):
            filtered_edu = {
                key: edu[key] for key in education_fields_to_keep if key in edu
            }
            if filtered_edu:
                relevant_education.append(filtered_edu)

    return relevant_education


def extract_relavant_profile_properties(profile_name: dict) -> dict:
    with open(profile_name, "r") as file:
        data = json.load(file)

        experiences = data.get("experiences", [])
        education = data.get("education", [])

        relevant_experiences = _get_relevant_experiences(experiences)
        relevant_profile_fields = _get_relevant_profile_files(data)
        companies_worked_for = _get_company_worked_for(relevant_experiences)
        total_experiences = _calculate_total_experiences(relevant_experiences)
        relevant_educations = _get_relevant_education(education)

        profile_details = {
            "experience_details": relevant_experiences,
            "companies_worked_for": companies_worked_for,
            "total_experieinces": total_experiences,
            "education": relevant_educations,
            **relevant_profile_fields,
        }

        return profile_details


def process_folder(input_folder: str, output_folder: str):
    os.makedirs(output_folder, exist_ok=True)
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".json"):
            input_file_path = os.path.join(input_folder, file_name)
            try:
                processed_data = extract_relavant_profile_properties(input_file_path)
                output_file_path = os.path.join(output_folder, file_name)
                with open(output_file_path, "w") as output_file:
                    json.dump(processed_data, output_file, indent=4)
                logger.info(f"Processed and saved: {output_file_path}")
            except Exception as e:
                logger.error(f"Error processing {file_name}: {e}")


if __name__ == "__main__":
    process_folder("./data", "./processed_data")
