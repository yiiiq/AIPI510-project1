import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for saving plots
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from typing import Optional, List

# Set consistent style
plt.style.use('default')
sns.set_palette("husl")

# Ensure reports directory exists
def ensure_reports_dir():
    reports_dir = os.path.join(os.path.dirname(__file__), '..', 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    return reports_dir

def plot_vulnerability_histograms(df: pd.DataFrame, save_path: Optional[str] = None) -> None:
    """
    Create histograms of RPL_THEMES to show vulnerability distribution.

    Args:
        df: Processed Gulf Coast dataset
        save_path: Optional path to save the figure
    """
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Gulf Coast Counties: Social Vulnerability Distribution', fontsize=16, fontweight='bold')

    # Overall vulnerability
    axes[0, 0].hist(df['RPL_THEMES'], bins=20, alpha=0.7, color='red', edgecolor='black')
    axes[0, 0].set_title('Overall Vulnerability (RPL_THEMES)')
    axes[0, 0].set_xlabel('Percentile Ranking (0=least, 1=most vulnerable)')
    axes[0, 0].set_ylabel('Number of Counties')

    # Theme histograms
    themes = ['RPL_THEME1', 'RPL_THEME2', 'RPL_THEME3', 'RPL_THEME4']
    theme_titles = [
        'Socioeconomic Status',
        'Household Characteristics',
        'Minority Status & Language',
        'Housing & Transportation'
    ]

    positions = [(0, 1), (0, 2), (1, 0), (1, 1)]

    for i, (theme, title, pos) in enumerate(zip(themes, theme_titles, positions)):
        axes[pos].hist(df[theme], bins=20, alpha=0.7, edgecolor='black')
        axes[pos].set_title(f'{title}\n({theme})')
        axes[pos].set_xlabel('Percentile Ranking')
        axes[pos].set_ylabel('Number of Counties')

    # Hurricane Risk Index
    axes[1, 2].hist(df['HURRICANE_RISK_INDEX'], bins=20, alpha=0.7, color='orange', edgecolor='black')
    axes[1, 2].set_title('Hurricane Risk Index\n(Theme2 + Theme4)/2')
    axes[1, 2].set_xlabel('Hurricane Risk Score')
    axes[1, 2].set_ylabel('Number of Counties')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    else:
        # Auto-save to reports directory
        reports_dir = ensure_reports_dir()
        save_path = os.path.join(reports_dir, 'vulnerability_histograms.png')
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"📊 Saved vulnerability histograms to: {save_path}")

    plt.close()  # Close figure to free memory

def plot_state_vulnerability_comparison(df: pd.DataFrame, save_path: Optional[str] = None) -> None:
    """
    Create bar chart comparing average theme scores by Gulf Coast state.

    Args:
        df: Processed Gulf Coast dataset
        save_path: Optional path to save the figure
    """
    # Calculate state averages
    state_avg = df.groupby('STATE')[['RPL_THEME1', 'RPL_THEME2', 'RPL_THEME3', 'RPL_THEME4']].mean()

    fig, ax = plt.subplots(figsize=(12, 8))

    # Create grouped bar chart
    x = np.arange(len(state_avg.index))
    width = 0.2

    theme_labels = ['Socioeconomic', 'Household Chars', 'Minority/Language', 'Housing/Transport']
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

    for i, (col, label, color) in enumerate(zip(state_avg.columns, theme_labels, colors)):
        ax.bar(x + i*width, state_avg[col], width, label=label, color=color, alpha=0.8)

    ax.set_xlabel('Gulf Coast State')
    ax.set_ylabel('Average Vulnerability Score')
    ax.set_title('Average Social Vulnerability Themes by Gulf Coast State', fontsize=14, fontweight='bold')
    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels(state_avg.index)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    else:
        # Auto-save to reports directory
        reports_dir = ensure_reports_dir()
        save_path = os.path.join(reports_dir, 'state_vulnerability_comparison.png')
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"📊 Saved state comparison to: {save_path}")

    plt.close()  # Close figure to free memory

def plot_top_counties_risk(df: pd.DataFrame, n_counties: int = 10, save_path: Optional[str] = None) -> None:
    """
    Plot top N counties by Hurricane Risk Index.

    Args:
        df: Processed Gulf Coast dataset
        n_counties: Number of top counties to show
        save_path: Optional path to save the figure
    """
    top_counties = df.nlargest(n_counties, 'HURRICANE_RISK_INDEX').copy()
    top_counties['COUNTY_STATE'] = top_counties['COUNTY'] + ', ' + top_counties['STATE']

    fig, ax = plt.subplots(figsize=(12, 8))

    bars = ax.barh(range(len(top_counties)), top_counties['HURRICANE_RISK_INDEX'],
                   color='red', alpha=0.7, edgecolor='black')

    # Add value labels on bars
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width + 0.01, bar.get_y() + bar.get_height()/2,
                f'{width:.3f}', ha='left', va='center', fontweight='bold')

    ax.set_yticks(range(len(top_counties)))
    ax.set_yticklabels(top_counties['COUNTY_STATE'])
    ax.set_xlabel('Hurricane Risk Index')
    ax.set_title(f'Top {n_counties} Gulf Coast Counties by Hurricane Risk Index',
                 fontsize=14, fontweight='bold')
    ax.grid(axis='x', alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    else:
        # Auto-save to reports directory
        reports_dir = ensure_reports_dir()
        save_path = os.path.join(reports_dir, f'top_{n_counties}_counties_risk.png')
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"📊 Saved top counties chart to: {save_path}")

    plt.close()  # Close figure to free memory

