# Data Understanding

## Data Source

The Tableau workbook identifies the Maryland State Board of Elections as its source. The official state site publishes the certified 2026 gubernatorial primary results and related election data files.

- [Official primary results](https://elections.maryland.gov/elections/2026/primary_results/index.html)
- [2026 election data files](https://elections.maryland.gov/elections/2026/election_data/index.html)

## Dataset Grain

One row represents one Maryland county or county-equivalent in the statewide turnout summary.

- **Rows:** 24
- **Geography:** 23 counties plus Baltimore City
- **Election:** 2026 Maryland gubernatorial primary
- **Level of detail:** County-level aggregate

County is the natural key in this analytical dataset. No duplicate county rows are present in the exported workbook data.

## Source Fields

| Field | Type | Role | Interpretation |
| --- | --- | --- | --- |
| `County` | Text | Dimension/key | County or Baltimore City |
| `Cards Cast` | Integer | Measure | Ballots recorded in the turnout summary |
| `Eligible Voters` | Integer | Measure | Eligible-voter denominator reported by the source |
| `Percentage` | Text in the workbook source | Reference field | Source-provided percentage; Tableau calculations use counts directly |

## Calculated Measures

| Measure | Definition | Business use |
| --- | --- | --- |
| County turnout rate | `Cards Cast / Eligible Voters` | Compares participation across differently sized counties |
| Votes not cast | `Eligible Voters - Cards Cast` | Estimates the scale of non-participation in the source population |
| Non-voter rate | `Votes Not Cast / Eligible Voters` | Complements the turnout rate |
| Statewide turnout rate | `SUM(Cards Cast) / SUM(Eligible Voters)` | Provides a weighted statewide benchmark |
| Turnout difference | `County Turnout Rate - 16.68%` | Shows performance above or below the statewide result |
| County turnout rank | Descending rank of county turnout rate | Identifies the highest and lowest participation rates |

The statewide rate must be calculated from statewide totals. Averaging the 24 county percentages would give each county equal weight and would not represent statewide voter turnout.

## Validation Results

- All 24 Maryland jurisdictions are represented.
- County names are unique.
- Eligible-voter and cards-cast values are positive for every row.
- Cards cast do not exceed eligible voters in any county.
- County turnout values derived from the two count fields range from 12.43% to 24.11%.
- The county totals reconcile to 3,686,495 eligible voters and 614,845 cards cast.
- The weighted statewide turnout calculation reconciles to 16.68%.
- Calculated non-voters reconcile to 3,071,650, or 83.32% of the eligible-voter total.

## Data-to-Decision Connections

| Business question | Fields or calculations used | Interpretation |
| --- | --- | --- |
| Which counties participated most or least? | County turnout rate and rank | Rate-based comparison controls for county size |
| Where is the largest outreach opportunity? | Eligible voters, votes not cast, turnout difference | Combines scale with relative performance |
| Which counties differ from the state? | Turnout difference | Flags counties above or below the weighted benchmark |
| Is county size related to turnout? | Eligible voters and county turnout rate | Provides a descriptive association for follow-up analysis |

## Analytical Findings Supported by the Data

- Dorchester recorded the highest turnout rate at 24.11%.
- Cecil recorded the lowest turnout rate at 12.43%.
- Montgomery had the largest eligible-voter population at 701,022 and a turnout rate of 15.59%.
- The Pearson correlation between eligible-voter population and turnout rate is approximately -0.51 across the 24 jurisdictions.

The correlation is calculated from aggregate county observations. It should not be interpreted as an individual-level relationship or a causal effect.

## Data Limitations

- County aggregates hide precinct and neighborhood variation.
- The dataset has no historical comparison period.
- It does not separate early, election-day, mail-in, or provisional voting.
- It does not include party affiliation, demographics, ballot competitiveness, outreach, polling-place access, or other explanatory variables.
- “Eligible voters” is retained as the source label and is not independently reconstructed in this project.
- The dashboard's 16.68% turnout-difference benchmark is stored as a constant. It is valid for this fixed dataset but should be converted to a dynamic calculation if the workbook is refreshed, expanded, or filtered.

## Analytical Readiness

The dataset is suitable for descriptive county comparison, mapping, ranking, and resource-prioritization screening. It is not sufficient for causal analysis, program evaluation, or individual-level inference.
