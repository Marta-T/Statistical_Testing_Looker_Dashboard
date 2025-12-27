import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest


def histogram(
    df,
    col,
    group_col,
    group_1,
    group_2,
    bins=50,
    figsize=(12, 6),
    text_group1=None,
    text_group2=None,
):
    """
    Function that creates a histogram comparing two groups side by side.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe containing the data to plot
    col : str
        Name of the column to plot (e.g., 'sum_gamerounds')
    group_col : str
        Name of the column containing group labels (e.g., 'version')
    group_1 : str
        Name of the first group to plot (e.g., 'gate_30')
    group_2 : str
        Name of the second group to plot (e.g., 'gate_40')
    bins : int, optional
        Number of bins for the histogram. Default is 50.
    figsize : tuple of floats, optional
        Figure size (width, height) in inches. Default is (12, 6).
    text_group1 : str, optional
        Statistics text to display on the first histogram. Default is None.
    text_group2 : str, optional
        Statistics text to display on the second histogram. Default is None.

    Returns
    -------
    None
        Displays the histogram plot
    """
    plt.figure(figsize=figsize)

    plt.subplot(1, 2, 1)
    df[df[group_col] == group_1][col].hist(bins=bins, edgecolor="black")
    plt.title(f"Distribution of {group_1} game rounds")
    plt.xlabel(col)
    plt.ylabel("Frequency")
    plt.grid(False)
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)

    if text_group1:
        plt.text(
            0.95,
            0.95,
            text_group1,
            transform=plt.gca().transAxes,
            fontsize=9,
            verticalalignment="top",
            horizontalalignment="left",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
        )

    plt.subplot(1, 2, 2)
    df[df[group_col] == group_2][col].hist(bins=bins, edgecolor="black")
    plt.title(f"Distribution of {group_2} game rounds")
    plt.xlabel(col)
    plt.ylabel("Frequency")
    plt.grid(False)
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)

    if text_group2:
        plt.text(
            0.95,
            0.95,
            text_group2,
            transform=plt.gca().transAxes,
            fontsize=9,
            verticalalignment="top",
            horizontalalignment="left",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
        )

    plt.tight_layout()
    plt.show()


def remove_outliers(df, col):
    """
    Remove outliers from a dataframe using the IQR (Interquartile Range) method.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe containing the data
    col : str
        Name of the column to remove outliers from

    Returns
    -------
    pandas.DataFrame
        Dataframe with outliers removed based on IQR method (values outside Q1 - 1.5*IQR and Q3 + 1.5*IQR)
    """
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    df_cleaned = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]

    return df_cleaned