def plot_vulnerability_flags_correlation(df: pd.DataFrame, save_path: Optional[str] = None) -> None:
    """
    Create correlation heatmap of vulnerability flags.

    Args:
        df: Processed Gulf Coast dataset
        save_path: Optional path to save the figure
    """
    flag_cols = ['F_NOVEH', 'F_MOBILE', 'F_CROWD', 'F_UNINSUR', 'F_AGE65', 'F_DISABL', 'F_SNGPNT']
    flag_labels = ['No Vehicle', 'Mobile Home', 'Crowded Housing', 'No Insurance',
                   'Elderly (65+)', 'Disabled', 'Single Parent']

    # Calculate correlation matrix
    corr_matrix = df[flag_cols].corr()

    fig, ax = plt.subplots(figsize=(10, 8))

    # Create heatmap
    sns.heatmap(corr_matrix, annot=True, cmap='RdYlBu_r', center=0,
                square=True, linewidths=0.5, cbar_kws={"shrink": .8},
                xticklabels=flag_labels, yticklabels=flag_labels)

    ax.set_title('Correlation Matrix: Hurricane Vulnerability Flags',
                 fontsize=14, fontweight='bold', pad=20)

    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    else:
        # Auto-save to reports directory
        reports_dir = ensure_reports_dir()
        save_path = os.path.join(reports_dir, 'vulnerability_flags_correlation.png')
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"📊 Saved correlation heatmap to: {save_path}")

    plt.close()  # Close figure to free memory

def plot_risk_scores_comparison(df: pd.DataFrame, save_path: Optional[str] = None) -> None:
    """
    Compare the different risk scores we created.

    Args:
        df: Processed Gulf Coast dataset
        save_path: Optional path to save the figure
    """
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Hurricane Vulnerability Risk Scores Comparison', fontsize=16, fontweight='bold')

    # Hurricane Risk Index
    axes[0, 0].hist(df['HURRICANE_RISK_INDEX'], bins=20, alpha=0.7, color='red', edgecolor='black')
    axes[0, 0].set_title('Hurricane Risk Index')
    axes[0, 0].set_xlabel('Risk Score')
    axes[0, 0].set_ylabel('Number of Counties')

    # Evacuation Challenge Score
    axes[0, 1].hist(df['EVAC_CHALLENGE_SCORE'], bins=20, alpha=0.7, color='orange', edgecolor='black')
    axes[0, 1].set_title('Evacuation Challenge Score')
    axes[0, 1].set_xlabel('Challenge Score')
    axes[0, 1].set_ylabel('Number of Counties')

    # Medical Vulnerability Score
    axes[1, 0].hist(df['MEDICAL_VULNERABILITY_SCORE'], bins=range(0, 4), alpha=0.7,
                    color='blue', edgecolor='black', align='left')
    axes[1, 0].set_title('Medical Vulnerability Score')
    axes[1, 0].set_xlabel('Number of Medical Risk Factors')
    axes[1, 0].set_ylabel('Number of Counties')
    axes[1, 0].set_xticks(range(0, 4))

    # Flag Count
    axes[1, 1].hist(df['FLAG_COUNT'], bins=range(0, 8), alpha=0.7,
                    color='green', edgecolor='black', align='left')
    axes[1, 1].set_title('Total Vulnerability Flags')
    axes[1, 1].set_xlabel('Number of Risk Flags')
    axes[1, 1].set_ylabel('Number of Counties')
    axes[1, 1].set_xticks(range(0, 8))

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    else:
        # Auto-save to reports directory
        reports_dir = ensure_reports_dir()
        save_path = os.path.join(reports_dir, 'risk_scores_comparison.png')
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"📊 Saved risk scores comparison to: {save_path}")

    plt.close()  # Close figure to free memory

def create_vulnerability_dashboard(df: pd.DataFrame, save_path: Optional[str] = None) -> None:
    """
    Create a comprehensive dashboard with key visualizations.

    Args:
        df: Processed Gulf Coast dataset
        save_path: Optional path to save the figure
    """
    print("Creating Gulf Coast Hurricane Vulnerability Dashboard...")
    print("=" * 60)

    # Generate all visualizations
    plot_vulnerability_histograms(df)
    plot_state_vulnerability_comparison(df)
    plot_top_counties_risk(df)
    plot_vulnerability_flags_correlation(df)
    plot_risk_scores_comparison(df)

    print("Dashboard creation complete!")

if __name__ == "__main__":
    from preprocessing import load_and_process_gulf_data

    # Load processed data
    df = load_and_process_gulf_data()

    # Create dashboard
    create_vulnerability_dashboard(df)