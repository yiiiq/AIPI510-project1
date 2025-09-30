# 🌀 Gulf Coast Hurricane Vulnerability Analysis

A comprehensive analysis of hurricane vulnerability in Gulf Coast counties using the CDC's Social Vulnerability Index (SVI) 2022 dataset. This project identifies counties most at risk during hurricane events by analyzing evacuation barriers, vulnerable populations, and housing characteristics.

## 📊 Project Overview

This analysis focuses on **Gulf Coast states** (Texas, Louisiana, Mississippi, Alabama, Florida) to understand:

- **Evacuation Challenges**: Which counties face the greatest barriers to hurricane evacuation
- **Vulnerable Populations**: Where elderly, disabled, and medically fragile populations are concentrated
- **Housing Vulnerability**: Areas with mobile homes, crowded housing, and transportation limitations
- **Hurricane Risk Index**: A composite score combining household characteristics and housing/transportation vulnerabilities

## 🏗️ Project Structure

```
project1/
├── data/
│   ├── SVI_2022_US_county.csv          # CDC Social Vulnerability Index data
│   └── shapefiles/                     # Auto-downloaded US county boundaries
├── src/
│   ├── preprocessing.py                 # Data cleaning and feature engineering
│   ├── visualization.py                 # Charts, histograms, and correlation plots
│   ├── mapping.py                      # Geographic visualizations (real + simplified)
│   ├── analysis.py                     # Statistical analysis and insights
│   ├── main.py                         # Complete analysis pipeline
│   └── example_usage.py                # Usage examples for Jupyter notebooks
├── notebook/
│   └── exploration.ipynb               # Interactive analysis notebook
├── reports/                            # Generated plots and summaries
└── README.md
```

## ⚡ Quick Start

### Option 1: Complete Analysis Pipeline
Run the full analysis with all visualizations:

```bash
python src/main.py
```

### Option 2: Command Line Options
```bash
# Analysis only (no visualizations)
python src/main.py --analysis-only

# Visualizations only
python src/main.py --viz-only

# Save all plots to reports/ directory
python src/main.py --save-plots
```


### ✅ **Real Choropleth Maps** (with GeoPandas)
- **Actual US county boundaries** using Census Bureau shapefiles
- **Professional geographic visualization** with proper county shapes
- **Auto-downloads** US Census TIGER/Line shapefiles (16MB) on first use
- **Color-coded counties** showing exact geographic risk distribution

### 📊 **Simplified Maps** (without GeoPandas)
- **Geographic scatter plots** with approximate state positions
- **Still shows regional patterns** and identifies high-risk areas
- **No additional dependencies** required
- **Lightweight fallback** that works everywhere

**To enable real maps:**
```bash
pip install geopandas
```

## 🔍 Key Features

### Data Processing
- **Automated data cleaning**: Filters to Gulf Coast counties and relevant vulnerability columns
- **Feature engineering**: Creates Hurricane Risk Index, Evacuation Challenge Score, Medical Vulnerability Score
- **Flag analysis**: Binary indicators for top 10% vulnerability in key areas

### Visualizations
- **Vulnerability histograms**: Distribution of social vulnerability themes
- **State comparisons**: Average vulnerability scores by Gulf Coast state
- **Top counties analysis**: Counties with highest hurricane risk
- **Correlation heatmaps**: Relationships between vulnerability factors
- **Geographic maps**: Real choropleth maps with US county boundaries (when GeoPandas is installed) or simplified scatter-plot maps

### Analysis & Insights
- **Hurricane risk profiling**: Comprehensive risk categorization
- **Evacuation barrier analysis**: Transportation and housing vulnerabilities
- **Medical vulnerability assessment**: Health-related risk factors
- **Executive summaries**: Automated report generation
- **Storytelling insights**: Key statistics for presentations

## 📈 Core Metrics

### Hurricane Risk Index
Average of **RPL_THEME2** (Household Characteristics) + **RPL_THEME4** (Housing/Transportation)
- Measures intersection of fragile households and evacuation barriers

### Evacuation Challenge Score
Weighted combination of:
- **F_NOVEH** (60%): No vehicle access
- **F_MOBILE** (30%): Mobile homes
- **F_CROWD** (10%): Crowded housing

### Medical Vulnerability Score
Sum of health-related flags:
- **F_AGE65**: Elderly population (65+)
- **F_DISABL**: Disabled individuals
- **F_UNINSUR**: No health insurance

## 📋 Requirements

### Python Dependencies
```bash
pip install requirements.txt
```

### Data Requirements
- `data/SVI_2022_US_county.csv` (included in project)
- CDC Social Vulnerability Index 2022 dataset
