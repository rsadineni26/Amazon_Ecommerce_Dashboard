import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

# Load cleaned data
df = pd.read_csv("Cleaned_Ecommerce_Purchases.csv")

# === Prepare Insights ===
avg_purchase_price = df['Purchase Price'].mean()
top_language = df['Language'].value_counts().idxmax()

# === Charts ===

# 1. Top 5 Companies by Avg Purchase Price
top_companies = df.groupby('Company')['Purchase Price'].mean().sort_values(ascending=False).head(5)
fig_companies = px.bar(
    x=top_companies.index,
    y=top_companies.values,
    labels={'x': 'Company', 'y': 'Avg Purchase Price'},
    title='Top 5 Companies by Avg Purchase Price'
)

# 2. AM vs PM Pie Chart
fig_ampm = px.pie(
    df, names='AM or PM', title='AM vs PM Purchases'
)

# 3. Top 5 Credit Card Providers by Total Purchase
top_cc = df.groupby('CC Provider')['Purchase Price'].sum().sort_values(ascending=False).head(5)
fig_cc = px.bar(
    x=top_cc.index,
    y=top_cc.values,
    labels={'x': 'Credit Card Provider', 'y': 'Total Purchase Value'},
    title='Top 5 Credit Card Providers by Purchase Value'
)

# 4. Language Distribution as Column Chart
lang_counts = df['Language'].value_counts().sort_values(ascending=False)
fig_lang = px.bar(
    x=lang_counts.index,
    y=lang_counts.values,
    labels={'x': 'Language', 'y': 'Count'},
    title='Language Distribution'
)

# 5. Top 10 Job Titles as Line Chart
top_jobs = df['Job'].value_counts().head(10)
fig_jobs = px.line(
    x=top_jobs.index,
    y=top_jobs.values,
    markers=True,
    labels={'x': 'Job Title', 'y': 'Count'},
    title='Top 10 Job Titles'
)

# === Build Dash App ===
app = Dash(__name__)
app.title = "Ecommerce Insights Dashboard"

# === Layout with CSS ===
app.layout = html.Div(children=[
    html.H1("Ecommerce Dashboard", style={
        'textAlign': 'center',
        'color': '#333',
        'backgroundColor': '#f8f8f8',
        'padding': '20px',
        'borderBottom': '2px solid #ccc'
    }),

    html.Div([
        html.Div([
            html.H3("Average Purchase Price", style={'marginBottom': '5px'}),
            html.P(f"${avg_purchase_price:.2f}", style={'fontSize': '20px', 'color': '#007BFF'})
        ], className='card'),

        html.Div([
            html.H3("Most Common Language", style={'marginBottom': '5px'}),
            html.P(top_language, style={'fontSize': '20px', 'color': '#28A745'})
        ], className='card'),
    ], style={
        'display': 'flex',
        'justifyContent': 'space-around',
        'marginBottom': '30px'
    }),

    dcc.Graph(figure=fig_companies),
    dcc.Graph(figure=fig_ampm),
    dcc.Graph(figure=fig_cc),
    dcc.Graph(figure=fig_lang),
    dcc.Graph(figure=fig_jobs),
], style={
    'fontFamily': 'Arial, sans-serif',
    'padding': '0 20px'
})

# === Add custom CSS for cards ===
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            .card {
                background-color: #f0f0f0;
                padding: 20px;
                border-radius: 8px;
                width: 40%;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                text-align: center;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# === Run Server ===
if __name__ == "__main__":
    app.run(debug=True)
