# Import packages
from census import Census
import pandas as pd
import numpy as np
import os

# Connect to the Census API
API_KEY = "your_API_key_here"
c = Census(API_KEY)


# Retrieve 5-year ACS data for all U.S. states
# Includes population, median household income, and educational attainment
data = c.acs5.get(
    (
        "NAME",
        "B01003_001E",  # Total population
        "B15003_001E",  # Total population age 25+
        "B19013_001E",  # Median household income

        # Educational attainment: Population age 25+
        "B15003_002E",  # No schooling completed
        "B15003_003E",  # Nursery school
        "B15003_004E",  # Kindergarten
        "B15003_005E",  # 1st grade
        "B15003_006E",  # 2nd grade
        "B15003_007E",  # 3rd grade
        "B15003_008E",  # 4th grade
        "B15003_009E",  # 5th grade
        "B15003_010E",  # 6th grade
        "B15003_011E",  # 7th grade
        "B15003_012E",  # 8th grade
        "B15003_013E",  # 9th grade
        "B15003_014E",  # 10th grade
        "B15003_015E",  # 11th grade
        "B15003_016E",  # 12th grade, no diploma
        "B15003_017E",  # Regular high school diploma
        "B15003_018E",  # GED or alternative credential
        "B15003_019E",  # Some college, less than 1 year
        "B15003_020E",  # Some college, 1 or more years, no degree
        "B15003_021E",  # Associate's degree
        "B15003_022E",  # Bachelor's degree
        "B15003_023E",  # Master's degree
        "B15003_024E",  # Professional school degree
        "B15003_025E",  # Doctorate degree
    ),
    {"for": "state:*"}
)


# Convert API results into a DataFrame
df = pd.DataFrame(data)

# Remove the state FIPS code column
df = df.drop(columns=["state"])

# Rename columns for readability
df = df.rename(columns={
    "NAME": "state",
    "B01003_001E": "total_pop",
    "B15003_001E": "adults_25_plus",
    "B19013_001E": "median_income",
    "B15003_002E": "no_schooling_count",
    "B15003_003E": "nursery_count",
    "B15003_004E": "kindergarten_count",
    "B15003_005E": "first_grade_count",
    "B15003_006E": "second_grade_count",
    "B15003_007E": "third_grade_count",
    "B15003_008E": "fourth_grade_count",
    "B15003_009E": "fifth_grade_count",
    "B15003_010E": "sixth_grade_count",
    "B15003_011E": "seventh_grade_count",
    "B15003_012E": "eighth_grade_count",
    "B15003_013E": "ninth_grade_count",
    "B15003_014E": "tenth_grade_count",
    "B15003_015E": "eleventh_grade_count",
    "B15003_016E": "twelfth_grade_no_diploma_count",
    "B15003_017E": "hs_diploma_count",
    "B15003_018E": "ged_count",
    "B15003_019E": "some_college_less_year_count",
    "B15003_020E": "some_college_year_plus_count",
    "B15003_021E": "associates_count",
    "B15003_022E": "bachelors_count",
    "B15003_023E": "masters_count",
    "B15003_024E": "professional_degree_count",
    "B15003_025E": "doctorate_count"
})


# Convert data columns to numeric values
# Replace negative Census estimates (indicating missing or unavailable data) with NaN
numeric_cols = df.columns.drop("state")

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")
    df[col] = df[col].apply(lambda x: np.nan if x < 0 else x)


# The dataset currently contains individual educational attainment categories.
# The following code combines them into broader groups for easier analysis.

# Keep population and income variables in the cleaned dataset.
census_clean = df[["state", "total_pop", "adults_25_plus", "median_income"]].copy()


# Calculate the percentage of adults (25+) in each educational attainment group

# Did not complete high school
census_clean["less_than_hs_pct"] = (
    df.loc[:, "no_schooling_count":"twelfth_grade_no_diploma_count"].sum(axis=1)
    / df["adults_25_plus"] * 100
)

# Completed high school, but not a bachelor's degree
census_clean["hs_to_associates_pct"] = (
    df[[
        "hs_diploma_count",
        "ged_count",
        "some_college_less_year_count",
        "some_college_year_plus_count",
        "associates_count"
    ]].sum(axis=1)
    / df["adults_25_plus"] * 100
)

# Bachelor's degree, but nothing higher
census_clean["bachelors_only_pct"] = (
    df["bachelors_count"] / df["adults_25_plus"] * 100
)

# Master's degree, but nothing higher
census_clean["masters_only_pct"] = (
    df["masters_count"] / df["adults_25_plus"] * 100
)

# Professional degree or doctorate
census_clean["professional_or_doctorate_pct"] = (
    df[["professional_degree_count", "doctorate_count"]].sum(axis=1)
    / df["adults_25_plus"] * 100
)


# Export cleaned data to CSV
os.makedirs("data", exist_ok=True)
census_clean.to_csv("data/census_educational_data.csv", index=False)
