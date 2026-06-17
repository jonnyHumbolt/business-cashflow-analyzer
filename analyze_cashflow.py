import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def load_data(filepath):
    return pd.read_csv(filepath)

def calculate_metrics(df):
    income = df[df['type'] == 'Income']['amount'].sum()
    expenses = df[df['type'] == 'Expense']['amount'].sum()
    net_cash_flow = income - expenses
    return income, expenses, net_cash_flow

def identify_high_expenses(df, threshold=1000):
    expenses_df = df[df['type'] == 'Expense']
    grouped = expenses_df.groupby('category')['amount'].sum()
    high_expenses = grouped[grouped > threshold]
    return high_expenses.to_dict()

def generate_expenses_chart(df, output_filepath):
    expenses_df = df[df['type'] == 'Expense']
    category_expenses = expenses_df.groupby('category')['amount'].sum().reset_index()
    category_expenses = category_expenses.sort_values(by='amount', ascending=False)

    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    fig, ax = plt.subplots(figsize=(8, 5))

    colors = ['#1e3a8a', '#3b82f6', '#60a5fa', '#93c5fd', '#bfdbfe']
    if len(category_expenses) > len(colors):
        colors = colors * (len(category_expenses) // len(colors) + 1)
    colors = colors[:len(category_expenses)]

    bars = ax.bar(category_expenses['category'], category_expenses['amount'], color=colors, edgecolor='none', width=0.6)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#cbd5e1')

    ax.tick_params(bottom=False, left=False)
    ax.yaxis.grid(True, linestyle='--', alpha=0.5, color='#cbd5e1')
    ax.xaxis.grid(False)

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"${height:,.2f}",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, fontweight='bold', color='#1e293b')

    ax.set_title("Expenses by Category", fontsize=16, fontweight='bold', pad=20, color='#0f172a')
    ax.set_ylabel("Total Amount ($)", fontsize=12, fontweight='semibold', labelpad=10, color='#334155')
    ax.set_xlabel("Category", fontsize=12, fontweight='semibold', labelpad=10, color='#334155')

    plt.xticks(fontsize=11, color='#475569')
    plt.yticks(fontsize=11, color='#475569')

    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('$%1.0f'))

    plt.tight_layout()
    plt.savefig(output_filepath, dpi=300, bbox_inches='tight')
    plt.close(fig)

def generate_report(income, expenses, net_cash_flow, high_expenses, output_filepath):
    with open(output_filepath, 'w') as f:
        f.write("# Financial Summary\n\n")
        f.write("## Key Metrics\n")
        f.write(f"- **Total Income:** ${income:,.2f}\n")
        f.write(f"- **Total Expenses:** ${expenses:,.2f}\n")
        f.write(f"- **Net Cash Flow:** ${net_cash_flow:,.2f}\n\n")

        f.write("## High-Expense Categories (>$1,000)\n")
        if high_expenses:
            for category, amount in high_expenses.items():
                f.write(f"- **{category}:** ${amount:,.2f}\n")
        else:
            f.write("- None\n")
        
        f.write("\n## Expense Breakdown by Category\n")
        f.write("![Expenses Chart](expenses_chart.png)\n")

def main():
    df = load_data('business_transactions.csv')
    income, expenses, net_cash_flow = calculate_metrics(df)
    high_expenses = identify_high_expenses(df)
    generate_expenses_chart(df, 'expenses_chart.png')
    generate_report(income, expenses, net_cash_flow, high_expenses, 'financial_summary.md')

if __name__ == '__main__':
    main()
