import csv
from django.shortcuts import render
import os

def index(request):
    items = []
    csv_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'allen_street_db.csv')
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        headers = reader.fieldnames  # Extract the headers (column names)

        if request.method == 'POST':
            column1 = request.POST.get('column1')
            condition1 = request.POST.get('condition1')
            value1 = request.POST.get('value1')
            column2 = request.POST.get('column2')
            condition2 = request.POST.get('condition2')
            value2 = request.POST.get('value2')

            # Filter the rows based on the conditions
            for row in reader:
                if evaluate_condition(row[column1], condition1, value1) and evaluate_condition(row[column2], condition2, value2):
                    items.append(row)
        else:
            # If not a POST request, display all rows
            items = list(reader)

    return render(request, 'index.html', {'headers': headers, 'items': items})

def evaluate_condition(field_value, condition, value):
    if condition == '=':
        return field_value == value
    elif condition == '!=':
        return field_value != value
    elif condition == '>':
        return field_value > value
    elif condition == '<':
        return field_value < value
    elif condition == 'LIKE':
        return value in field_value
    return False