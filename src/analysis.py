import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional

def analyze_evacuation_barriers(df: pd.DataFrame) -> Dict:
    """
    Analyze evacuation barriers using RPL_THEME4 (Housing/Transportation).

    Args:
        df: Processed Gulf Coast dataset

    Returns:
        Dict: Analysis results for evacuation challenges
    """
    analysis = {}

    # Overall evacuation challenge statistics
    analysis['total_counties'] = len(df)
    analysis['high_evacuation_risk'] = len(df[df['RPL_THEME4'] >= 0.75])
    analysis['high_evacuation_pct'] = (analysis['high_evacuation_risk'] / analysis['total_counties']) * 100

    # Top evacuation challenge counties
    analysis['top_evacuation_counties'] = df.nlargest(10, 'RPL_THEME4')[
        ['STATE', 'COUNTY', 'RPL_THEME4', 'F_NOVEH', 'F_MOBILE']
    ].to_dict('records')

    # State-level evacuation challenges
    state_evac = df.groupby('STATE').agg({
        'RPL_THEME4': ['mean', 'count'],
        'F_NOVEH': 'sum',
        'F_MOBILE': 'sum'
    }).round(3)

    state_evac.columns = ['avg_evacuation_risk', 'county_count', 'no_vehicle_flags', 'mobile_home_flags']
    analysis['state_evacuation_summary'] = state_evac.to_dict('index')

    return analysis

def analyze_vulnerable_populations(df: pd.DataFrame) -> Dict:
    """
    Analyze vulnerable populations using RPL_THEME2 (Household Characteristics).

    Args:
        df: Processed Gulf Coast dataset

    Returns:
        Dict: Analysis results for vulnerable populations
    """
    analysis = {}

    # Overall population vulnerability
    analysis['high_population_vulnerability'] = len(df[df['RPL_THEME2'] >= 0.75])
    analysis['high_pop_vuln_pct'] = (analysis['high_population_vulnerability'] / len(df)) * 100

    # Top vulnerable population counties
    analysis['top_vulnerable_pop_counties'] = df.nlargest(10, 'RPL_THEME2')[
        ['STATE', 'COUNTY', 'RPL_THEME2', 'F_AGE65', 'F_DISABL', 'F_SNGPNT']
    ].to_dict('records')

    # Medical vulnerability analysis
    analysis['medical_vulnerability_distribution'] = df['MEDICAL_VULNERABILITY_SCORE'].value_counts().sort_index().to_dict()

    # Counties with multiple medical vulnerabilities
    analysis['high_medical_risk_counties'] = len(df[df['MEDICAL_VULNERABILITY_SCORE'] >= 2])
    analysis['high_medical_risk_pct'] = (analysis['high_medical_risk_counties'] / len(df)) * 100

    return analysis

