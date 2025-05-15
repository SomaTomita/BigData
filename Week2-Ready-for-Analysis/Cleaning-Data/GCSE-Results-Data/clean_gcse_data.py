import pandas as pd
from datetime import datetime
import numpy as np


def clean_gcse_data(input_file):
    # Read the ARFF file
    # Skip the ARFF header (lines starting with @)
    with open(input_file, "r") as f:
        lines = f.readlines()
        data_start = [i for i, line in enumerate(lines) if line.strip() == "@data"][
            0
        ] + 1
        data_lines = [line.strip() for line in lines[data_start:]]

    # Convert to DataFrame
    df = pd.DataFrame([line.split(",") for line in data_lines])
    df.columns = ["firstname", "lastname", "gender", "dob", "auth"] + sum(
        [[f"subject{i}", f"grade{i}"] for i in range(1, 6)], []
    )

    # Clean names
    df["firstname"] = df["firstname"].replace("", "UNKNOWN")
    df["lastname"] = df["lastname"].replace("", "UNKNOWN")

    # Clean gender
    gender_map = {"m": "M", "f": "F", "x": "O", "mf": "U", "": "U"}  # Flag for review
    df["gender"] = df["gender"].map(lambda x: gender_map.get(x.strip(), "U"))

    # Clean dates
    def standardize_date(date_str):
        date_str = date_str.strip()
        try:
            # Try different date formats
            for fmt in ["%Y/%m/%d", "%d/%m/%Y", "%Y/%b/%d"]:
                try:
                    return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
                except ValueError:
                    continue
            return "Invalid Date"
        except:
            return "Invalid Date"

    df["dob"] = df["dob"].map(standardize_date)

    # Clean grades
    def standardize_grade(grade):
        grade = str(grade).strip()
        if grade in ["A*", "A+", "A", "B", "C", "D", "E", "F", "G", "U"]:
            return grade
        if grade.isdigit() and 0 <= int(grade) <= 7:
            # Map numeric grades to letters (simplified mapping)
            grade_map = {7: "A", 6: "B", 5: "C", 4: "D", 3: "E", 2: "F", 1: "G", 0: "U"}
            return grade_map[int(grade)]
        if grade in ["", " "]:
            return "NA"
        return "Invalid"

    for i in range(1, 6):
        df[f"grade{i}"] = df[f"grade{i}"].map(standardize_grade)

    # Clean subjects
    def clean_subject(subject):
        if pd.isna(subject) or subject.strip() in ["", " "]:
            return "NA"
        # Remove quotes and standardize
        return subject.strip().strip("'")

    for i in range(1, 6):
        df[f"subject{i}"] = df[f"subject{i}"].map(clean_subject)

    # Flag duplicate subjects per student
    def flag_duplicates(row):
        subjects = [row[f"subject{i}"] for i in range(1, 6)]
        subjects = [s for s in subjects if s != "NA"]
        if len(subjects) != len(set(subjects)):
            return True
        return False

    df["has_duplicate_subjects"] = df.apply(flag_duplicates, axis=1)

    return df


def main():
    # Input and output files
    input_file = "Week2-Ready-for-Analysis/Cleaning-Data/GCSE-Results-Data/gcse.arff"
    output_file = (
        "Week2-Ready-for-Analysis/Cleaning-Data/GCSE-Results-Data/gcse_cleaned.csv"
    )

    # Clean data
    cleaned_df = clean_gcse_data(input_file)

    # Save cleaned data
    cleaned_df.to_csv(output_file, index=False)

    # Print summary
    print(f"Data cleaning completed. Output saved to {output_file}")
    print("\nSummary:")
    print(f"Total records: {len(cleaned_df)}")
    print(
        f"Records with unknown names: {len(cleaned_df[cleaned_df['firstname'] == 'UNKNOWN'])}"
    )
    print(
        f"Records with invalid dates: {len(cleaned_df[cleaned_df['dob'] == 'Invalid Date'])}"
    )
    print(
        f"Records with invalid grades: {len(cleaned_df[cleaned_df.filter(like='grade').eq('Invalid').any(axis=1)])}"
    )
    print(
        f"Records with duplicate subjects: {len(cleaned_df[cleaned_df['has_duplicate_subjects']])}"
    )


if __name__ == "__main__":
    main()
