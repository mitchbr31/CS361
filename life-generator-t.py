# Tate Jenkins
# CS 361
# 2/14/2021

import csv
import tkinter as tk
import sys
import pika
import threading
import json
import time

def get_selected_cats(cat_name, entries):
    # returns category name from gui and dict of entries in that category

    selected_cat = {}
    for key, val in entries.items():
        if val['cat'] == cat_name:
            selected_cat[key] = val

    return cat_name, selected_cat

def get_top_items(selected_cat, num_items):
    # returns top reviewed items

    # get the top reviewed items
    selected_cat = dict(sorted(selected_cat.items(), key=lambda item: item[0]))
    selected_cat = dict(sorted(selected_cat.items(), \
         key=lambda item: item[1]['number_of_reviews'], reverse=True))
    selected_cat = {k: selected_cat[k] for k in list(selected_cat)[:num_items*10]}
    selected_cat = dict(sorted(selected_cat.items(), \
         key=lambda item: item[0]))
    selected_cat = dict(sorted(selected_cat.items(), \
         key=lambda item: item[1]['average_review_rating'], reverse=True))
    selected_cat = {k: selected_cat[k] for k in list(selected_cat)[:num_items]}

    return selected_cat

def get_input_params(input_params):
    (cat_name, num_items) = input_params      
    if num_items is None:
        num_items = x_var.get()    
    if cat_name is None:
        cat_name = listbox.get(listbox.curselection())
    input_params = (cat_name, num_items)
    return input_params

def generate_results(top_items, input_params):
    # generate output csv   
    (cat_name, num_items) = input_params   
    all_results = []

    for key, val in top_items.items():
        results = {}
        results['input_item_type'] = 'toys'
        results['input_item_category'] = cat_name
        results['input_number_to_generate'] = num_items
        results['output_item_name'] = val['product_name']
        results['output_item_rating'] = val['average_review_rating']
        results['output_item_num_reviews'] = val['number_of_reviews']
        all_results.append(results)  

    return all_results  

def populate_results(top_items, results_listbox):
    # put the results in the gui 

    if results_listbox is not None:
        for key, val in top_items.items():
            results_listbox.insert(0, val['product_name'])

def write_output(all_results):

    with open('output.csv', mode='w+', encoding='utf8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['input_item_type','input_item_category', 
        'input_number_to_generate','output_item_name','output_item_rating','output_item_num_reviews'])
        for result in all_results:
            writer.writerow(result.values())

def get_results(entries, results_listbox, input_params, channel):
    # write and publish output items data based on the tkinter or command line input

    input_params = (cat_name, num_items) = get_input_params(input_params)

    # generate dictionary with only the selected category
    cat_name, selected_cat = get_selected_cats(cat_name, entries)
    
    # get the top reviewed items
    top_items = get_top_items(selected_cat, num_items)
   
    all_results = generate_results(top_items, input_params)

    # populate the results listbox
    populate_results(top_items, results_listbox)

    write_output(all_results)

    # publish output as json
    channel.basic_publish(exchange='', routing_key='hello', body=json.dumps(all_results), \
         properties=pika.BasicProperties(delivery_mode=2,
    ))
    channel.close()


class PikaMessenger():

    exchange_name = 'exchange'

    def __init__(self, *args, **kwargs):
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.conn.channel()
        self.channel.exchange_declare(
            exchange=self.exchange_name, 
            exchange_type='topic')

    def consume(self, keys, callback):
        result = self.channel.queue_declare('', exclusive=True)
        queue_name = result.method.queue
        for key in keys:
            self.channel.queue_bind(
                exchange=self.exchange_name, 
                queue=queue_name, 
                routing_key=key)

        self.channel.basic_consume(
            queue=queue_name, 
            on_message_callback=callback, 
            auto_ack=True)

        self.channel.start_consuming()
    
    def stop_consume(self, keys):
        result = self.channel.queue_declare('', exclusive=True)
        queue_name = result.method.queue
        for key in keys:
            self.channel.queue_bind(
                exchange=self.exchange_name, 
                queue=queue_name, 
                routing_key=key)
        self.channel.stop_consuming()        

    def publish(self, keys, callback, body):
        result = self.channel.queue_declare('', exclusive=True)
        queue_name = result.method.queue
        for key in keys:
            self.channel.queue_bind(
                exchange=self.exchange_name,
                queue=queue_name,
                routing_key=key
            )

        self.channel.basic_publish(exchange=self.exchange_name, routing_key='request', body=body, properties=pika.BasicProperties(delivery_mode=2,),)


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

