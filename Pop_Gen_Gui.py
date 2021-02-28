import requests
from tkinter import *
from tkinter import filedialog
import csv
import json

root = Tk()
root.title("Census Gen")


def error_window(err_text):
    """
    Displays an external window explaining the error
    """
    err_window = Toplevel()
    err_window.geometry("300x150")
    err_label = Label(err_window, text=err_text, justify=CENTER)
    err_label.pack()
    err_button = Button(err_window, text="OK", padx=20, pady=10,
                        command=err_window.destroy)
    err_button.pack(anchor='se')


def api(y_input, s_input):
    """
    calls API using year and state inputs from the user inputs
    """
    api_address = "".join(['https://api.census.gov/data/', y_input,
            '/acs/acs1/profile?get=NAME,DP02_0001E&for=state:', s_input])
    response = requests.get(api_address)
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        error_window("API Error")


def close():
    """
    exits program when called
    """
    root.destroy()


def check_inputs():
    """
    Checks if year and state inputs are valid and calls
    API, display_data, write_data, clear_inputs if True,
    else calls error_window
    """
    inp_check = True
    year = e_year.get()
    state_inp = e_state.get()
    year_list = ['2005', '2006', '2007', '2008', '2009',
                 '2010', '2011', '2012', '2013', '2014',
                 '2015', '2016', '2017', '2018', '2019']
    if str(year) == '':
        error_window("Please enter the correct year (2005-2019)")
        return
    if state_inp == "":
        error_window("Please enter the correct state or state abbreviation")
        return
    if str(year) in year_list:
        inp_check = True
    else:
        error_window("Please enter the correct year (2005-2019)")
        return

    state_inp = e_state.get()
    state_inp = state_inp.upper()
    us_state_abbrev = {
        'ALABAMA': 'AL',  # 01
        'ALASKA': 'AK',  # 02
        'empty1': '',  # 03 does not exist
        'ARIZONA': 'AZ',  # 04
        'ARKANSAS': 'AR',  # 05
        'CALIFORNIA': 'CA',  # 06
        'empty2': "",  # 07 does not exist
        'COLORADO': 'CO',  # 08
        'CONNECTICUT': 'CT',  # 09
        'DELAWARE': 'DE',  # 10
        'DISTRICT OF COLUMBIA': 'DC',  # 11
        'FLORIDA': 'FL',  # 12
        'empty3': '',  # 13
        'GEORGIA': 'GA',  # 14
        'HAWAII': 'HI',  # 15
        'IDAHO': 'ID',  # 16
        'ILLINOIS': 'IL',  # 17
        'INDIANA': 'IN',  # 18
        'IOWA': 'IA',  # 19
        'KANSAS': 'KS',  # 20
        'KENTUCKY': 'KY',  # 21
        'LOUISIANA': 'LA',  # 22
        'MAINE': 'ME',  # 23
        'MARYLAND': 'MD',  # 24
        'MASSACHUSETTS': 'MA',  # 25
        'MICHIGAN': 'MI',  # 26
        'MINNESOTA': 'MN',  # 27
        'MISSISSIPPI': 'MS',  # 28
        'MISSOURI': 'MO',  # 29
        'MONTANA': 'MT',  # 30
        'NEBRASKA': 'NE',  # 31
        'NEVADA': 'NV',  # 32
        'NEW HAMPSHIRE': 'NH',  # 33
        'NEW JERSEY': 'NJ',  # 34
        'NEW MEXICO': 'NM',  # 35
        'NEW YORK': 'NY',  # 36
        'NORTH CAROLINA': 'NC',  # 37
        'NORTH DAKOTA': 'ND',  # 38
        'OHIO': 'OH',  # 39
        'OKLAHOMA': 'OK',  # 40
        'OREGON': 'OR', # 41
        'PENNSYLVANIA': 'PA',  # 42
        'PUERTO RICO': 'PR',  # 43
        'RHODE ISLAND': 'RI',  # 44
        'SOUTH CAROLINA': 'SC',  # 45
        'SOUTH DAKOTA': 'SD',  # 46
        'TENNESSEE': 'TN',  # 47
        'TEXAS': 'TX',  # 48
        'UTAH': 'UT',  # 49
        'VERMONT': 'VT',  # 50
        'VIRGINIA': 'VA',  # 51
        'WASHINGTON': 'WA',  # 52
        'WEST VIRGINIA': 'WV',  # 53
        'WISCONSIN': 'WI',  # 54
        'WYOMING': 'WY'  # 55
    }
    if state_inp in us_state_abbrev.values():
        inp_check = True
        # returns location in us_state_abbrev dictionary needed for API
        location = [i for i, t in enumerate(us_state_abbrev.values()) if t == state_inp]
    elif state_inp in us_state_abbrev:
        inp_check = True
        # returns location in us_state_abbrev dictionary needed for API
        location = [i for i, t in enumerate(us_state_abbrev) if t == state_inp]
    else:
        error_window("Please enter the correct state or state abbreviation")
        return

    if inp_check:
        api_data = api(str(year), str(location[0]+1))
        display_data(year, api_data[1][0], api_data[1][1])
        write_data(year, api_data[1][0], api_data[1][1])
        clear_inputs()


