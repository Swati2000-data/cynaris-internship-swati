# Business Hypothesis Testing and Statistical Validation

## Project Overview
This project applies statistical hypothesis testing to the Sample Superstore dataset to validate business assumptions and support data-driven decision-making.

## Objectives
- Formulate null and alternative hypotheses for business scenarios.
- Perform one-sample and independent two-sample t-tests.
- Calculate p-values and 95% confidence intervals.
- Interpret statistical significance.
- Understand Type I and Type II errors and their business consequences.

## Business Scenarios

### 1. Average Sales Benchmark
- H0: Average order sales = $200.
- H1: Average order sales ≠ $200.
- Test: One-sample t-test.
- Sample mean: $458.61.
- P-value: Approximately 0.
- Decision: Reject H0.

**Conclusion:** Average order sales are significantly different from and higher than the $200 benchmark.

### 2. Consumer vs Corporate Sales
- H0: Consumer and Corporate average sales are equal.
- H1: Consumer and Corporate average sales are different.
- Test: Independent Welch's two-sample t-test.
- Consumer mean: $449.11.
- Corporate mean: $466.41.
- P-value: 0.555584.
- Decision: Fail to reject H0.

**Conclusion:** There is insufficient statistical evidence to establish a significant difference in average sales between the two customer segments.

### 3. Average Order Profitability
- H0: Average order profit = $0.
- H1: Average order profit ≠ $0.
- Test: One-sample t-test.
- Average profit: $57.18.
- P-value: Approximately 0.
- Decision: Reject H0.

**Conclusion:** Average order-level profit is significantly positive.

## Type I and Type II Errors

**Type I Error:** Rejecting a true null hypothesis.  
Business impact: Making an unnecessary business investment based on a false positive finding.

**Type II Error:** Failing to reject a false null hypothesis.  
Business impact: Missing a genuine business opportunity due to insufficient statistical evidence.

## Technologies Used
- Python
- Pandas
- NumPy
- SciPy
- VS Code
- Git and GitHub

## Key Learnings
- Formulating business hypotheses.
- Applying statistical tests using SciPy.
- Interpreting p-values and confidence intervals.
- Evaluating statistical significance.
- Translating statistical findings into business insights.

## Repository Deliverables
- `hypothesis_testing.py` – Python implementation of hypothesis tests.
- `README.md` – Project documentation.
- `Sample - Superstore.csv` – Dataset used for analysis.
