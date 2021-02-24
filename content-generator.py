import sys
import tkinter as tk
import wikipedia
import csv


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
    with open("output.csv", "w") as file:
        csv_out = csv.writer(file)
        csv_out.writerow([ent_in1.get(), ent_in2.get(), wiki_out])

    # Print data in GUI
    lbl_output["text"] = wiki_out


if __name__ == "__main__":
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
        with open("output.csv", "w") as file:
            csv_out = csv.writer(file)
            csv_out.writerow([cmd1, cmd2, para])

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
