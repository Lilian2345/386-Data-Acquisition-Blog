# Education and Household Income Across the United States

## Introduction

Education is often viewed as an important factor in economic opportunity. People with higher levels of education tend to have access to different career opportunities, but the relationship between education and income can vary across geographic areas. Differences in industries, cost of living, and local economies may also influence household income.

I wanted to explore whether states with higher levels of educational attainment also tend to have higher median household incomes. Rather than looking at individual education and income records, I used publicly available Census data to compare educational attainment and income across U.S. states.

My goal was to create a dataset that could help identify broad patterns between education and economic outcomes and provide a starting point for further analysis.

## Research Question

**How does median household income vary across education levels among U.S. states?**

More specifically, I wanted to investigate which educational attainment categories have the strongest relationships with median household income. I grouped educational attainment into five categories:

- Less than a high school education
- High school diploma through associate's degree
- Bachelor's degree only
- Master's degree only
- Professional degree or doctorate

## Data Source and Ethics

I collected my data from the [U.S. Census Bureau's American Community Survey (ACS)](https://www.census.gov/programs-surveys/acs). The ACS provides demographic and economic estimates for communities throughout the United States.

I used the Census API to retrieve ACS five-year estimates. The main Census tables used were:

- **B01003:** Total population
- **B15003:** Educational attainment for the population age 25 and older
- **B19013:** Median household income

The data comes from publicly available, aggregated Census estimates rather than private individual records. Because I used an official government API instead of scraping individual websites, there were no concerns about accessing private information or collecting data without permission. I also avoided collecting personally identifiable information.

For anyone interested in a similar project, the [Census API documentation](https://www.census.gov/data/developers/data-sets.html) explains how to access available datasets and variables.

## Data Collection and Cleaning

I used Python to retrieve and organize the data. The main packages were `census` and `pandas`. The Census Python package makes it possible to request specific variables from the API without manually constructing each request.

The general process was:

1. Obtain a free API key from the [Census Bureau](https://api.census.gov/data/key_signup.html).
2. Use the `Census` package to request population, income, and educational attainment variables.
3. Convert the API response into a pandas DataFrame.
4. Rename the Census variable codes to more readable column names.
5. Convert numeric variables to numeric data types and treat negative Census estimates as missing values.
6. Combine the individual educational attainment counts into five broader categories.
7. Calculate the percentage of adults age 25 and older in each education category.
8. Export the cleaned dataset as a CSV file.

For example, the percentage of adults with only a bachelor's degree was calculated by dividing the number of adults whose highest reported educational attainment was a bachelor's degree by the total population age 25 and older, then multiplying by 100.

The final dataset contains population, median household income, and five educational attainment percentages for each geographic area.

The full collection and cleaning process is available in my [GitHub code repository](https://github.com/Lilian2345/386-Data-Acquisition-Blog/).

## Exploratory Data Analysis

I used `pandas`, `matplotlib`, and `seaborn` to explore the dataset. My analysis focused on comparing population and income across states and examining the relationships between educational attainment and median household income.

### Population and Income Across States

First, I compared population and median household income across the geographic areas in the dataset. I converted population into millions and income into thousands of dollars to make the charts easier to read.

```{python}
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("data/census_educational_data.csv")

df["population_millions"] = df["total_pop"] / 1000000
df["income_thousands"] = df["median_income"] / 1000

largest_pop = df.sort_values("population_millions", ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(10, 8))

sns.barplot(
    data=largest_pop,
    x="population_millions",
    y="state",
    hue="population_millions",
    palette="Blues_r",
    legend=False,
    ax=axes[0]
)

axes[0].set_title("Population by State")
axes[0].set_xlabel("Population (Millions)")
axes[0].set_ylabel("")

sns.barplot(
    data=largest_pop.sort_values("income_thousands", ascending=False),
    x="income_thousands",
    y="state",
    hue="income_thousands",
    palette="Greens_r",
    legend=False,
    ax=axes[1]
)

axes[1].set_title("Median Household Income by State")
axes[1].set_xlabel("Median Income (Thousands of Dollars)")
axes[1].set_ylabel("")

plt.tight_layout()
plt.show()
```

The dataset contains 52 geographic observations: the 50 states, Washington, D.C., and Puerto Rico. The average median household income across these areas was approximately **$79,371**, with a median of approximately $77,419. Washington, D.C. had the highest median household income at $109,870, while Puerto Rico had the lowest at $26,297. Among the 50 states, Massachusetts had the highest median household income at $103,960, and Mississippi had the lowest at $56,447.

### Educational Attainment and Income

Next, I examined how each educational attainment category was associated with median household income. I created scatterplots with linear regression lines to visualize the relationships. I also calculated correlation coefficients to measure the strength and direction of each linear association.

```{python}
education_vars = {
    "less_than_hs_pct": "Less Than High School",
    "hs_to_associates_pct": "High School Through Associate's",
    "bachelors_only_pct": "Bachelor's Degree Only",
    "masters_only_pct": "Master's Degree Only",
    "professional_or_doctorate_pct": "Professional Degree or Doctorate"
}

fig, axes = plt.subplots(3, 2, figsize=(8, 10))
axes = axes.flatten()

for i, (variable, label) in enumerate(education_vars.items()):
    correlation = df[variable].corr(df["income_thousands"])

    sns.regplot(
        data=df,
        x=variable,
        y="income_thousands",
        ax=axes[i],
        color="purple",
        scatter_kws={"alpha": 0.7}
    )

    axes[i].set_title(
        f"{label} vs. Income\nCorrelation: {correlation:.3f}"
    )
    axes[i].set_xlabel("Percentage of Adults Age 25+")
    axes[i].set_ylabel("Median Household Income (Thousands)")

    axes[i].xaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: f"{x:.0f}%")
    )

fig.delaxes(axes[5])
plt.tight_layout()
plt.show()
```

The strongest positive correlation was between the percentage of adults with a master's degree only and median household income (**0.721**). The percentage with a bachelor's degree only also had a strong positive correlation (**0.712**). The professional degree or doctorate category had a positive correlation of **0.580**.

On the other hand, the percentage of adults with less than a high school education had a negative correlation of **-0.479**. The high school through associate's degree category also had a negative correlation of **-0.616**.

Overall, the results suggest that states with higher percentages of adults with bachelor's and master's degrees also tend to have higher median household incomes. However, these relationships are based on comparisons between states, not individual people. Also, since the education categories add up to the entire adult population, a higher percentage in one category means a lower combined percentage in the others. Therefore, these relationships should simply be interpreted as comparisons rather than evidence of a causal relationship.

## Limitations and Further Questions

This analysis has some limitations. Since it compares data across geographic areas rather than individuals, it cannot tell us whether people with more education necessarily earn more. Household income is also influenced by factors such as household size, local industries, and cost of living, which are not included in this dataset. Additionally, correlation does not necessarily mean causation.

A good next step would be to expand the dataset to smaller geographic areas, such as counties, and include additional variables like unemployment, poverty, and cost of living (such as the CPI). This would provide more observations and help explain why income and educational attainment vary across different areas.

## Resources

- [U.S. Census Bureau](https://www.census.gov/)
- [American Community Survey](https://www.census.gov/programs-surveys/acs)
- [Census API Documentation](https://www.census.gov/data/developers/data-sets.html)
- [Census API Key Signup](https://api.census.gov/data/key_signup.html)
- [Census Python Package](https://github.com/datamade/census)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Seaborn Documentation](https://seaborn.pydata.org/)

**Code Repository:** [View my project on GitHub](https://github.com/Lilian2345/386-Data-Acquisition-Blog/tree/main)
