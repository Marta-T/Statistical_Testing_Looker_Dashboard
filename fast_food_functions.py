import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


def histogram(df, col, bins=20, figsize=(6, 4), stats_text=None):
    """
    Function that creates a histogram with descriptive statistics.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe containing the data to plot
    col : str
        Name of the column to plot
    bins : int, optional
        Number of bins for the histogram. Default is 20.
    figsize : tuple of floats, optional
        Figure size (width, height) in inches. Default is (6,4).
    stats_text : str, optional
        Statistics text to display. Default is None.

    Returns
    -------
    None
        Displays the histogram plot
    """
    plt.figure(figsize=figsize)

    df[col].hist(bins=bins, edgecolor="black")
    plt.title(f"Distribution of {col}")
    plt.xlabel(col)
    plt.ylabel("Frequency")
    plt.grid(False)
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)

    if stats_text:
        plt.text(
            0.95,
            0.95,
            stats_text,
            transform=plt.gca().transAxes,
            fontsize=9,
            verticalalignment="top",
            horizontalalignment="left",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
        )

    plt.tight_layout()
    plt.show()


def histogram_compare_groups(
    df, group, metric, bins=50, figsize=(12, 6), stats_text=None
):
    """
    Function that creates a histogram comparing two groups side by side.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe containing the data to plot
    bins : int, optional
        Number of bins for the histogram. Default is 50.
    figsize : tuple of floats, optional
        Figure size (width, height) in inches. Default is (12, 6).
    stats_text : dict, optional
        Dictionary with each group statistics. The keys have to be numbered.

    Returns
    -------
    None
        Displays the histogram plot
    """
    plt.figure(figsize=figsize)

    for i in range(1, 4):
        plt.subplot(2, 2, i)
        df[df[group] == i][metric].hist(bins=bins, edgecolor="black")
        plt.title(f"Distribution of {group.lower()} {i} {metric.lower()}")
        plt.xlabel(metric.capitalize())
        plt.ylabel("Frequency")
        plt.grid(False)
        plt.gca().spines["top"].set_visible(False)
        plt.gca().spines["right"].set_visible(False)

        if stats_text and i in stats_text:
            text_string = ""
            for key, value in stats_text[i].items():
                text_string += f"{key}: {value}\n"
            plt.text(
                0.95,
                0.95,
                text_string[:-1],
                transform=plt.gca().transAxes,
                fontsize=9,
                verticalalignment="top",
                horizontalalignment="left",
                bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
            )

    plt.tight_layout()
    plt.show()


def histogram_with_ci(
    means,
    scipy_lower_errors,
    scipy_upper_errors,
    bootstrap_lower_errors,
    bootstrap_upper_errors,
    scipy_ci_list,
    bootstrap_ci_list,
    title,
    ylabel,
    xlabel,
    labels,
    stats_text,
    ylim=[100000, 300000],
    figsize=(8, 5),
):
    """
    Create a grouped bar chart comparing confidence intervals calculated using scipy and bootstrap methods.

    Parameters
    ----------
    means : array-like
        Mean values for each group to plot
    scipy_lower_errors : array-like
        Lower error margins from scipy confidence intervals (distance from mean to lower bound)
    scipy_upper_errors : array-like
        Upper error margins from scipy confidence intervals (distance from mean to upper bound)
    bootstrap_lower_errors : array-like
        Lower error margins from bootstrap confidence intervals (distance from mean to lower bound)
    bootstrap_upper_errors : array-like
        Upper error margins from bootstrap confidence intervals (distance from mean to upper bound)
    scipy_ci_list : list of tuples
        List of confidence interval bounds from scipy method [(lower1, upper1), (lower2, upper2), ...]
        Used for annotation labels on the plot
    bootstrap_ci_list : list of tuples
        List of confidence interval bounds from bootstrap method [(lower1, upper1), (lower2, upper2), ...]
        Used for annotation labels on the plot
    title : str
        Title for the plot
    ylabel : str
        Label for y-axis
    xlabel : str
        Label for x-axis
    labels : list of str
        Labels for each group on x-axis (e.g., ['Promotion 1', 'Promotion 2', 'Promotion 3'])
    stats_text : str
        Statistical summary text to display in text box on the right side of the plot
    ylim : list of float, optional
        Y-axis limits [min, max]. Default is [100000, 300000].
    figsize : tuple of float, optional
        Figure size (width, height) in inches. Default is (8, 5).

    Returns
    -------
    None
        Displays the bar chart with confidence intervals and annotation labels.
    """
    x = np.arange(len(means))
    width = 0.35

    plt.figure(figsize=figsize)
    plt.subplots_adjust(left=0.1, right=0.65, top=0.95, bottom=0.1)

    plt.bar(
        x=x - width / 2,
        height=means,
        width=width,
        yerr=[scipy_lower_errors, scipy_upper_errors],
        label="Scipy CI",
        capsize=5,
    )
    plt.bar(
        x=x + width / 2,
        height=means,
        width=width,
        yerr=[bootstrap_lower_errors, bootstrap_upper_errors],
        label="Bootstrap CI",
        capsize=5,
    )
    plt.legend()
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.xticks(ticks=list(range(len(labels))), labels=labels)

    ax = plt.gca()
    ax.set_ylim(ylim)

    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)

    for i in range(len(means)):
        plt.text(
            x[i] - width / 2,
            means[i] + scipy_upper_errors[i] + 5000,
            f"{scipy_ci_list[i][0]:.0f}-\n{scipy_ci_list[i][1]:.0f}",
            ha="center",
            fontsize=8,
        )
        plt.text(
            x[i] + width / 2,
            means[i] + bootstrap_upper_errors[i] + 5000,
            f"{bootstrap_ci_list[i][0]:.0f}-\n{bootstrap_ci_list[i][1]:.0f}",
            ha="center",
            fontsize=8,
        )

    plt.text(
        1.1,
        0.95,
        stats_text,
        transform=plt.gca().transAxes,
        fontsize=9,
        verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor="lightblue", alpha=0.5),
    )