def histogram_retention_rates(
    categories,
    gate_30_values,
    gate_40_values,
    ci_30,
    ci_40,
    figsize=(7, 4),
    z_test_text=None,
    stats_text_30=None,
    stats_text_40=None,
):
    """
    Create a grouped bar chart comparing retention rates between two versions with confidence intervals.

    Parameters
    ----------
    categories : list of str
        List of category names for x-axis labels (e.g., ['1-day retention', '7-day retention'])
    gate_30_values : list of float
        Percentage values for gate_30 group corresponding to each category
    gate_40_values : list of float
        Percentage values for gate_40 group corresponding to each category
    ci_30 : list of float
        95% confidence interval margins for gate_30 values
    ci_40 : list of float
        95% confidence interval margins for gate_40 values
    figsize : tuple of floats, optional
        Figure size (width, height) in inches. Default is (7,4).
    z_test_text : str
        Formatted text containing z-test results to display on the plot
    stats_text_30 : str
        Formatted text containing descriptive statistics for gate_30 to display on the plot
    stats_text_40 : str
        Formatted text containing descriptive statistics for gate_40 to display on the plot

    Returns
    -------
    None
        Displays the grouped bar chart with error bars and confidence interval labels
    """
    x = np.arange(len(categories))
    width = 0.35
    fig, ax = plt.subplots(figsize=figsize)

    if z_test_text or stats_text_30 or stats_text_40:
        plt.subplots_adjust(left=0.1, right=0.65, top=0.95, bottom=0.1)

    bars1 = ax.bar(
        x - width / 2, gate_30_values, width, label="gate_30", yerr=ci_30, capsize=3
    )
    bars2 = ax.bar(
        x + width / 2, gate_40_values, width, label="gate_40", yerr=ci_40, capsize=3
    )

    ax.set_ylabel("Percentage (%)")
    ax.set_title("Retention rates by version (with 95% CI)")
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()

    for i, (val, ci) in enumerate(zip(gate_30_values, ci_30)):
        ax.text(
            i - width / 2,
            val + ci + 0.5,
            f"{val-ci:.1f}%-{val+ci:.1f}%",
            ha="center",
            va="bottom",
            fontsize=7,
        )
    for i, (val, ci) in enumerate(zip(gate_40_values, ci_40)):
        ax.text(
            i + width / 2,
            val + ci + 0.5,
            f"{val-ci:.1f}%-{val+ci:.1f}%",
            ha="center",
            va="bottom",
            fontsize=7,
        )

    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)

    if z_test_text:
        fig.text(
            0.70,
            0.95,
            z_test_text,
            fontsize=9,
            verticalalignment="top",
            bbox=dict(boxstyle="round", facecolor="lightblue", alpha=0.5),
        )
    if stats_text_30:
        fig.text(
            0.70,
            0.55,
            stats_text_30,
            fontsize=9,
            verticalalignment="top",
            bbox=dict(boxstyle="round", facecolor="lightblue", alpha=0.5),
        )
    if stats_text_40:
        fig.text(
            0.70,
            0.35,
            stats_text_40,
            fontsize=9,
            verticalalignment="top",
            bbox=dict(boxstyle="round", facecolor="lightblue", alpha=0.5),
        )
    plt.show()


def proportion_ci(count, total, confidence=0.95):
    """
    Calculate the margin of error for a proportion using the Wald method.
    It which works well for large samples (n > 30) and proportions not too close to 0 or 1.

    Parameters
    ----------
    count : int
        Number of successes (e.g., number of users retained)
    total : int
        Total number of observations (e.g., total number of users)
    confidence : float, optional
        Confidence level for the interval. Default is 0.95 (95% confidence interval).

    Returns
    -------
    float
        Margin of error for the proportion (half-width of the confidence interval)
    """
    prop = count / total
    se = np.sqrt(prop * (1 - prop) / total)
    margin = stats.norm.ppf((1 + confidence) / 2) * se
    return margin


def z_test(
    dataframe, group_col, group1_name, group2_name, target_col, alpha=0.05, print=False
):
    """
    Perform two-sample z-test for proportions with effect size.

    Parameters:
    -----------
    dataframe : pd.DataFrame
        The dataset
    group_col : str
        Column name containing group labels
    group1_name : str
        Name of first group (e.g., 'gate_30')
    group2_name : str
        Name of second group (e.g., 'gate_40')
    target_col : str
        Column name with binary outcome (True/False)
    alpha : float
        Significance level (default 0.05)
    print : bool
        If True, prints out the statistics of the columns (default is False)

    Returns:
    --------
    dict : Results including p-value, effect size, and proportions
    """
    counts = [
        dataframe[dataframe[group_col] == group1_name][target_col].sum(),
        dataframe[dataframe[group_col] == group2_name][target_col].sum(),
    ]
    nobs = [
        len(dataframe[dataframe[group_col] == group1_name]),
        len(dataframe[dataframe[group_col] == group2_name]),
    ]

    z_stat, p_value = proportions_ztest(counts, nobs)

    p1 = counts[0] / nobs[0]
    p2 = counts[1] / nobs[1]

    cohens_h = 2 * (np.arcsin(np.sqrt(p2)) - np.arcsin(np.sqrt(p1)))

    if print:
        print(f"{target_col.upper()}\n")
        print(f"{group1_name}: {p1:.2%}")
        print(f"{group2_name}: {p2:.2%}")
        print(f"Difference: {abs(p2-p1):.2%}")
        print(f"Cohen's h: {cohens_h:.3f}")
        print(f"Z-statistic: {z_stat:.4f}")
        print(f"p-value: {p_value:.4f}")
        print(f"Result: {'Significant' if p_value < alpha else 'Not significant'}")

    return {
        "p_value": p_value,
        "z_statistic": z_stat,
        "cohens_h": cohens_h,
        "proportion_group1": p1,
        "proportion_group2": p2,
        "significant": p_value < alpha,
    }


