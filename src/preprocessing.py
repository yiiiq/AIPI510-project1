import pandas as pd
import os

def load_svi_data():
    """
    Load the full SVI 2022 US county dataset.

    Returns:
        pd.DataFrame: The complete SVI dataset
    """
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "SVI_2022_US_county.csv")
    df = pd.read_csv(data_path)
    return df

def filter_gulf_coast_counties(df):
    """
    Filter the dataset to include only Gulf Coast counties.

    Args:
        df (pd.DataFrame): The full SVI dataset

    Returns:
        pd.DataFrame: Filtered dataset containing only Gulf Coast counties
    """
    gulf_states = ["TX", "LA", "MS", "AL", "FL"]
    df_gulf = df[df["ST_ABBR"].isin(gulf_states)].copy()
    return df_gulf

def clean_svi_data(df):
    """
    Clean SVI dataset by keeping only hurricane vulnerability columns.

    Args:
        df (pd.DataFrame): The raw SVI dataset

    Returns:
        pd.DataFrame: Cleaned dataset with only relevant columns
    """
    # Identification columns
    id_cols = ['STATE', 'COUNTY', 'FIPS']

    # Overall vulnerability
    overall_cols = ['RPL_THEMES']

    # Theme percentile rankings
    theme_cols = ['RPL_THEME1', 'RPL_THEME2', 'RPL_THEME3', 'RPL_THEME4']

    # Vulnerability flags (binary indicators of top 10% vulnerability)
    flag_cols = ['F_NOVEH', 'F_MOBILE', 'F_CROWD', 'F_UNINSUR', 'F_AGE65', 'F_DISABL', 'F_SNGPNT']

    # Select only the columns we need
    all_cols = id_cols + overall_cols + theme_cols + flag_cols
    df_clean = df[all_cols].copy()

    return df_clean

def create_hurricane_features(df):
    """
    Create hurricane-specific vulnerability features.

    Args:
        df (pd.DataFrame): Cleaned SVI dataset

    Returns:
        pd.DataFrame: Dataset with new hurricane vulnerability features
    """
    df = df.copy()

    # Hurricane Risk Index: Average of household characteristics + housing/transport
    df['HURRICANE_RISK_INDEX'] = (df['RPL_THEME2'] + df['RPL_THEME4']) / 2

    # Evacuation Challenge Score: Weighted combo of evacuation-related flags
    # No vehicle (60%), mobile homes (30%), crowded housing (10%)
    df['EVAC_CHALLENGE_SCORE'] = (
        df['F_NOVEH'] * 0.60 +
        df['F_MOBILE'] * 0.30 +
        df['F_CROWD'] * 0.10
    )

    # Medical Vulnerability Score: Sum of health-related flags
    df['MEDICAL_VULNERABILITY_SCORE'] = (
        df['F_AGE65'] + df['F_DISABL'] + df['F_UNINSUR']
    )

    # Flag Count: Total number of hurricane-relevant flags
    flag_columns = ['F_NOVEH', 'F_MOBILE', 'F_CROWD', 'F_UNINSUR', 'F_AGE65', 'F_DISABL', 'F_SNGPNT']
    df['FLAG_COUNT'] = df[flag_columns].sum(axis=1)

    return df

def load_and_process_gulf_data():
    """
    Complete pipeline: load, filter, clean, and engineer features for Gulf Coast data.

    Returns:
        pd.DataFrame: Processed Gulf Coast counties dataset
    """
    # Load and filter
    df = load_svi_data()
    df_gulf = filter_gulf_coast_counties(df)

    # Clean and engineer features
    df_clean = clean_svi_data(df_gulf)
    df_processed = create_hurricane_features(df_clean)

    return df_processed

if __name__ == "__main__":
    # Example usage
    df_processed = load_and_process_gulf_data()
    print(f"Processed Gulf Coast dataset shape: {df_processed.shape}")
    print(f"\nColumns: {list(df_processed.columns)}")
    print(f"\nSample of Hurricane Risk Index:")
    print(df_processed[['STATE', 'COUNTY', 'HURRICANE_RISK_INDEX']].head())
    print(f"\nTop 5 counties by Hurricane Risk Index:")
    top_risk = df_processed.nlargest(5, 'HURRICANE_RISK_INDEX')[['STATE', 'COUNTY', 'HURRICANE_RISK_INDEX']]
    print(top_risk)