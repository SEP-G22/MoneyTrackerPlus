import os

import matplotlib.pyplot as plt
from collections import defaultdict
from models import *


def generate_pie_chart(transactions):
    category_totals = defaultdict(float)
    for transaction in transactions:
        category_totals[transaction.category] += transaction.amount

    labels = category_totals.keys()
    sizes = category_totals.values()

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.title('Transaction Categories Pie Chart')

    # Save the plot to a file
    image_path = os.path.join('images', 'pie_chart.png')
    plt.savefig(image_path)
    plt.close(fig)

    return image_path


def generate_line_chart(transactions):
    income_totals = defaultdict(float)
    expense_totals = defaultdict(float)

    for transaction in transactions:
        if transaction.type == 'income':
            income_totals[transaction.date] += transaction.amount
        elif transaction.type == 'expense':
            expense_totals[transaction.date] += transaction.amount

    dates = sorted(set(income_totals.keys()).union(expense_totals.keys()))
    income_values = [income_totals[date] for date in dates]
    expense_values = [expense_totals[date] for date in dates]

    fig, ax = plt.subplots()
    ax.plot(dates, income_values, label='Income')
    ax.plot(dates, expense_values, label='Expense')

    ax.set_xlabel('Date')
    ax.set_ylabel('Amount')
    ax.set_title('Income and Expense Over Time')
    ax.legend()

    plt.show()
