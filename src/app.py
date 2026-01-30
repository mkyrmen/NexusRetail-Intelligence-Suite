import sys
import os

# 1. TELL PYTHON WHERE YOUR LIBRARIES ARE
# This must be at the absolute top
sys.path.append('Z:/Python')

import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

# Import your database manager from the same folder
try:
    from db_manager import get_dashboard_data
except ImportError:
    from src.db_manager import get_dashboard_data

# 2. Initialize App with a high-end theme (CYBORG = Dark Mode)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# 3. App Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Executive Sales Warehouse Intelligence", 
                        className="text-center text-primary mt-4 mb-4"), width=12)
    ]),
    
    # KPI Row
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Total Revenue", className="card-title text-muted"),
                html.H2(id="kpi-revenue", className="text-info")
            ])
        ], color="dark", outline=True), width=4),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Profit Margin", className="card-title text-muted"),
                html.H2(id="kpi-margin", className="text-success")
            ])
        ], color="dark", outline=True), width=4),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Order Count", className="card-title text-muted"),
                html.H2(id="kpi-orders", className="text-warning")
            ])
        ], color="dark", outline=True), width=4),
    ], className="mb-4"),

    # Filters & Main Visuals
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Label("Select Market Segment:", className="text-info mb-2"),
                    dcc.Dropdown(
                        id='segment-dropdown',
                        options=[], 
                        placeholder="Loading Segments...",
                        className="mb-3",
                        style={'color': '#000'} # Ensures text is visible in dropdown
                    ),
                    dcc.Graph(id='main-trend-chart')
                ])
            ], color="dark")
        ], width=8),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='category-breakdown-chart')
                ])
            ], color="dark")
        ], width=4)
    ])
], fluid=True)

# 4. Callbacks
@app.callback(
    [Output('segment-dropdown', 'options'),
     Output('segment-dropdown', 'value'),
     Output('kpi-revenue', 'children'),
     Output('kpi-margin', 'children'),
     Output('kpi-orders', 'children'),
     Output('main-trend-chart', 'figure'),
     Output('category-breakdown-chart', 'figure')],
    [Input('segment-dropdown', 'value')]
)
def refresh_data(selected_segment):
    # Pull fresh data from the SQLite warehouse
    df = get_dashboard_data()
    
    # Handle data if Region column exists (replacing Segment if necessary)
    group_col = 'Region' if 'Region' in df.columns else 'Segment'
    
    # Populate dropdown options
    unique_groups = df[group_col].unique()
    options = [{'label': s, 'value': s} for s in unique_groups]
    
    if not selected_segment:
        selected_segment = unique_groups[0]
        
    filtered_df = df[df[group_col] == selected_segment]
    
    # Compute Metrics
    total_sales = filtered_df['Sales'].sum()
    total_profit = filtered_df['Profit'].sum()
    margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0
    
    # Visual 1: Area Chart for Sales Trend
    trend = filtered_df.groupby(filtered_df['Order_Date'].dt.to_period('M')).sum(numeric_only=True).reset_index()
    trend['Order_Date'] = trend['Order_Date'].astype(str)
    fig_trend = px.area(trend, x='Order_Date', y='Sales', 
                        title=f"Revenue Velocity: {selected_segment}",
                        template="plotly_dark",
                        color_discrete_sequence=['#00bc8c'])
    
    # Visual 2: Bar Chart for Category Profit
    cat_data = filtered_df.groupby('Category').sum(numeric_only=True).reset_index()
    fig_cat = px.bar(cat_data, x='Category', y='Profit', 
                     color='Category', 
                     title="Profitability by Category",
                     template="plotly_dark")
    
    return options, selected_segment, f"${total_sales:,.0f}", f"{margin:.1f}%", f"{len(filtered_df):,}", fig_trend, fig_cat

if __name__ == '__main__':
    app.run(debug=True)