def create_hurricane_risk_profile(df: pd.DataFrame) -> Dict:
    """
    Create comprehensive hurricane risk profiles for Gulf Coast counties.

    Args:
        df: Processed Gulf Coast dataset

    Returns:
        Dict: Hurricane risk analysis results
    """
    analysis = {}

    # Hurricane Risk Index statistics
    analysis['hurricane_risk_stats'] = {
        'mean': df['HURRICANE_RISK_INDEX'].mean(),
        'median': df['HURRICANE_RISK_INDEX'].median(),
        'std': df['HURRICANE_RISK_INDEX'].std(),
        'min': df['HURRICANE_RISK_INDEX'].min(),
        'max': df['HURRICANE_RISK_INDEX'].max()
    }

    # Risk categories
    analysis['risk_categories'] = {
        'very_high_risk': len(df[df['HURRICANE_RISK_INDEX'] >= 0.8]),
        'high_risk': len(df[(df['HURRICANE_RISK_INDEX'] >= 0.6) & (df['HURRICANE_RISK_INDEX'] < 0.8)]),
        'moderate_risk': len(df[(df['HURRICANE_RISK_INDEX'] >= 0.4) & (df['HURRICANE_RISK_INDEX'] < 0.6)]),
        'low_risk': len(df[df['HURRICANE_RISK_INDEX'] < 0.4])
    }

    # Top 15 most at-risk counties
    top_risk = df.nlargest(15, 'HURRICANE_RISK_INDEX')
    analysis['highest_risk_counties'] = top_risk[
        ['STATE', 'COUNTY', 'HURRICANE_RISK_INDEX', 'RPL_THEME2', 'RPL_THEME4',
         'EVAC_CHALLENGE_SCORE', 'MEDICAL_VULNERABILITY_SCORE', 'FLAG_COUNT']
    ].to_dict('records')

    # Worst-case scenario counties (high in both evacuation AND medical risks)
    worst_case = df[
        (df['RPL_THEME4'] >= 0.75) & (df['MEDICAL_VULNERABILITY_SCORE'] >= 2)
    ]
    analysis['worst_case_counties'] = worst_case[
        ['STATE', 'COUNTY', 'HURRICANE_RISK_INDEX', 'RPL_THEME4', 'MEDICAL_VULNERABILITY_SCORE']
    ].to_dict('records')
    analysis['worst_case_count'] = len(worst_case)

    return analysis

def generate_storytelling_insights(df: pd.DataFrame) -> Dict:
    """
    Generate key storytelling insights for hurricane vulnerability analysis.

    Args:
        df: Processed Gulf Coast dataset

    Returns:
        Dict: Key insights for storytelling
    """
    insights = {}

    # Key statistics
    insights['total_counties'] = len(df)
    insights['total_states'] = df['STATE'].nunique()

    # Top vulnerability themes
    theme_means = {
        'socioeconomic': df['RPL_THEME1'].mean(),
        'household_characteristics': df['RPL_THEME2'].mean(),
        'minority_language': df['RPL_THEME3'].mean(),
        'housing_transportation': df['RPL_THEME4'].mean()
    }
    insights['most_challenging_theme'] = max(theme_means, key=theme_means.get)
    insights['theme_rankings'] = sorted(theme_means.items(), key=lambda x: x[1], reverse=True)

    # State comparisons
    state_risk = df.groupby('STATE')['HURRICANE_RISK_INDEX'].mean().sort_values(ascending=False)
    insights['highest_risk_state'] = state_risk.index[0]
    insights['lowest_risk_state'] = state_risk.index[-1]
    insights['state_risk_rankings'] = state_risk.to_dict()

    # Flag analysis
    flag_cols = ['F_NOVEH', 'F_MOBILE', 'F_CROWD', 'F_UNINSUR', 'F_AGE65', 'F_DISABL', 'F_SNGPNT']
    flag_totals = df[flag_cols].sum().sort_values(ascending=False)
    insights['most_common_vulnerability'] = flag_totals.index[0]
    insights['vulnerability_flag_counts'] = flag_totals.to_dict()

    # Multiple vulnerability analysis
    insights['counties_with_5plus_flags'] = len(df[df['FLAG_COUNT'] >= 5])
    insights['counties_with_all_flags'] = len(df[df['FLAG_COUNT'] == 7])

    # Evacuation specific insights
    evacuation_critical = df[df['F_NOVEH'] == 1]
    insights['no_vehicle_counties'] = len(evacuation_critical)
    insights['no_vehicle_pct'] = (len(evacuation_critical) / len(df)) * 100

    mobile_home_critical = df[df['F_MOBILE'] == 1]
    insights['mobile_home_counties'] = len(mobile_home_critical)
    insights['mobile_home_pct'] = (len(mobile_home_critical) / len(df)) * 100

    return insights

