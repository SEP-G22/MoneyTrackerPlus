import os
import matplotlib.pyplot as plt
from collections import defaultdict
from models import *
from matplotlib import font_manager

# Set the font to a Chinese font
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # Use Microsoft YaHei font for Chinese characters
plt.rcParams['axes.unicode_minus'] = False  # Ensure minus sign is displayed correctly

def generate_pie_chart(transactions):
    income_totals = defaultdict(float)
    expense_totals = defaultdict(float)

    for transaction in transactions:
        if transaction.category.type == 'Income':
            income_totals[transaction.category.category] += transaction.amount
        elif transaction.category.type == 'Expense':
            expense_totals[transaction.category.category] += transaction.amount

    total_income = sum(income_totals.values())
    total_expense = sum(expense_totals.values())
    balance = total_income - total_expense

    # Data for the first pie chart (income vs expense)
    first_labels = ['收入', '支出']
    first_sizes = [total_income, total_expense]

    # Data for the second pie chart (expense categories)
    second_labels = expense_totals.keys()
    second_sizes = expense_totals.values()

    # Data for the third pie chart (income categories)
    third_labels = income_totals.keys()
    third_sizes = income_totals.values()

    fig, axs = plt.subplots(1, 3, figsize=(12, 4))

    # Plot first pie chart (income vs expense)
    wedges, texts, autotexts = axs[0].pie(first_sizes, labels=first_labels, autopct='%1.1f%%', startangle=90, colors=['#66b3ff','#ff9999'], wedgeprops=dict(width=0.3, edgecolor='w'))
    axs[0].set_title('收入與支出')
    axs[0].text(0, 0, f'結餘: \n{balance:.2f}', ha='center', va='center', fontsize=12, fontweight='bold')

    # Plot second pie chart (expense categories)
    wedges, texts, autotexts = axs[1].pie(second_sizes, labels=second_labels, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors, wedgeprops=dict(width=0.3, edgecolor='w'))
    axs[1].set_title('支出分類')
    axs[1].text(0, 0, f'總支出: \n{total_expense:.2f}', ha='center', va='center', fontsize=12, fontweight='bold')

    # Plot third pie chart (income categories)
    wedges, texts, autotexts = axs[2].pie(third_sizes, labels=third_labels, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors, wedgeprops=dict(width=0.3, edgecolor='w'))
    axs[2].set_title('收入分類')
    axs[2].text(0, 0, f'總收入: \n{total_income:.2f}', ha='center', va='center', fontsize=12, fontweight='bold')

    plt.subplots_adjust(left=0.1, right=0.9, top=0.95, bottom=0.05, wspace=0.4)

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
