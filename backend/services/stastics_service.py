import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis
from scipy.stats import norm
from scipy.stats import ttest_1samp
from scipy.stats import shapiro
from scipy.stats import f_oneway
from scipy.stats import chi2_contingency
from scipy.stats import pearsonr
import os
import json
from datetime import datetime

class StatisticsService:
    """
    Enterprise Statistical Analysis Service.
    """

    @staticmethod
    def health():
        return {
            "module": "Statistical Analysis",
            "status": "Running",
            "version": "1.0.0"
        }

    @staticmethod
    def descriptive_statistics(df):
        """
        Generate descriptive statistics for all numerical columns.
        """

        numerical_df = df.select_dtypes(include=["number"])

        if numerical_df.empty:
            raise ValueError(
                "Dataset contains no numerical columns."
            )

        report = {}

        for column in numerical_df.columns:

            data = numerical_df[column].dropna()

            mean = data.mean()

            std = data.std()

            report[column] = {

                "count": int(data.count()),

                "mean": round(float(mean), 2),

                "median": round(float(data.median()), 2),

                "mode": round(float(data.mode().iloc[0]), 2),

                "minimum": round(float(data.min()), 2),

                "maximum": round(float(data.max()), 2),

                "range": round(
                    float(data.max() - data.min()),
                    2
                ),

                "variance": round(
                    float(data.var()),
                    2
                ),

                "standard_deviation": round(
                    float(std),
                    2
                ),

                "q1": round(
                    float(data.quantile(0.25)),
                    2
                ),

                "q3": round(
                    float(data.quantile(0.75)),
                    2
                ),

                "iqr": round(
                    float(
                        data.quantile(0.75)
                        - data.quantile(0.25)
                    ),
                    2
                ),

                "coefficient_of_variation": round(
                    float((std / mean) * 100),
                    2
                ) if mean != 0 else None

            }

        return report
    
    @staticmethod
    def probability_distribution(df):
        """
        Analyze probability distribution of numerical columns.
        """

        numerical_df = df.select_dtypes(include=["number"])

        if numerical_df.empty:
            raise ValueError(
                "Dataset contains no numerical columns."
            )

        report = {}

        for column in numerical_df.columns:

            data = numerical_df[column].dropna()

            mean = data.mean()

            std = data.std()

            skewness = skew(data)

            kurt = kurtosis(data)

            if abs(skewness) < 0.5:
                distribution = "Approximately Normal"

            elif skewness > 0.5:
                distribution = "Positively Skewed"

            else:
                distribution = "Negatively Skewed"

            report[column] = {

                "mean": round(float(mean), 2),

                "standard_deviation": round(float(std), 2),

                "skewness": round(float(skewness), 4),

                "kurtosis": round(float(kurt), 4),

                "distribution": distribution,

                "68_percent_range": [
                    round(float(mean - std), 2),
                    round(float(mean + std), 2)
                ],

                "95_percent_range": [
                    round(float(mean - 2 * std), 2),
                    round(float(mean + 2 * std), 2)
                ],

                "99_7_percent_range": [
                    round(float(mean - 3 * std), 2),
                    round(float(mean + 3 * std), 2)
                ]

            }

        return report
    
    @staticmethod
    def confidence_intervals(df):
        """
        Calculate 95% confidence intervals for numerical columns.
        """

        numerical_df = df.select_dtypes(include=["number"])

        if numerical_df.empty:
            raise ValueError(
                "Dataset contains no numerical columns."
            )

        report = {}

        confidence_level = 0.95
        z_score = norm.ppf(0.975)

        for column in numerical_df.columns:

            data = numerical_df[column].dropna()

            n = len(data)

            mean = data.mean()

            std = data.std()

            standard_error = std / np.sqrt(n)

            margin_of_error = z_score * standard_error

            lower = mean - margin_of_error

            upper = mean + margin_of_error

            report[column] = {

                "sample_size": int(n),

                "mean": round(float(mean), 2),

                "standard_deviation": round(float(std), 2),

                "standard_error": round(float(standard_error), 4),

                "margin_of_error": round(float(margin_of_error), 4),

                "confidence_level": "95%",

                "lower_confidence_limit": round(float(lower), 2),

                "upper_confidence_limit": round(float(upper), 2)

            }

        return report
    
    @staticmethod
    def hypothesis_test(df, column, hypothesized_mean):
        """
        Perform a one-sample t-test.
        """

        if column not in df.columns:
            raise ValueError(
                f"Column '{column}' not found."
            )

        if not pd.api.types.is_numeric_dtype(df[column]):
            raise ValueError(
                "Selected column must be numerical."
            )

        data = df[column].dropna()

        t_statistic, p_value = ttest_1samp(
            data,
            hypothesized_mean
        )

        alpha = 0.05

        if p_value < alpha:
            decision = "Reject the Null Hypothesis"
            interpretation = (
                f"The mean of '{column}' is significantly different "
                f"from {hypothesized_mean}."
            )
        else:
            decision = "Fail to Reject the Null Hypothesis"
            interpretation = (
                f"There is insufficient evidence to conclude that "
                f"the mean of '{column}' differs from "
                f"{hypothesized_mean}."
            )

        return {

            "column": column,

            "sample_size": int(len(data)),

            "sample_mean": round(float(data.mean()), 2),

            "hypothesized_mean": hypothesized_mean,

            "t_statistic": round(float(t_statistic), 4),

            "p_value": round(float(p_value), 6),

            "alpha": alpha,

            "decision": decision,

            "interpretation": interpretation

        }
    
    @staticmethod
    def normality_test(df, column):
        """
        Perform Shapiro-Wilk Normality Test.
        """

        if column not in df.columns:
            raise ValueError(
                f"Column '{column}' not found."
            )

        if not pd.api.types.is_numeric_dtype(df[column]):
            raise ValueError(
                "Selected column must be numerical."
            )

        data = df[column].dropna()

        statistic, p_value = shapiro(data)

        alpha = 0.05

        if p_value > alpha:

            decision = "Fail to Reject the Null Hypothesis"

            interpretation = (
                f"The '{column}' data appears to follow a normal distribution."
            )

        else:

            decision = "Reject the Null Hypothesis"

            interpretation = (
                f"The '{column}' data does not appear to follow a normal distribution."
            )

        return {

            "column": column,

            "sample_size": int(len(data)),

            "test": "Shapiro-Wilk",

            "test_statistic": round(float(statistic), 6),

            "p_value": round(float(p_value), 6),

            "alpha": alpha,

            "decision": decision,

            "interpretation": interpretation

        }
    
    @staticmethod
    def anova_test(df, numerical_column, group_column):
        """
        Perform One-Way ANOVA.
        """

        if numerical_column not in df.columns:
            raise ValueError(
                f"Column '{numerical_column}' not found."
            )

        if group_column not in df.columns:
            raise ValueError(
                f"Column '{group_column}' not found."
            )

        if not pd.api.types.is_numeric_dtype(df[numerical_column]):
            raise ValueError(
                "Numerical column must contain numeric values."
            )

        grouped_data = []

        group_names = []

        for group_name, group in df.groupby(group_column):

            values = group[numerical_column].dropna()

            if len(values) >= 2:

                grouped_data.append(values)

                group_names.append(str(group_name))

        if len(grouped_data) < 2:

            raise ValueError(
                "At least two groups with sufficient data are required."
            )

        f_statistic, p_value = f_oneway(*grouped_data)

        alpha = 0.05

        if p_value < alpha:

            decision = "Reject the Null Hypothesis"

            interpretation = (
                f"The mean of '{numerical_column}' differs significantly "
                f"between at least one of the '{group_column}' groups."
            )

        else:

            decision = "Fail to Reject the Null Hypothesis"

            interpretation = (
                f"No statistically significant difference was found "
                f"between the group means."
            )

        return {

            "test": "One-Way ANOVA",

            "numerical_column": numerical_column,

            "group_column": group_column,

            "number_of_groups": len(group_names),

            "groups": group_names,

            "f_statistic": round(float(f_statistic), 4),

            "p_value": round(float(p_value), 6),

            "alpha": alpha,

            "decision": decision,

            "interpretation": interpretation

        }
    
    @staticmethod
    def chi_square_test(df, column1, column2):
        """
        Perform Chi-Square Test of Independence.
        """

        if column1 not in df.columns:
            raise ValueError(
                f"Column '{column1}' not found."
            )

        if column2 not in df.columns:
            raise ValueError(
                f"Column '{column2}' not found."
            )

        contingency_table = pd.crosstab(
            df[column1],
            df[column2]
        )

        if contingency_table.empty:
            raise ValueError(
                "Unable to build contingency table."
            )

        chi2, p_value, dof, expected = chi2_contingency(
            contingency_table
        )

        alpha = 0.05

        if p_value < alpha:

            decision = "Reject the Null Hypothesis"

            interpretation = (
                f"There is a statistically significant association "
                f"between '{column1}' and '{column2}'."
            )

        else:

            decision = "Fail to Reject the Null Hypothesis"

            interpretation = (
                f"No statistically significant association was found "
                f"between '{column1}' and '{column2}'."
            )

        return {

            "test": "Chi-Square Test of Independence",

            "column_1": column1,

            "column_2": column2,

            "chi_square_statistic": round(
                float(chi2),
                4
            ),

            "degrees_of_freedom": int(dof),

            "p_value": round(
                float(p_value),
                6
            ),

            "alpha": alpha,

            "decision": decision,

            "interpretation": interpretation,

            "contingency_table": contingency_table.to_dict()

        }
    
    @staticmethod
    def correlation_significance(df, column1, column2):
        """
        Perform Pearson Correlation Significance Test.
        """

        if column1 not in df.columns:
            raise ValueError(
                f"Column '{column1}' not found."
            )

        if column2 not in df.columns:
            raise ValueError(
                f"Column '{column2}' not found."
            )

        if not pd.api.types.is_numeric_dtype(df[column1]):
            raise ValueError(
                f"'{column1}' must be numerical."
            )

        if not pd.api.types.is_numeric_dtype(df[column2]):
            raise ValueError(
                f"'{column2}' must be numerical."
            )

        data = df[[column1, column2]].dropna()

        if len(data) < 3:
            raise ValueError(
                "At least 3 observations are required."
            )

        correlation, p_value = pearsonr(
            data[column1],
            data[column2]
        )

        alpha = 0.05

        abs_corr = abs(correlation)

        if abs_corr >= 0.90:
            strength = "Very Strong"

        elif abs_corr >= 0.70:
            strength = "Strong"

        elif abs_corr >= 0.50:
            strength = "Moderate"

        elif abs_corr >= 0.30:
            strength = "Weak"

        else:
            strength = "Very Weak"

        if p_value < alpha:

            decision = "Statistically Significant"

            interpretation = (
                f"There is a statistically significant correlation "
                f"between '{column1}' and '{column2}'."
            )

        else:

            decision = "Not Statistically Significant"

            interpretation = (
                f"No statistically significant correlation "
                f"was found between '{column1}' and '{column2}'."
            )

        return {

            "test": "Pearson Correlation",

            "column_1": column1,

            "column_2": column2,

            "correlation": round(
                float(correlation),
                4
            ),

            "strength": strength,

            "p_value": round(
                float(p_value),
                6
            ),

            "alpha": alpha,

            "decision": decision,

            "interpretation": interpretation

        }
    
    @staticmethod
    def statistical_insights(df):
        """
        Generate automated statistical insights.
        """

        numerical_df = df.select_dtypes(include=["number"])

        if numerical_df.empty:
            raise ValueError(
                "Dataset contains no numerical columns."
            )

        report = {}

        for column in numerical_df.columns:

            data = numerical_df[column].dropna()

            mean = data.mean()
            std = data.std()

            cv = (
                (std / mean) * 100
                if mean != 0
                else None
            )

            skewness = skew(data)

            if abs(skewness) < 0.5:
                distribution = "Approximately Normal"

            elif skewness > 0.5:
                distribution = "Positively Skewed"

            else:
                distribution = "Negatively Skewed"

            # ------------------------
            # Business Insight
            # ------------------------

            insights = []

            if cv is not None:

                if cv < 20:
                    insights.append(
                        "Low variability observed."
                    )

                elif cv < 50:
                    insights.append(
                        "Moderate variability observed."
                    )

                else:
                    insights.append(
                        "High variability observed."
                    )

            if distribution == "Approximately Normal":

                insights.append(
                    "Data is approximately normally distributed."
                )

            elif distribution == "Positively Skewed":

                insights.append(
                    "Data contains relatively higher extreme values."
                )

            else:

                insights.append(
                    "Data contains relatively lower extreme values."
                )

            recommendation = (
                "Suitable for standard statistical analysis."
                if distribution == "Approximately Normal"
                else
                "Consider transformation or robust statistical methods."
            )

            report[column] = {

                "mean": round(float(mean), 2),

                "standard_deviation": round(float(std), 2),

                "coefficient_of_variation": (
                    round(float(cv), 2)
                    if cv is not None
                    else None
                ),

                "skewness": round(
                    float(skewness),
                    4
                ),

                "distribution": distribution,

                "business_insight": insights,

                "recommendation": recommendation

            }

        return report
    
    @staticmethod
    def export_statistics_report(df):
        """
        Export complete statistical report.
        """

        report = {
            "generated_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "statistical_insights":
                StatisticsService.statistical_insights(df)
        }

        export_folder = "exports"

        os.makedirs(
            export_folder,
            exist_ok=True
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        output_file = os.path.join(
            export_folder,
            f"statistics_report_{timestamp}.json"
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                report,
                file,
                indent=4
            )

        return {

            "status": "Success",

            "message": "Statistics report exported successfully.",

            "file": output_file

        }