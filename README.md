# Educational Attainment and Household Income Across U.S. States

## Project Overview

This project uses data from the U.S. Census Bureau to explore the relationship between educational attainment and median household income across U.S. states.

Education is often associated with economic outcomes, but I wanted to explore how these patterns differ across states. Specifically, this project examines whether states with higher levels of educational attainment also tend to have higher median household incomes.

**Research Question:** Do states with higher levels of educational attainment tend to have higher median household incomes?

## Data Source

The data comes from the [U.S. Census Bureau's American Community Survey (ACS)](https://www.census.gov/programs-surveys/acs), using the ACS 5-year estimates.

I accessed the data through the Census API using Python's `census` package. The dataset includes estimates for all 50 U.S. states and the District of Columbia.

The API provides information on population, household income, and educational attainment. I combined these variables into one dataset and grouped the educational attainment categories into broader groups to make comparisons easier.

## Repository Contents

```text
├── data/
│   └── census_educational_data.csv
├── census_data.py
└── README.md
```

- **data/**: Contains the final cleaned dataset.
- **census_data.py**: Python script used to retrieve, clean, and transform the Census data.
- **README.md**: Project description and instructions.

## Variables

The final dataset contains the following variables:

| Variable | Description |
|---|---|
| `state` | State name |
| `total_pop` | Total state population |
| `adults_25_plus` | Population age 25 and older |
| `median_income` | Median household income |
| `less_than_hs_pct` | Percentage of adults who did not complete high school |
| `hs_to_associates_pct` | Percentage who completed high school through an associate's degree, but not a bachelor's degree |
| `bachelors_only_pct` | Percentage whose highest degree is a bachelor's degree |
| `masters_only_pct` | Percentage whose highest degree is a master's degree |
| `professional_or_doctorate_pct` | Percentage whose highest degree is a professional or doctorate degree |

All educational attainment percentages use the population age 25 and older as the denominator.

## Data Collection and Cleaning

The dataset was collected using the Census API and the ACS 5-year estimates. The Python script follows these steps:

1. **Retrieve data:** Request population, median household income, and all 24 educational attainment categories (for adults age 25+) for every state.
2. **Organize data:** Convert the API results into a Pandas DataFrame and rename the columns for readability.
3. **Clean data:** Convert numeric variables to numeric types and replace negative Census estimates, which indicate unavailable or missing data, with missing values.
4. **Group educational attainment:** Combine the original 24 education categories into five broader groups based on the highest level of education completed.
5. **Calculate percentages:** Divide each group's population count by the total population age 25+ and multiply by 100.
6. **Export data:** Save the cleaned dataset as a CSV file.

## How to Reproduce the Dataset

Install the necessary Python packages:

```bash
pip install census pandas
```

You will also need a free [Census API key](https://api.census.gov/data/key_signup.html).

Open census_data.py and replace "YOUR_API_KEY" with your Census API key.

Then run the Python script:

```bash
python census_data.py
```

The script will retrieve the Census data, clean and group the variables, and export the final dataset to `data/census_educational_data.csv`.

## Further Information

- [U.S. Census Bureau](https://www.census.gov/)
- [American Community Survey](https://www.census.gov/programs-surveys/acs)
- [Census API Documentation](https://www.census.gov/data/developers/data-sets/acs-5year.html)
- [Census Python Package Documentation](https://github.com/datamade/census)

## Future Analysis

The final dataset can be used to explore differences in educational attainment and household income across states. Potential analyses include:

- Comparing median household income across states with different educational attainment levels.
- Examining the relationship between bachelor's degree attainment and median household income.
- Identifying states with unusually high or low income relative to their educational attainment.
- Creating visualizations to explore geographic and regional patterns.

This dataset provides a starting point for exploring how educational attainment and economic outcomes vary across the United States.


Note: This data originates from the US Census Bureau and is free to use.