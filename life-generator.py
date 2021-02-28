# Tate Jenkins
# CS 361
# 2/14/2021

import csv
import tkinter as tk
import sys


input_file = None
if sys.argv[0] != sys.argv[-1]:
    input_file = sys.argv[-1]


def get_results(entries, results_listbox, cat_name, x):

    if cat_name is None:
        cat_name = listbox.get(listbox.curselection())
    
    if x is None:
        x = x_var.get()

    selected_cat = {}
    for key, val in entries.items():
        if val['cat'] == cat_name:
            selected_cat[key] = val
    
    selected_cat = dict(sorted(selected_cat.items(), key=lambda item: item[0]))
    selected_cat = dict(sorted(selected_cat.items(), key=lambda item: item[1]['number_of_reviews'], reverse=True))
    selected_cat = {k: selected_cat[k] for k in list(selected_cat)[:x*10]}
    selected_cat = dict(sorted(selected_cat.items(), key=lambda item: item[0]))
    selected_cat = dict(sorted(selected_cat.items(), key=lambda item: item[1]['average_review_rating'], reverse=True))
    selected_cat = {k: selected_cat[k] for k in list(selected_cat)[:x]}

    all_results = []

    if results_listbox is not None:
        for key, val in selected_cat.items():
            results_listbox.insert(0, val['product_name'])

    for key, val in selected_cat.items():
        results = {}
        results['input_item_type'] = 'toys'
        results['input_item_category'] = cat_name
        results['input_number_to_generate'] = x
        results['output_item_name'] = val['product_name']
        results['output_item_rating'] = val['average_review_rating']
        results['output_item_num_reviews'] = val['number_of_reviews']
        all_results.append(results)

    with open('life_output.csv', mode='w+', encoding='utf8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['input_item_type','input_item_category','input_number_to_generate','output_item_name','output_item_rating','output_item_num_reviews'])
        for result in all_results:
            writer.writerow(result.values())



entries = {}
cats = {}
filename = 'amazon_co-ecommerce_sample.csv'

with open(filename, mode='r', encoding='utf8') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        if '>' in row['amazon_category_and_sub_category']:
            cat = row['amazon_category_and_sub_category'].split(' > ')[0]
            row['cat'] = cat 
            if row['cat'] not in cats:
                cats[row['cat']] = 0
            entry = row
            entry['cat'] = row['cat']
            entry['number_of_reviews'] = int(row['number_of_reviews'].replace(',','')) if row['number_of_reviews'] != '' else 0
            entry['average_review_rating'] = float(row['average_review_rating'].split(' ')[0]) if row['average_review_rating'] != '' else 0
            entries[row['uniq_id']] = entry

if input_file:
    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == 'toys':
                category = row[1]
                number = int(row[2])


window = tk.Tk()
window.geometry("400x500")
selected_cat_var = tk.StringVar()
x_var = tk.IntVar()

listbox = tk.Listbox(window)
for key, val in cats.items():
    listbox.insert(0, key)
listbox.pack(padx=10, pady=10,fill=tk.BOTH, expand=True)

num_items_label = tk.Label(window, text="Number of toys to output")
num_items_label.pack()
num_items_entry = tk.Entry(window, textvariable=x_var)
num_items_entry.pack()

if not input_file:
    button = tk.Button(window, text="Submit", command=lambda: get_results(entries, results_listbox, None, None))
    button.pack()

label = tk.Label(window, text="Results")
label.pack()
results_listbox = tk.Listbox(window)
results_listbox.pack(padx=10, pady=10,fill=tk.BOTH, expand=True)
if input_file:
    get_results(entries, results_listbox, category, number)
window.mainloop()