def welch_t_test(group1, group2, alpha=0.05, print=False):
    """
    Perform Welch's t-test to compare means of two independent groups with unequal variances.

    Parameters
    ----------
    group1 : pandas.Series or array-like
        First group of numerical data
    group2 : pandas.Series or array-like
        Second group of numerical data
    alpha : float, optional
        Significance level for hypothesis testing. Default is 0.05.
    verbose : bool, optional
        If True, prints test results to console. Default is False.

    Returns
    -------
    dict
        Dictionary containing:
        - 'p_value': p-value from the t-test
        - 't_statistic': t-statistic value
        - 'cohens_d': Cohen's d effect size
        - 'mean_difference': difference between group means
        - 'ci_95': 95% confidence interval for the mean difference
        - 'significant': boolean indicating if result is significant at alpha level
    """
    statistic, p_value = stats.ttest_ind(group1, group2, equal_var=False)

    mean_diff = group1.mean() - group2.mean()
    pooled_std = np.sqrt((group1.var() + group2.var()) / 2)
    cohens_d = mean_diff / pooled_std

    se = np.sqrt(group1.var() / len(group1) + group2.var() / len(group2))
    ci_95 = stats.t.interval(
        0.95, df=len(group1) + len(group2) - 2, loc=mean_diff, scale=se
    )

    if print:
        print(f"t-statistic: {statistic:.2f}")
        print(f"p-value: {p_value:.4f}")
        print(f"Mean difference: {mean_diff:.2f}")
        print(f"Cohen's d: {cohens_d:.3f}")
        print(f"95% CI: {ci_95}")

    return {
        "p_value": p_value,
        "t_statistic": statistic,
        "cohens_d": cohens_d,
        "mean_difference": mean_diff,
        "ci_95": ci_95,
        "significant": p_value < alpha,
    }


def boxplot_gamerounds(
    data, labels, welch_t_test_text, statistics_gate_30, statistics_gate_40
):
    fig, ax = plt.subplots(figsize=(6, 5))
    plt.subplots_adjust(left=0.1, right=0.65, top=0.95, bottom=0.1)

    bp = ax.boxplot(
        data,
        labels=labels,
        patch_artist=True,
        flierprops=dict(marker="o", markerfacecolor="white", markersize=3),
        medianprops=dict(color="black", linewidth=1),
        boxprops=dict(facecolor="lightblue", edgecolor="black", linewidth=1),
        whiskerprops=dict(color="black", linewidth=1),
        capprops=dict(color="black", linewidth=1),
    )

    colors = ["lightblue", "lightcoral"]
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)

    ax.set_ylabel("Sum of gamerounds")
    ax.set_xlabel("Version")
    ax.set_title("Distribution of gamerounds by version")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.text(
        0.70,
        0.95,
        welch_t_test_text,
        fontsize=9,
        verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor="lightblue", alpha=0.5),
    )
    fig.text(
        0.70,
        0.7,
        statistics_gate_30,
        fontsize=9,
        verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor="lightblue", alpha=0.5),
    )
    fig.text(
        0.70,
        0.4,
        statistics_gate_40,
        fontsize=9,
        verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor="lightblue", alpha=0.5),
    )

    plt.show()
