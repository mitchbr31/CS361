import sys
import tkinter as tk
import wikipedia
import csv
import json
import pika
import time
import threading

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
        
        self.channel.basic_publish(exchange=self.exchange_name, routing_key='response', body=body, properties=pika.BasicProperties(delivery_mode=2,))


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

def start_content_publisher(body="default body"):

    def callback(ch, method, properties, body=body):
        print(" [x] %r:%r published" % (method.routing_key, body))

    with PikaMessenger() as publisher:
        # Grabs the wiki data
        para = get_wiki(cmd1, cmd2)

        publisher.publish(keys=['response'], callback=callback, body=json.dumps(para))

def start_consumer():

    def callback(ch, method, properties, body):
        print(" [x] %r:%r consumed" % (method.routing_key, body))
        if body:
            global cmd1
            global cmd2
            cmds = json.loads(body)
            cmd1 = cmds[0]
            cmd2 = cmds[1]
            consumer.stop_consume(keys=['request'])
            time.sleep(1)
            publisher_thread = threading.Thread(target=start_content_publisher)
            publisher_thread.start()

    with PikaMessenger() as consumer:
        consumer.consume(keys=['request'], callback=callback)


def get_wiki(key_1, key_2):
    # Searches for Wikipedia page
    page = wikipedia.page(key_1.lower(), auto_suggest=False)

    # Split wiki content into list (values are paragraphs)
    page_content = page.content.split(sep="\n")

    # Finds the first paragraph containing both keywords and returns it
    keyword_content = list(item for item in page_content if key_1.lower() and key_2.lower() in item.lower())

    return keyword_content[0]


def user_input():
    # Grab the Wikipedia paragraph
    wiki_out = get_wiki(ent_in1.get(), ent_in2.get())

    # Output data to csv
    to_csv(ent_in1.get(), ent_in2.get(), wiki_out)

    # Print data in GUI
    lbl_output["text"] = wiki_out


def to_csv(in1, in2, out):
    with open("output.csv", "w") as file:
        csv_out = csv.writer(file)
        csv_out.writerow([in1, in2, out])
    """
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
    )

    channel = connection.channel()
    channel.queue_declare(queue='content-gen')

    channel.basic_publish(exchange='', routing_key='content-gen', body=json.dumps([in1, in2, out]),
                          properties=pika.BasicProperties(delivery_mode=2,
                                                          ))
    channel.close()
    """
    publisher_thread = threading.Thread(target=start_content_publisher)
    publisher_thread.start()

if __name__ == "__main__":

    consumer_thread = threading.Thread(target=start_consumer)
    consumer_thread.start()
    """
    publisher_thread = threading.Thread(target=start_publisher)
    publisher_thread.start()
    """

    if len(sys.argv) == 2:
        # Command-line execution

        # Load in keywords from input csv file
        with open(sys.argv[1], "r") as infile:
            filereader = csv.reader(infile, delimiter=';')
            for row in filereader:
                # Grab the two keywords
                cmd1 = row[0]
                cmd2 = row[1]

        # Grabs the wiki data
        para = get_wiki(cmd1, cmd2)

        # Output data to csv
        to_csv(cmd1, cmd2, para)

    elif len(sys.argv) == 1:
        # GUI execution

        # Generate the tkinter window
        window = tk.Tk()
        window.title("Content Generator")
        window.resizable(width=False, height=False)

        # Grab the first keyword
        frm_input1 = tk.Frame(master=window)
        lbl_in1 = tk.Label(text="First Keyword:", master=frm_input1)
        lbl_in1.pack(side=tk.LEFT)
        ent_in1 = tk.Entry(master=frm_input1)
        ent_in1.pack(side=tk.LEFT)
        frm_input1.pack()

        # Grab the second keyword
        frm_input2 = tk.Frame(master=window)
        lbl_in2 = tk.Label(text="Second Keyword:", master=frm_input2)
        lbl_in2.pack(side=tk.LEFT)
        ent_in2 = tk.Entry(master=frm_input2)
        ent_in2.pack(side=tk.LEFT)
        frm_input2.pack()

        # Submit the keywords entered by the user
        btn_submit = tk.Button(
            text="Generate Text",
            master=window,
            command=user_input
        )
        btn_submit.pack()

        # Print the output
        lbl_out_title = tk.Label(text="Output:")
        lbl_out_title.pack()
        lbl_output = tk.Label(
            text="Output will appear here.",
            master=window,
            width=50,
            wraplength=450
        )
        lbl_output.pack()

        window.mainloop()