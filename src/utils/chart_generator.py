import os
from datetime import datetime, timedelta
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np

from models import *

# Set the font to a Chinese font
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # Use Microsoft YaHei font for Chinese characters
plt.rcParams['axes.unicode_minus'] = False  # Ensure minus sign is displayed correctly


def generate_empty_image(image_path):
    fig, ax = plt.subplots()
    ax.text(0.5, 0.5, 'No Data Available', ha='center', va='center', fontsize=12, color='gray')
    ax.axis('off')
    plt.savefig(image_path)
    plt.close(fig)


def generate_pie_chart(transactions):
    if not transactions:
        image_path = os.path.join('images', 'pie_chart.png')
        generate_empty_image(image_path)
        return image_path

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
    if not transactions:
        image_path = os.path.join('images', 'line_chart.png')
        generate_empty_image(image_path)
        return image_path
    # Initialize dictionaries to store income and expense totals by week
    weekly_income = defaultdict(float)
    weekly_expense = defaultdict(float)

    # Process each transaction
    for transaction in transactions:
        week_start = transaction.date - timedelta(days=transaction.date.weekday())
        if transaction.category.type == 'Income':
            weekly_income[week_start] += transaction.amount
        elif transaction.category.type == 'Expense':
            weekly_expense[week_start] += transaction.amount

    # Sort the weeks
    sorted_weeks = sorted(weekly_income.keys() | weekly_expense.keys())

    # Prepare data for plotting
    dates = [week.strftime('%Y-%m-%d') for week in sorted_weeks]
    income_values = [weekly_income[week] for week in sorted_weeks]
    expense_values = [weekly_expense[week] for week in sorted_weeks]
    balance_values = [income - expense for income, expense in zip(income_values, expense_values)]

    # Convert date strings to datetime objects
    dates = [datetime.strptime(date, '%Y-%m-%d') for date in dates]

    # Plot the line chart
    plt.figure(figsize=(10, 5))
    plt.plot(dates, income_values, label='收入', marker='o')
    plt.plot(dates, expense_values, label='支出', marker='o')
    plt.plot(dates, balance_values, label='結餘', marker='o')
    plt.xlabel('日期 (每周)')
    plt.ylabel('金額 (元)')
    plt.title('每周總收支情形')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)

    # Save the plot to a file
    image_path = os.path.join('images', 'line_chart.png')
    plt.tight_layout()
    plt.savefig(image_path)
    plt.close()

    return image_path


def generate_bar_chart(transactions):
    if not transactions:
        image_path = os.path.join('images', 'bar_chart.png')
        generate_empty_image(image_path)
        return image_path

    income_totals = defaultdict(float)
    expense_totals = defaultdict(float)

    for transaction in transactions:
        if transaction.category.type == 'Income':
            income_totals[transaction.category.category] += transaction.amount
        elif transaction.category.type == 'Expense':
            expense_totals[transaction.category.category] += transaction.amount

    total_income = sum(income_totals.values())
    total_expense = sum(expense_totals.values())

    income_categories = list(income_totals.keys())
    expense_categories = list(expense_totals.keys())
    income_values = [income_totals[category] for category in income_categories]
    expense_values = [expense_totals[category] for category in expense_categories]

    fig, ax = plt.subplots(figsize=(12, 2))  # Adjusted figsize to reduce the height

    # Plot income bar
    bottom = 0
    income_colors = plt.cm.Blues(np.linspace(0.3, 0.7, len(income_categories)))
    for value, category, color in zip(income_values, income_categories, income_colors):
        ax.barh('Income', value, left=bottom, label=f'{category} ({value/total_income:.1%})', color=color, height=0.4)
        bottom += value

    # Plot expense bar
    bottom = 0
    expense_colors = plt.cm.Reds(np.linspace(0.3, 0.7, len(expense_categories)))
    for value, category, color in zip(expense_values, expense_categories, expense_colors):
        ax.barh('Expense', value, left=bottom, label=f'{category} ({value/total_expense:.1%})', color=color, height=0.4)
        bottom += value

    # Add labels, title, and legend
    ax.set_xlabel('Amount')
    ax.set_title('支出與收入分析')
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=3)  # Adjusted legend position

    # Beautify the plot
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#DDDDDD')
    ax.xaxis.set_tick_params(width=0)
    ax.yaxis.set_tick_params(width=0)
    ax.xaxis.grid(True, color='#EEEEEE')
    ax.yaxis.grid(False)

    plt.tight_layout()

    # Save the plot to a file
    image_path = os.path.join('images', 'bar_chart.png')
    plt.savefig(image_path)
    plt.close(fig)

    return image_path