def display_data(year_out, state_out, pop_out):
    """
    displays results in lower right window
    """
    y_out_label = Label(r_frame, text=year_out, bg='#E7F0EA')
    y_out_label.grid(row=1, column=0)
    s_out_label = Label(r_frame, text=state_out, bg='#E7F0EA')
    s_out_label.grid(row=1, column=1)
    pop_out_label = Label(r_frame, text=pop_out, bg='#E7F0EA')
    pop_out_label.grid(row=1, column=2)


def clear_inputs():
    """
    clears both input fields in the GUI when called
    """
    e_year.delete(0, END)
    e_state.delete(0, END)


# Create left and right containers
l_frame = Frame(root, bg='#A9DFBF', width=250, height=450, pady=3,
                highlightbackground="black", highlightthickness=1)
r_frame = Frame(root, bg='#E7F0EA', width=600, height=450, pady=3,
                highlightbackground="black", highlightthickness=1)
# headers frames for GUI
header_bar = Frame(r_frame, bg='#DEDEDE', width=200, height=30, pady=3,
                highlightbackground="#ADB9B0", highlightthickness=1)
header_bar2 = Frame(r_frame, bg='#DEDEDE', width=200, height=30, pady=3,
                highlightbackground="#ADB9B0", highlightthickness=1)
header_bar3 = Frame(r_frame, bg='#DEDEDE', width=200, height=30, pady=3,
                highlightbackground="#ADB9B0", highlightthickness=1)
# header labels and placement of year, state, and population
header_state = Label(header_bar, text="Year", bg="#DEDEDE")
header_state.place(relx = 0.5, rely = 0.5, anchor='center')
header_state = Label(header_bar2, text="State", bg="#DEDEDE")
header_state.place(relx = 0.5, rely = 0.5, anchor='center')
header_pop = Label(header_bar3, text="Population", bg="#DEDEDE")
header_pop.place(relx = 0.5, rely = 0.5, anchor='center')

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# location of frames
l_frame.grid(row=0, column=0, sticky='nw')
r_frame.grid(row=0, column=1, columnspan=3, sticky="ne")
header_bar.grid(row=0, column=0, sticky='nw')
header_bar2.grid(row=0, column=1, sticky='nw')
header_bar3.grid(row=0, column=2, sticky='nw')

# label and input field diplay
year_label = Label(l_frame, text="Input Year", bg='#A9DFBF')
year_label.place(relx = 0.2, rely = 0.35, anchor='center')
e_year = Entry(l_frame, width=35, borderwidth=3)
e_year.place(relx=.5, rely=.4, anchor='center')
state_label = Label(l_frame, text="Input State", bg='#A9DFBF')
state_label.place(relx = 0.2, rely = 0.50, anchor='center')
e_state = Entry(l_frame, width=35, borderwidth=3)
e_state.place(relx=.5, rely=.55, anchor='center')
run_button = Button(l_frame, text="Get Data", padx=30, pady=5, command=check_inputs)
run_button.place(relx=.5, rely=.7, anchor='center')


def read_data():
    """
    Opens input.csv file if it exist, else returns nothing
    """
    try:
        with open('pop_input.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            cnt = 0
            for row in csv_reader:
                if cnt == 1:
                    e_year.insert(0, row[0])
                    e_state.insert(0, row[1])
                    return True
                cnt += 1
    except IOError:
        return False


def write_data(year_out, state_out, pop_out):
    """
    Saves data to output.csv
    """
    with open('pop_output.csv', 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Input_Year', 'Input_State', 'Population'])
        csv_writer.writerow([year_out, state_out, pop_out])

def open_file():
    global cvs_file
    root.filename = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("jpeg files", "*.jpg"),("all files", "*.*")))
    print(root.filename)


menu_bar = Menu(root)
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=clear_inputs)
file_menu.add_command(label="Open", command=read_data)
file_menu.add_command(label="Save", command=write_data)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=close)
menu_bar.add_cascade(label="File", menu=file_menu)
root.config(menu=menu_bar)

read_data()

if __name__ == '__main__':
    root.mainloop()
