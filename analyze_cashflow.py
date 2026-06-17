import pandas as pd

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

def main():
    df = load_data('business_transactions.csv')
    income, expenses, net_cash_flow = calculate_metrics(df)
    high_expenses = identify_high_expenses(df)
    generate_report(income, expenses, net_cash_flow, high_expenses, 'financial_summary.md')

if __name__ == '__main__':
    main()
