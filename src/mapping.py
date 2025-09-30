import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import os
from typing import Optional, Dict, Any

# Try to import geopandas for real choropleth maps
try:
    import geopandas as gpd
    GEOPANDAS_AVAILABLE = True
    print("GeoPandas available - real choropleth maps enabled!")
except ImportError:
    GEOPANDAS_AVAILABLE = False
    print("GeoPandas not available - using simplified scatter plot maps")

# Ensure reports directory exists
def ensure_reports_dir():
    reports_dir = os.path.join(os.path.dirname(__file__), '..', 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    return reports_dir

def create_choropleth_data(df: pd.DataFrame, value_column: str) -> pd.DataFrame:
    """
    Prepare data for choropleth mapping by formatting FIPS codes.

    Args:
        df: Processed Gulf Coast dataset
        value_column: Column name to visualize

    Returns:
        pd.DataFrame: Data formatted for mapping
    """
    map_data = df[['FIPS', 'STATE', 'COUNTY', value_column]].copy()

    # Ensure FIPS is string and properly formatted
    map_data['FIPS'] = map_data['FIPS'].astype(str).str.zfill(5)

    # Create display name
    map_data['DISPLAY_NAME'] = map_data['COUNTY'] + ', ' + map_data['STATE']

    return map_data

def plot_simple_choropleth(df: pd.DataFrame, value_column: str, title: str,
                          save_path: Optional[str] = None) -> None:
    """
    Create a simplified choropleth-style visualization using scatter plot.
    This is a fallback when geographic shapefiles aren't available.

    Args:
        df: Processed Gulf Coast dataset
        value_column: Column to visualize
        title: Plot title
        save_path: Optional path to save figure
    """
    # Create approximate geographic positions based on state
    # Handle both abbreviations and full state names
    state_positions = {
        'TX': (-98, 31), 'Texas': (-98, 31),
        'LA': (-92, 31), 'Louisiana': (-92, 31),
        'MS': (-89, 32.5), 'Mississippi': (-89, 32.5),
        'AL': (-86.5, 32.5), 'Alabama': (-86.5, 32.5),
        'FL': (-82, 28), 'Florida': (-82, 28)
    }

    # Check what state values we actually have
    unique_states = df['STATE'].unique()
    print(f"States in dataset: {unique_states}")

    # Use the states that exist in our data
    valid_positions = {}
    for state in unique_states:
        if state in state_positions:
            valid_positions[state] = state_positions[state]
        else:
            print(f"Warning: State '{state}' not found in position mapping")
            # Default position if state not found
            valid_positions[state] = (-90, 30)

    state_positions = valid_positions

    # Add some random offset to spread counties within states
    np.random.seed(42)
    plot_data = df.copy()
    plot_data['lon'] = plot_data['STATE'].map(lambda x: state_positions.get(x, (-90, 30))[0]) + np.random.normal(0, 1, len(df))
    plot_data['lat'] = plot_data['STATE'].map(lambda x: state_positions.get(x, (-90, 30))[1]) + np.random.normal(0, 0.5, len(df))

    fig, ax = plt.subplots(figsize=(12, 8))

    # Create scatter plot with color mapping
    scatter = ax.scatter(plot_data['lon'], plot_data['lat'], c=plot_data[value_column],
                        s=60, alpha=0.7, cmap='Reds', edgecolors='black', linewidth=0.5)

    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label(value_column.replace('_', ' ').title())

    # Customize plot
    ax.set_xlabel('Approximate Longitude')
    ax.set_ylabel('Approximate Latitude')
    ax.set_title(title, fontsize=14, fontweight='bold')

    # Add state labels
    for state, (lon, lat) in state_positions.items():
        ax.text(lon, lat + 1, state, fontsize=12, fontweight='bold',
                ha='center', va='center', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    else:
        # Auto-save to reports directory
        reports_dir = ensure_reports_dir()
        filename = f'{value_column.lower()}_choropleth.png'
        save_path = os.path.join(reports_dir, filename)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"🗺️ Saved choropleth map to: {save_path}")

    plt.close()  # Close figure to free memory

def create_county_ranking_map(df: pd.DataFrame, value_column: str, top_n: int = 20,
                             title: str = None, save_path: Optional[str] = None) -> None:
    """
    Highlight top N counties by risk score on a simplified map.

    Args:
        df: Processed Gulf Coast dataset
        value_column: Column to rank by
        top_n: Number of top counties to highlight
        title: Plot title
        save_path: Optional path to save figure
    """
    if title is None:
        title = f"Top {top_n} Counties by {value_column.replace('_', ' ').title()}"

    # Get top counties
    top_counties = df.nlargest(top_n, value_column)

    # State positions - handle both abbreviations and full state names
    state_positions = {
        'TX': (-98, 31), 'Texas': (-98, 31),
        'LA': (-92, 31), 'Louisiana': (-92, 31),
        'MS': (-89, 32.5), 'Mississippi': (-89, 32.5),
        'AL': (-86.5, 32.5), 'Alabama': (-86.5, 32.5),
        'FL': (-82, 28), 'Florida': (-82, 28)
    }

    # Check what state values we actually have and create safe mapping
    unique_states = df['STATE'].unique()
    valid_positions = {}
    for state in unique_states:
        if state in state_positions:
            valid_positions[state] = state_positions[state]
        else:
            print(f"Warning: State '{state}' not found in position mapping")
            valid_positions[state] = (-90, 30)  # Default position

    state_positions = valid_positions

    # Create plot data
    np.random.seed(42)
    plot_data = df.copy()
    plot_data['lon'] = plot_data['STATE'].map(lambda x: state_positions.get(x, (-90, 30))[0]) + np.random.normal(0, 1, len(df))
    plot_data['lat'] = plot_data['STATE'].map(lambda x: state_positions.get(x, (-90, 30))[1]) + np.random.normal(0, 0.5, len(df))

    fig, ax = plt.subplots(figsize=(14, 10))

    # Plot all counties in light gray
    ax.scatter(plot_data['lon'], plot_data['lat'], c='lightgray',
              s=30, alpha=0.5, edgecolors='gray', linewidth=0.3)

    # Highlight top counties
    top_data = plot_data[plot_data['FIPS'].isin(top_counties['FIPS'])]
    scatter = ax.scatter(top_data['lon'], top_data['lat'], c=top_data[value_column],
                        s=100, alpha=0.8, cmap='Reds', edgecolors='black', linewidth=1)

    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label(value_column.replace('_', ' ').title())

    # Label top 5 counties
    top_5 = top_counties.head(5)
    for _, county in top_5.iterrows():
        county_data = plot_data[plot_data['FIPS'] == county['FIPS']].iloc[0]
        ax.annotate(f"{county['COUNTY']}, {county['STATE']}\n({county[value_column]:.3f})",
                   (county_data['lon'], county_data['lat']),
                   xytext=(10, 10), textcoords='offset points',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                   fontsize=8, ha='left')

    # Add state labels
    for state, (lon, lat) in state_positions.items():
        ax.text(lon, lat + 2, state, fontsize=14, fontweight='bold',
                ha='center', va='center', bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

    ax.set_xlabel('Approximate Longitude')
    ax.set_ylabel('Approximate Latitude')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    else:
        # Auto-save to reports directory
        reports_dir = ensure_reports_dir()
        filename = f'top_{top_n}_{value_column.lower()}_map.png'
        save_path = os.path.join(reports_dir, filename)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"🗺️ Saved county ranking map to: {save_path}")

    plt.close()  # Close figure to free memory

def create_mapping_dashboard(df: pd.DataFrame) -> None:
    """
    Create a series of choropleth-style maps for hurricane vulnerability analysis.

    Args:
        df: Processed Gulf Coast dataset
    """
    print("Creating Hurricane Vulnerability Maps...")
    print("=" * 50)

    # Hurricane Risk Index map
    plot_simple_choropleth(df, 'HURRICANE_RISK_INDEX',
                          'Gulf Coast Hurricane Risk Index by County')

    # Evacuation Challenge map
    plot_simple_choropleth(df, 'EVAC_CHALLENGE_SCORE',
                          'Evacuation Challenge Score by County')

    # Overall vulnerability map
    plot_simple_choropleth(df, 'RPL_THEMES',
                          'Overall Social Vulnerability by County')

    # Top counties maps
    create_county_ranking_map(df, 'HURRICANE_RISK_INDEX', top_n=15,
                             title='Top 15 Counties by Hurricane Risk')

    create_county_ranking_map(df, 'EVAC_CHALLENGE_SCORE', top_n=15,
                             title='Top 15 Counties by Evacuation Challenge')

    print("Mapping dashboard complete!")

def plot_real_choropleth(df: pd.DataFrame, value_column: str, title: str = None,
                        shapefile_path: str = None, save_path: Optional[str] = None) -> None:
    """
    Create a real choropleth map using geopandas with US county boundaries.

    Args:
        df: Processed Gulf Coast dataset
        value_column: Column to visualize
        title: Plot title
        shapefile_path: Path to shapefile, if None tries to download from web
        save_path: Optional path to save figure
    """
    if not GEOPANDAS_AVAILABLE:
        print("GeoPandas not available. Install with: pip install geopandas")
        print("Falling back to simplified map...")
        plot_simple_choropleth(df, value_column, title or f"{value_column} Choropleth", save_path)
        return

    try:
        # Try to load counties shapefile
        if shapefile_path and os.path.exists(shapefile_path):
            print(f"📁 Loading shapefile from: {shapefile_path}")
            counties = gpd.read_file(shapefile_path)
        else:
            # Try to use built-in geopandas data or download from web
            try:
                print("Downloading US counties data from natural earth...")
                counties = gpd.read_file("https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json")
                # Rename FIPS column if needed
                if 'id' in counties.columns:
                    counties['FIPS'] = counties['id'].astype(str).str.zfill(5)
            except:
                print("Could not download county boundaries. Using simplified map...")
                plot_simple_choropleth(df, value_column, title or f"{value_column} Choropleth", save_path)
                return

        # Prepare data for merging
        df_map = df.copy()
        df_map['FIPS'] = df_map['FIPS'].astype(str).str.zfill(5)

        # Merge with geography
        if 'FIPS' in counties.columns:
            gulf_map = counties.merge(df_map, on='FIPS', how='inner')
        elif 'GEOID' in counties.columns:
            counties['FIPS'] = counties['GEOID'].astype(str).str.zfill(5)
            gulf_map = counties.merge(df_map, on='FIPS', how='inner')
        else:
            print("Could not find matching FIPS/GEOID column in shapefile")
            plot_simple_choropleth(df, value_column, title or f"{value_column} Choropleth", save_path)
            return

        print(f"Successfully merged {len(gulf_map)} counties with geographic boundaries")

        # Create the choropleth map
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plot the choropleth
        gulf_map.plot(column=value_column,
                     cmap='Reds',
                     legend=True,
                     ax=ax,
                     edgecolor='white',
                     linewidth=0.5,
                     legend_kwds={'shrink': 0.8, 'aspect': 20})

        # Customize the map
        ax.set_title(title or f"Gulf Coast {value_column.replace('_', ' ').title()}",
                    fontsize=16, fontweight='bold', pad=20)
        ax.axis('off')  # Remove axes for cleaner map

        # Add state labels
        state_centers = gulf_map.dissolve(by='STATE').centroid
        for state, center in state_centers.items():
            ax.text(center.x, center.y, state, fontsize=12, fontweight='bold',
                   ha='center', va='center',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
        else:
            # Auto-save to reports directory
            reports_dir = ensure_reports_dir()
            filename = f'real_{value_column.lower()}_choropleth.png'
            save_path = os.path.join(reports_dir, filename)
            plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
            print(f"🗺️ Saved real choropleth map to: {save_path}")

        plt.close()

    except Exception as e:
        print(f"Error creating real choropleth: {e}")
        print("Falling back to simplified map...")
        plot_simple_choropleth(df, value_column, title or f"{value_column} Choropleth", save_path)

def download_us_counties_shapefile(data_dir: str = "data/shapefiles") -> str:
    """
    Download US counties shapefile from Census Bureau.

    Args:
        data_dir: Directory to save shapefile

    Returns:
        Path to downloaded shapefile
    """
    if not GEOPANDAS_AVAILABLE:
        print("GeoPandas not available for downloading shapefiles")
        return None

    try:
        import urllib.request
        import zipfile

        # Create directory
        os.makedirs(data_dir, exist_ok=True)

        # Census Bureau URL for county shapefiles
        url = "https://www2.census.gov/geo/tiger/GENZ2022/shp/cb_2022_us_county_500k.zip"
        zip_path = os.path.join(data_dir, "counties.zip")
        shapefile_path = os.path.join(data_dir, "cb_2022_us_county_500k.shp")

        if os.path.exists(shapefile_path):
            print(f"Shapefile already exists at: {shapefile_path}")
            return shapefile_path

        print("Downloading US counties shapefile from Census Bureau...")
        urllib.request.urlretrieve(url, zip_path)

        print("Extracting shapefile...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(data_dir)

        os.remove(zip_path)  # Clean up zip file
        print(f"Shapefile downloaded to: {shapefile_path}")
        return shapefile_path

    except Exception as e:
        print(f"Error downloading shapefile: {e}")
        return None

def create_enhanced_mapping_dashboard(df: pd.DataFrame, shapefile_path: str = None) -> None:
    """
    Create enhanced mapping dashboard with real choropleth maps if possible.

    Args:
        df: Processed Gulf Coast dataset
        shapefile_path: Optional path to US counties shapefile
    """
    print("Creating Enhanced Hurricane Vulnerability Maps...")
    print("=" * 55)

    # Try to use real choropleth maps first
    if GEOPANDAS_AVAILABLE:
        print("Creating real choropleth maps with county boundaries...")

        # Download shapefile if not provided
        if not shapefile_path:
            data_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'shapefiles')
            shapefile_path = download_us_counties_shapefile(data_dir)

        # Create real choropleth maps
        plot_real_choropleth(df, 'HURRICANE_RISK_INDEX',
                           'Gulf Coast Hurricane Risk Index by County', shapefile_path)

        plot_real_choropleth(df, 'EVAC_CHALLENGE_SCORE',
                           'Evacuation Challenge Score by County', shapefile_path)

        plot_real_choropleth(df, 'RPL_THEMES',
                           'Overall Social Vulnerability by County', shapefile_path)

        print("Enhanced mapping dashboard complete!")
    else:
        print("GeoPandas not available - falling back to simplified maps")
        create_mapping_dashboard(df)

if __name__ == "__main__":
    from preprocessing import load_and_process_gulf_data

    # Load processed data
    df = load_and_process_gulf_data()

    # Create mapping dashboard
    create_mapping_dashboard(df)