def create_executive_summary(df: pd.DataFrame) -> str:
    """
    Create an executive summary of hurricane vulnerability findings.

    Args:
        df: Processed Gulf Coast dataset

    Returns:
        str: Executive summary text
    """
    insights = generate_storytelling_insights(df)
    evacuation_analysis = analyze_evacuation_barriers(df)
    population_analysis = analyze_vulnerable_populations(df)
    risk_profile = create_hurricane_risk_profile(df)

    summary = f"""
GULF COAST HURRICANE VULNERABILITY ANALYSIS - EXECUTIVE SUMMARY

SCOPE:
• {insights['total_counties']} counties across {insights['total_states']} Gulf Coast states
• Focus on evacuation barriers, vulnerable populations, and hurricane preparedness

KEY FINDINGS:

1. EVACUATION CHALLENGES:
• {evacuation_analysis['high_evacuation_pct']:.1f}% of counties ({evacuation_analysis['high_evacuation_risk']}) face severe evacuation barriers
• {insights['no_vehicle_pct']:.1f}% of counties have populations with limited vehicle access
• {insights['mobile_home_pct']:.1f}% of counties have significant mobile home populations

2. VULNERABLE POPULATIONS:
• {population_analysis['high_pop_vuln_pct']:.1f}% of counties have high concentrations of vulnerable households
• {population_analysis['high_medical_risk_pct']:.1f}% of counties face significant medical vulnerability challenges
• Most common vulnerability: {insights['most_common_vulnerability'].replace('F_', '').replace('_', ' ').title()}

3. HURRICANE RISK PROFILE:
• {risk_profile['risk_categories']['very_high_risk']} counties classified as very high risk
• {risk_profile['risk_categories']['high_risk']} counties classified as high risk
• Worst-case counties (high evacuation barriers + medical vulnerability): {risk_profile['worst_case_count']}

4. STATE COMPARISONS:
• Highest average risk: {insights['highest_risk_state']} ({insights['state_risk_rankings'][insights['highest_risk_state']]:.3f})
• Lowest average risk: {insights['lowest_risk_state']} ({insights['state_risk_rankings'][insights['lowest_risk_state']]:.3f})

RECOMMENDATION: Priority should be given to the {risk_profile['risk_categories']['very_high_risk']} counties with
Hurricane Risk Index scores above 0.8, focusing on evacuation planning and medical preparedness.
"""

    return summary

def print_detailed_analysis(df: pd.DataFrame) -> None:
    """
    Print comprehensive analysis results.

    Args:
        df: Processed Gulf Coast dataset
    """
    print("GULF COAST HURRICANE VULNERABILITY ANALYSIS")
    print("=" * 60)

    # Executive Summary
    print(create_executive_summary(df))

    # Detailed breakdowns
    print("\nTOP 10 HIGHEST RISK COUNTIES:")
    print("-" * 40)
    top_counties = df.nlargest(10, 'HURRICANE_RISK_INDEX')
    for _, county in top_counties.iterrows():
        print(f"{county['COUNTY']}, {county['STATE']}: {county['HURRICANE_RISK_INDEX']:.3f}")

    print("\nEVACUATION BARRIER ANALYSIS:")
    print("-" * 40)
    evacuation_analysis = analyze_evacuation_barriers(df)
    for state, data in evacuation_analysis['state_evacuation_summary'].items():
        print(f"{state}: Avg Risk {data['avg_evacuation_risk']:.3f}, "
              f"No Vehicle: {data['no_vehicle_flags']}, Mobile Homes: {data['mobile_home_flags']}")

    print("\nVULNERABILITY FLAG DISTRIBUTION:")
    print("-" * 40)
    insights = generate_storytelling_insights(df)
    for flag, count in insights['vulnerability_flag_counts'].items():
        flag_name = flag.replace('F_', '').replace('_', ' ').title()
        print(f"{flag_name}: {count} counties ({count/len(df)*100:.1f}%)")

if __name__ == "__main__":
    from preprocessing import load_and_process_gulf_data

    # Load processed data
    df = load_and_process_gulf_data()

    # Run comprehensive analysis
    print_detailed_analysis(df)