def start_publisher():

    def callback(ch, method, properties, body):
        print(" [x] %r:%r published" % (method.routing_key, body))

    with PikaMessenger() as publisher:

        publisher.publish(keys=['request'], callback=callback, body=json.dumps(['toys', 'Games']))



def start_request_consumer():

    def callback(ch, method, properties, body):
        print(" [x] %r:%r consumed" % (method.routing_key, body))
        if body:
            global inp1
            global inp2
            inps = json.loads(body)
            inp1 = inps[0]
            inp2 = inps[1]
            consumer.stop_consume(keys=['request'])
            time.sleep(1)
            consumer_thread_1 = threading.Thread(target=start_response_consumer)
            consumer_thread_1.start()
            publisher_thread = threading.Thread(target=start_life_publisher)
            publisher_thread.start()

    with PikaMessenger() as consumer:
        consumer.consume(keys=['request'], callback=callback)

def start_response_consumer():

    def callback(ch, method, properties, body):
        print(" [x] %r:%r consumed" % (method.routing_key, body))
        if body:
            consumer.stop_consume(keys=['response'])

    with PikaMessenger() as consumer:
        consumer.consume(keys=['response'], callback=callback)

def start_life_publisher(body="default body"):

    def callback(ch, method, properties, body=body):
        print(" [x] %r:%r published" % (method.routing_key, body))

    with PikaMessenger() as publisher:
        # Grabs the wiki data
        (num_items, cat_name) = (inp1, inp2)
        (entries, cats) = get_entries()
        # generate dictionary with only the selected category
        (cat_name, selected_cat) = get_selected_cats(cat_name, entries)
        top_items = get_top_items(selected_cat, int(num_items))

        publisher.publish(keys=['response'], callback=callback, body=json.dumps(top_items))

def get_entries():
    entries = {}
    cats = {}
    filename = 'amazon_co-ecommerce_sample.csv'

    # read the input file
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
                entry['number_of_reviews'] = int(row['number_of_reviews'].replace(',','')) \
                    if row['number_of_reviews'] != '' else 0
                entry['average_review_rating'] = float(row['average_review_rating'].split(' ')[0]) \
                     if row['average_review_rating'] != '' else 0
                entries[row['uniq_id']] = entry
    return (entries, cats)

def main():
    """
    # create pika connection
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672)
    )

    channel = connection.channel()
    channel.queue_declare(queue = 'hello')

    channel.basic_publish(exchange='', routing_key='hello', body=json.dumps('request'), \
         properties=pika.BasicProperties(delivery_mode=2,
    ))

    def callback(channel, method, properties, body):
        msg = json.loads(body)
        print("Received %r" % msg)

    channel.basic_consume(
        queue="hello", on_message_callback=callback, auto_ack=True
    )

    print("Waiting for messages, to exit press ctrl+C")
    channel.start_consuming()
    """
    #input("Press enter to request data. ")
   
    consumer_thread = threading.Thread(target=start_response_consumer)
    consumer_thread.start()

    publisher_thread = threading.Thread(target=start_publisher)
    publisher_thread.start()



    # check for input file
    input_file = None
    if sys.argv[0] != sys.argv[-1]:
        input_file = sys.argv[-1]

    global entries
    (entries, cats) = get_entries()

    if input_file:
        with open(input_file, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == 'toys':
                    category = row[1]
                    number = int(row[2])


    # generate the tkinter gui
    window = tk.Tk()
    window.geometry("400x500")
    selected_cat_var = tk.StringVar()
    global x_var 
    x_var = tk.IntVar()

    global listbox 
    listbox = tk.Listbox(window)
    for key, val in cats.items():
        listbox.insert(0, key)
    listbox.pack(padx=10, pady=10,fill=tk.BOTH, expand=True)

    num_items_label = tk.Label(window, text="Number of toys to output")
    num_items_label.pack()
    num_items_entry = tk.Entry(window, textvariable=x_var)
    num_items_entry.pack()

    if not input_file:
        button = tk.Button(window, text="Submit", \
            command=lambda: get_results(entries, results_listbox, (None, None), channel))
        button.pack()

    label = tk.Label(window, text="Results")
    label.pack()
    results_listbox = tk.Listbox(window)
    results_listbox.pack(padx=10, pady=10,fill=tk.BOTH, expand=True)

    if input_file:
        input_params = (category, number)
        get_results(entries, results_listbox, input_params, channel)
    window.mainloop()

if __name__ == '__main__':
    main()