# Business Understanding

## Project Context

Election participation is often summarized with a single statewide turnout rate. That measure is useful, but it can conceal meaningful geographic variation. Raw cards-cast totals create a different problem: large counties naturally produce more votes, even when a smaller share of eligible voters participates.

This project treats the election data as a resource-allocation and performance-monitoring problem. The goal is to combine rates and counts so stakeholders can identify where participation differs, estimate the scale of the opportunity, and decide where deeper analysis should begin.

## Main Decision Question

> Which Maryland counties participated above or below the statewide turnout benchmark, and where do turnout rates and eligible-voter counts suggest the greatest need for further review or outreach?

## Supporting Questions

1. What were statewide eligible-voter, cards-cast, turnout, and non-voter totals?
2. Which counties had the highest and lowest turnout rates?
3. How far did each county's turnout differ from the 16.68% statewide rate?
4. Which below-average counties contain the largest eligible-voter populations?
5. What relationship is visible between county population size and turnout rate?

## Stakeholders

| Stakeholder | Information needed | Decision supported |
| --- | --- | --- |
| State election administrators | Statewide benchmark, county outliers, count and rate comparisons | Where to request additional local review |
| Local election boards | County position relative to the state and peer counties | Whether participation patterns warrant operational investigation |
| Civic organizations | Low-turnout areas and size of the eligible-voter population | Where outreach may reach the most potential voters |
| Campaign and public-affairs teams | Geographic participation and population scale | Where field or communication analysis should begin |
| Journalists and researchers | Transparent rankings, measures, and caveats | Which patterns merit reporting or follow-up research |

## Success Measures

The dashboard should allow a user to:

- Reconcile statewide eligible voters, cards cast, and calculated non-voters
- Compare every jurisdiction using the same turnout definition
- Identify counties above and below the weighted statewide turnout rate
- Evaluate turnout rate alongside eligible-voter population rather than relying on one metric
- Move from a statewide summary to a specific county pattern without overstating causality

## Decision Logic

A low turnout rate does not automatically make a county the highest priority. Stakeholders should consider two dimensions together:

- **Performance gap:** How far the county falls below the statewide turnout rate
- **Opportunity scale:** How many eligible voters or non-voters are represented

This creates a practical screening framework. A large county slightly below the benchmark may represent more potential engagement than a small county with the lowest rate.

## Claim Boundaries

This analysis can identify:

- Geographic differences in turnout
- Counties above or below the statewide benchmark
- Concentrations of eligible voters and non-voters
- A county-level association between eligible-voter population and turnout rate

This analysis cannot establish:

- Why a county's turnout was high or low
- Whether election administration, campaign activity, demographics, or access caused a result
- How turnout varied within a county
- Which outreach intervention would increase participation
- Individual voter behavior

## Recommended Use

Use the dashboard to prioritize questions, not to diagnose causes. Any intervention should follow additional analysis using precinct-level results, voting method, historical turnout, demographic context, election access, and local operational information.
