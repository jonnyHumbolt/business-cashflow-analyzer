import pytest
import pandas as pd
import os
from analyze_cashflow import calculate_metrics, identify_high_expenses, generate_expenses_chart

@pytest.fixture
def sample_data():
    data = {
        'date': ['2026-06-01', '2026-06-03', '2026-06-05', '2026-06-10', '2026-06-12', '2026-06-14', '2026-06-15', '2026-06-16'],
        'description': ['Client Retainer A', 'Cloud Server Hosting', 'Client Project B', 'Office Rent', 'Co-Working Pass', 'Facebook Ads Run', 'Email Marketing Platform', 'Graphic Designer Contract'],
        'category': ['Revenue', 'Software', 'Revenue', 'Facilities', 'Facilities', 'Marketing', 'Software', 'Marketing'],
        'amount': [3500.00, 120.00, 2200.00, 1200.00, 150.00, 850.00, 45.00, 400.00],
        'type': ['Income', 'Expense', 'Income', 'Expense', 'Expense', 'Expense', 'Expense', 'Expense']
    }
    return pd.DataFrame(data)

def test_calculate_metrics(sample_data):
    income, expenses, net_cash_flow = calculate_metrics(sample_data)
    assert income == 5700.00
    assert expenses == 2765.00
    assert net_cash_flow == 2935.00

def test_identify_high_expenses(sample_data):
    high_expenses = identify_high_expenses(sample_data)
    assert 'Facilities' in high_expenses
    assert high_expenses['Facilities'] == 1350.00
    assert 'Marketing' in high_expenses
    assert high_expenses['Marketing'] == 1250.00
    assert 'Software' not in high_expenses

def test_identify_high_expenses_custom_threshold(sample_data):
    high_expenses = identify_high_expenses(sample_data, threshold=1300)
    assert 'Facilities' in high_expenses
    assert high_expenses['Facilities'] == 1350.00
    assert 'Marketing' not in high_expenses

def test_generate_expenses_chart(sample_data, tmp_path):
    chart_file = tmp_path / "test_chart.png"
    generate_expenses_chart(sample_data, str(chart_file))
    assert chart_file.exists()

