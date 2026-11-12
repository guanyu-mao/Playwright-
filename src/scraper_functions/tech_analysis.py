import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import numpy as np
import io
import base64

# Read the updated table
updated_file = r"C:\updated_azure_table\Combined Resource Groups for Prod & Pre-Prod.csv"
df = pd.read_csv(updated_file)

def monthly_tech_summary(df):
    df['Cost'] = pd.to_numeric(df['Cost'], errors='coerce')
    df['UsageDate'] = pd.to_datetime(df['UsageDate'])
    df['Month'] = df['UsageDate'].dt.to_period('M').astype(str)
    summary = df.groupby(['Month', 'ServiceName'])['Cost'].sum().reset_index()
    pivot = summary.pivot(index='Month', columns='ServiceName', values='Cost').fillna(0)
    pivot['Total'] = pivot.select_dtypes(include='number').sum(axis=1)
    return pivot

def plot_stacked_bar(pivot):
    fig, ax = plt.subplots(figsize=(12,6))
    pivot_no_total = pivot.drop(columns=['Total'])
    pivot_no_total = pivot_no_total.apply(pd.to_numeric, errors='coerce')
    pivot_no_total.plot(kind='bar', stacked=True, ax=ax)
    ax.set_ylabel('Monthly Cost')
    ax.set_title('Monthly Technology Consumption (Stacked, Monthly)')
    ax.legend(title='Technology', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    return fig

def linear_regression_per_tech(df):
    df['UsageDate'] = pd.to_datetime(df['UsageDate'])
    df['MonthNum'] = df['UsageDate'].dt.year * 12 + df['UsageDate'].dt.month
    tech_models = {}
    future_months = np.arange(df['MonthNum'].max() + 1, df['MonthNum'].max() + 13)
    future_dates = pd.date_range(df['UsageDate'].max(), periods=13, freq='MS')[1:]
    predictions = []

    for tech in df['ServiceName'].unique():
        tech_df = df[df['ServiceName'] == tech].groupby('MonthNum')['Cost'].sum().reset_index()
        if tech_df.empty or tech_df['Cost'].dropna().empty:
            continue
        X = tech_df[['MonthNum']]
        y = tech_df['Cost']
        model = LinearRegression().fit(X, y)
        y_pred = model.predict(X)
        r2 = r2_score(y, y_pred) if len(y) > 1 else float('nan')
        future_pred = model.predict(future_months.reshape(-1, 1))
        predictions.append((tech, future_dates, future_pred, model.coef_[0], model.intercept_, r2))
        tech_models[tech] = (model, r2, model.coef_[0], model.intercept_)
    return predictions, tech_models

def plot_clustered_regression(df, predictions):
    fig, ax = plt.subplots(figsize=(16,8))
    df['UsageDate'] = pd.to_datetime(df['UsageDate'])
    df['Month'] = df['UsageDate'].dt.to_period('M').astype(str)
    techs = [p[0] for p in predictions]
    actual = df.groupby(['Month', 'ServiceName'])['Cost'].sum().reset_index()
    pivot_actual = actual.pivot(index='Month', columns='ServiceName', values='Cost').fillna(0)
    pivot_actual = pivot_actual[techs]
    pivot_actual.plot(kind='bar', width=0.8, alpha=0.7, ax=ax)
    ax.set_ylabel('Monthly Cost')
    ax.set_xlabel('Month')
    ax.set_title('Technology Cost Trends (Clustered Bar Chart)')
    ax.legend(title='Technology', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    return fig

def regression_formulas_table(predictions):
    formulas = []
    for tech, _, _, coef, intercept, r2 in predictions:
        formulas.append({
            "Technology": tech,
            "Formula": f"Cost = {coef:.2f}*MonthNum + {intercept:.2f}",
            "R2 Accuracy": f"{r2:.2f}"
        })
    return pd.DataFrame(formulas)

if __name__ == "__main__":
    pivot = monthly_tech_summary(df)
    predictions, tech_models = linear_regression_per_tech(df)

    # Create PDF
    pdf_path = r"C:\updated_azure_table\tech_analysis_report.pdf"
    with PdfPages(pdf_path) as pdf:
        # --- Title Page ---
        fig_title, ax_title = plt.subplots(figsize=(10, 3))
        ax_title.axis('off')
        ax_title.text(
            0.0, 0.7, "Azure Costing Analysis", fontsize=28, fontweight='bold', ha='left', va='center'
        )
        ax_title.text(
            0.0, 0.4, "Updated Month: 2025/08", fontsize=18, ha='left', va='center'
        )
        pdf.savefig(fig_title)
        plt.close(fig_title)

        # Stacked bar chart
        fig1 = plot_stacked_bar(pivot)
        pdf.savefig(fig1)
        plt.close(fig1)

        # Clustered regression chart
        fig2 = plot_clustered_regression(df, predictions)
        pdf.savefig(fig2)
        plt.close(fig2)

        # Regression formulas table as a figure
        formulas_df = regression_formulas_table(predictions)
        fig3, ax3 = plt.subplots(figsize=(8, 1 + 0.5*len(formulas_df)))
        ax3.axis('off')
        tbl = ax3.table(cellText=formulas_df.values, colLabels=formulas_df.columns, loc='center')
        tbl.auto_set_font_size(False)
        tbl.set_fontsize(10)
        tbl.scale(1.5, 1.5)  # Increase width scaling for better column fit

        # Adjust column widths based on content
        for i, key in enumerate(formulas_df.columns):
            max_len = max([len(str(x)) for x in formulas_df[key]] + [len(key)])
            tbl.auto_set_column_width([i])
            for j in range(len(formulas_df)):
                tbl[(j+1, i)].set_width(0.15 + 0.02 * max_len)  # Adjust width formula as needed

        pdf.savefig(fig3)
        plt.close(fig3)

        # Ensure the pivot index (Month) is sorted chronologically
        pivot_sorted = pivot.copy()
        pivot_sorted.index = pd.to_datetime(pivot_sorted.index, format="%Y-%m")
        pivot_sorted = pivot_sorted.sort_index()
        pivot_sorted.index = pivot_sorted.index.strftime("%Y-%m")  # Convert back to string for display

        # Dynamically set figure width based on number of columns (wider for more columns)
        fig_width = max(8, 0.7 * len(pivot_sorted.columns))  # Tighter width per column
        fig_height = max(2, 0.35 * len(pivot_sorted))        # Tighter height per row
        fig4, ax4 = plt.subplots(figsize=(fig_width, fig_height))
        ax4.axis('off')
        ax4.set_position([0, 0, 1, 1])  # Fill the figure with the table

        # Create the table, centered
        tbl2 = ax4.table(
            cellText=pivot_sorted.round(2).values,
            colLabels=pivot_sorted.columns,
            rowLabels=pivot_sorted.index,
            loc='center'
        )
        tbl2.auto_set_font_size(False)
        tbl2.set_fontsize(8)  # Slightly larger font for readability
        tbl2.scale(1.2, 1.2)  # Less scaling for a tighter fit

        # Adjust column widths based on content length
        for i, key in enumerate(pivot_sorted.columns):
            max_len = max([len(str(x)) for x in pivot_sorted[key]] + [len(key)])
            width = 0.13 + 0.03 * max_len  # Wider base width and scaling
            tbl2.auto_set_column_width([i])
            for j in range(len(pivot_sorted)):
                tbl2[(j+1, i)].set_width(width)
                tbl2[(j+1, i)].set_text_props(ha='center', va='center')  # Center-align text

        # Center-align the row labels (months)
        for j in range(len(pivot_sorted)):
            tbl2[(j+1, -1)].set_text_props(ha='center', va='center')

        pdf.savefig(fig4)
        plt.close(fig4)

    print(f"PDF report saved to: {pdf_path}")

    # HTML Report Generation

   # When converting to base64 for HTML, use tight bounding box and small padding:
    def fig_to_base64(fig):
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1)
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)
        return f"data:image/png;base64,{img_base64}"

    stacked_bar_img = fig_to_base64(plot_stacked_bar(pivot))
    clustered_regression_img = fig_to_base64(plot_clustered_regression(df, predictions))
    formulas_img = fig_to_base64(fig3)  # fig3 is your regression formulas table
    pivot_img = fig_to_base64(fig4)     # fig4 is your pivot table

    from jinja2 import Environment, FileSystemLoader

    env = Environment(loader=FileSystemLoader('src/scraper_functions'))
    template = env.get_template('az_report.html')

    html_out = template.render(
        updated_month="2025/09",
        stacked_bar_img=stacked_bar_img,
        clustered_regression_img=clustered_regression_img,
        formulas_img=formulas_img,
        pivot_img=pivot_img
    )

    # Save HTML to the same directory as the PDF
    html_path = os.path.join(os.path.dirname(pdf_path), "az_report_rendered.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_out)
    print(f"HTML report saved to: {html_path}")