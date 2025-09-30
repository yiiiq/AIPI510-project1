#!/usr/bin/env python3
"""
Gulf Coast Hurricane Vulnerability Analysis - Main Script

This script provides a complete pipeline for analyzing hurricane vulnerability
in Gulf Coast counties using Social Vulnerability Index (SVI) data.

Usage:
    python src/main.py [options]

Options:
    --analysis-only    Run only the analysis (no visualizations)
    --viz-only         Run only visualizations (no analysis)
    --save-plots       Save all plots to reports/ directory

"""

import argparse
import os
import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.append(str(Path(__file__).parent))

from preprocessing import load_and_process_gulf_data
from analysis import print_detailed_analysis, create_executive_summary
from visualization import create_vulnerability_dashboard
from mapping import create_mapping_dashboard, create_enhanced_mapping_dashboard

def ensure_reports_directory():
    """Create reports directory if it doesn't exist."""
    reports_dir = Path(__file__).parent.parent / "reports"
    reports_dir.mkdir(exist_ok=True)
    return reports_dir

def run_full_analysis(save_plots=False):
    """
    Run the complete hurricane vulnerability analysis pipeline.

    Args:
        save_plots: Whether to save plots to reports directory
    """
    print("🌀 GULF COAST HURRICANE VULNERABILITY ANALYSIS")
    print("=" * 60)

    # Load and process data
    print("\n📊 Loading and processing SVI data...")
    df = load_and_process_gulf_data()
    print(f"✅ Processed {len(df)} Gulf Coast counties")

    # Set up reports directory if saving plots
    if save_plots:
        reports_dir = ensure_reports_directory()
        print(f"📁 Plots will be saved to: {reports_dir}")

    # Run analysis
    print("\n🔍 RUNNING DETAILED ANALYSIS:")
    print_detailed_analysis(df)

    # Create visualizations
    print("\n📈 CREATING VISUALIZATIONS:")
    create_vulnerability_dashboard(df)

    # Create maps - use enhanced mapping if geopandas available
    print("\n🗺️  CREATING VULNERABILITY MAPS:")
    try:
        create_enhanced_mapping_dashboard(df)
    except Exception as e:
        print(f"⚠️ Enhanced mapping failed: {e}")
        print("Falling back to simplified mapping...")
        create_mapping_dashboard(df)

    # Save executive summary
    if save_plots:
        summary = create_executive_summary(df)
        summary_path = reports_dir / "executive_summary.txt"
        with open(summary_path, 'w') as f:
            f.write(summary)
        print(f"📄 Executive summary saved to: {summary_path}")

    print("\n✨ ANALYSIS COMPLETE!")
    print("=" * 60)

def run_analysis_only():
    """Run only the statistical analysis without visualizations."""
    print("🔍 GULF COAST HURRICANE VULNERABILITY - ANALYSIS ONLY")
    print("=" * 60)

    df = load_and_process_gulf_data()
    print_detailed_analysis(df)

def run_visualizations_only(save_plots=False):
    """Run only the visualizations without detailed analysis."""
    print("📊 GULF COAST HURRICANE VULNERABILITY - VISUALIZATIONS")
    print("=" * 60)

    df = load_and_process_gulf_data()

    if save_plots:
        ensure_reports_directory()

    print("Creating vulnerability dashboard...")
    create_vulnerability_dashboard(df)

    print("Creating mapping dashboard...")
    try:
        create_enhanced_mapping_dashboard(df)
    except Exception as e:
        print(f"⚠️ Enhanced mapping failed: {e}")
        print("Falling back to simplified mapping...")
        create_mapping_dashboard(df)

def main():
    """Main function with command line argument parsing."""
    parser = argparse.ArgumentParser(
        description="Gulf Coast Hurricane Vulnerability Analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python src/main.py                    # Run full analysis
    python src/main.py --analysis-only    # Run analysis without plots
    python src/main.py --viz-only         # Run visualizations only
    python src/main.py --save-plots       # Save all plots to reports/
        """
    )

    parser.add_argument('--analysis-only', action='store_true',
                       help='Run only statistical analysis (no visualizations)')
    parser.add_argument('--viz-only', action='store_true',
                       help='Run only visualizations (no detailed analysis)')
    parser.add_argument('--save-plots', action='store_true',
                       help='Save plots to reports/ directory')

    args = parser.parse_args()

    try:
        if args.analysis_only:
            run_analysis_only()
        elif args.viz_only:
            run_visualizations_only(save_plots=args.save_plots)
        else:
            run_full_analysis(save_plots=args.save_plots)

    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()