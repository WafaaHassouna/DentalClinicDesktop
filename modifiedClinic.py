from tkinter import *
from tkinter import messagebox
from modifiedDBClinic import DataBase
from tkinter import ttk

db = DataBase('modifiedStore.db')

def populate_list():
    patients_list.delete(0, END)  # meaning delete every thing
    for row in db.fetch():  # fetch() is the method that I created in DataBase class
        patients_list.insert(END, row)

def add_item():
    if name_text.get() == '' or l_name_text.get() == '' or phone_text.get() == '' or nationalId_text.get() == '' or birthYear_text.get() == '' or job_text.get() == '' or city_text.get() == '' or street_text.get() == '' :
        messagebox.showerror('Required Field', 'Please, Fill the required Fields')

    else:
        db.insert(name_text.get(), l_name_text.get(), phone_text.get(), nationalId_text.get(), birthYear_text.get(), job_text.get(), city_text.get(), street_text.get(), gender_menu.get(), history_text.get(1.0, END))
        patients_list.delete(0, END)
        clear_text()
        populate_list()

def select_item(event):
    try:
        global selected_item  # I made the variable 'global' because it will be used in 'remove' method
        index = patients_list.curselection()[0]
        selected_item = patients_list.get(index)

        # To show what we selected in the boxes of each one of them :-
        name_entry.delete(0, END)
        name_entry.insert(0, selected_item[1])
        l_name_entry.delete(0, END)
        l_name_entry.insert(0, selected_item[2])
        phone_entry.delete(0, END)
        phone_entry.insert(0, selected_item[3])
        nationalId_entry.delete(0, END)
        nationalId_entry.insert(0, selected_item[4])
        birthYear_entry.delete(0, END)
        birthYear_entry.insert(0, selected_item[5])
        job_entry.delete(0, END)
        job_entry.insert(0, selected_item[6])
        city_entry.delete(0, END)
        city_entry.insert(0, selected_item[7])
        street_entry.delete(0, END)
        street_entry.insert(0, selected_item[8])
        gender_menu.delete(0, END)
        gender_menu.insert(0, selected_item[9])
        history_text.delete(1.0, END)
        history_text.insert(1.0, selected_item[10])
        
    except IndexError:
        pass

def remove_item():
    ID = selected_item[0]
    db.remove(selected_item[0])
    db.cur.execute('DELETE FROM patient_treatment WHERE patientId=?', (ID,))
    db.conn.commit()
    clear_text()
    populate_list()

def update_item():
    db.update(selected_item[0], name_text.get(), l_name_text.get(), phone_text.get(), nationalId_text.get(), birthYear_text.get(), job_text.get(), city_text.get(), street_text.get(), gender_menu.get(), history_text.get(1.0, END))
    populate_list()

def clear_text():
    name_entry.delete(0, END)
    l_name_entry.delete(0, END)
    phone_entry.delete(0, END)
    nationalId_entry.delete(0, END)
    birthYear_entry.delete(0, END)
    job_entry.delete(0, END)
    city_entry.delete(0, END)
    street_entry.delete(0, END)
    gender_menu.delete(0, END)
    history_text.delete(1.0, END)

# ===================================== Start Of Search Screen ==========================================

def search():
    search_window = Tk()
    search_window.geometry('520x600')
    search_window.title('Search')

    # ======================== Start Of View Treatment Screan ==================================
    def view_treatment():
        view_treatment_window = Tk()
        view_treatment_window.geometry('500x400')
        view_treatment_window.title("Patient's Treatments")
        global all_treatments
        if search_by_menu.get() == "Patient's ID":
            result5 = search_entry.get()
            all_treatments = db.cur.execute("SELECT * FROM patient_treatment WHERE patientId=?", (result5,))
            all_treatments = db.cur.fetchall()
            for r, rcd in enumerate(all_treatments):
                num = 0
                r +=2
                for rw in rcd:    
                    all_treatments_label = Label(view_treatment_window, text=rw, font=("bold", 11), pady=10, padx=10)
                    all_treatments_label.grid(row=r, column=num)
                    num +=1 

        if search_by_menu.get() == "National ID":
            result5 = search_entry.get()
            all_treatments = db.cur.execute("SELECT * FROM Patients JOIN patient_treatment ON patients.id = patient_treatment.patientId WHERE nationalId = ? ", (result5,))
            for r, rcd in enumerate(all_treatments):
                num = 0
                r +=2
                for rw in rcd:    
                    all_treatments_label = Label(view_treatment_window, text=rw, font=("bold", 11), pady=10, padx=10)
                    all_treatments_label.grid(row=r, column=num)
                    num +=1   

    # ======================== End Of View Treatment Screan ==================================
    def search_id():
        global rows2
        if search_by_menu.get() == "Search by":
            messagebox.showerror('', 'Please, Select a choice')

        elif search_by_menu.get() == "Patient's ID":
             result2 = search_entry.get()
             rows2 = db.cur.execute("SELECT * FROM patients WHERE id=?", (result2,))
             rows2 = db.cur.fetchall()
             if not rows2:
                messagebox.showerror("Wrong Patient's ID", 'Patient not found')
                search_window.destroy()
             else:
                 result3 = result2
                 search_options()


        elif search_by_menu.get() == "National ID":
             result4 = search_entry.get()
             row2 = db.cur.execute("SELECT * FROM patients WHERE nationalId=?", (result4,))
             rows2 = db.cur.fetchall()
             if not rows2:
                messagebox.showerror('Wrong National ID', 'Patient not found')
                search_window.destroy()
             else:
                 result3 = result4
                 search_options()


    def save_edits():
        global result3
        result3 = search_entry.get()
        patient_name = name_entry2.get()
        last_name = l_name_entry2.get()
        phone_no = phone_entry2.get()
        nationalId_no = nationalId_entry2.get()
        birthYear = birthYear_entry2.get()
        jobName = job_entry2.get()
        city_name = city_entry2.get()
        street_name = street_entry2.get()
        history = history_text2.get(1.0, END)
        db.cur.execute('UPDATE patients SET name = ?, l_name = ?, phone = ?, nationalId = ?, birthYear = ?, job = ?, city = ?, street = ?, history = ? WHERE id = ?',
                         (patient_name, last_name, phone_no, nationalId_no, birthYear, jobName, city_name, street_name, history, result3))
        db.conn.commit()

        populate_list()
        search_window.destroy()


    def search_options():
        # 1.Name:-
        global name_entry2
        name_text2 = StringVar()
        name_label2 = Label(search_window, text="Patient's name", font=('bold', 11))
        name_label2.grid(row=4, column=0)  
        name_entry2 = Entry(search_window, textvariable=name_text2)
        name_entry2.grid(row=4, column=1)
        name_entry2.insert(0, rows2[0][1])

        # 2.L_Name:-
        global l_name_entry2
        l_name_text2 = StringVar()
        l_name_label2 = Label(search_window, text="Last name", font=('bold', 11))
        l_name_label2.grid(row=5, column=0)  
        l_name_entry2 = Entry(search_window, textvariable=l_name_text2)
        l_name_entry2.grid(row=5, column=1)
        l_name_entry2.insert(0, rows2[0][2])

        # 3.Phone No.:-
        global phone_entry2
        phone_text2 = StringVar()
        phone_label2 = Label(search_window, text='Phone No.', font=('bold', 11))
        phone_label2.grid(row=6, column=0)
        phone_entry2 = Entry(search_window, textvariable=phone_text2)
        phone_entry2.grid(row=6, column=1)
        phone_entry2.insert(0, rows2[0][3])

        # 4.National Id :-
        global nationalId_entry2
        nationalId_text2 = StringVar()
        nationalId_label2 = Label(search_window, text='National Id', font=('bold', 11))
        nationalId_label2.grid(row=7, column=0)
        nationalId_entry2 = Entry(search_window, textvariable=nationalId_text2)
        nationalId_entry2.grid(row=7, column=1)
        nationalId_entry2.insert(0, rows2[0][4])

        # 5.Birth Year :-
        global birthYear_entry2
        birthYear_text2 = StringVar()
        birthYear_label2 = Label(search_window, text='Birth Year', font=('bold', 11))
        birthYear_label2.grid(row=8, column=0)
        birthYear_entry2 = Entry(search_window, textvariable=birthYear_text2)
        birthYear_entry2.grid(row=8, column=1)
        birthYear_entry2.insert(0, rows2[0][5])

        # 6.Job :-
        global job_entry2
        job_text2 = StringVar()
        job_label2 = Label(search_window, text="Patient's job", font=('bold', 11))
        job_label2.grid(row=9, column=0)
        job_entry2 = Entry(search_window, textvariable=job_text2)
        job_entry2.grid(row=9, column=1)
        job_entry2.insert(0, rows2[0][6])

        # 7.Address :-
        address_label2 = Label(search_window, text="Addr :       ", font=('bold', 11), pady=14)
        address_label2.grid(row=10, column=0, sticky=E)

        # 7. a) City :-
        global city_entry2
        city_text2 = StringVar()
        city_label2 = Label(search_window, text="City", font=('bold', 8))
        city_label2.grid(row=11, column=0, sticky=E)
        city_entry2 = Entry(search_window, textvariable=city_text2)
        city_entry2.grid(row=11, column=1)
        city_entry2.insert(0, rows2[0][7])

        # 7. b) street :-
        global street_entry2
        street_text2 = StringVar()
        street_label2 = Label(search_window, text="Street", font=('bold', 8), pady=14)
        street_label2.grid(row=12, column=0, sticky=E)
        street_entry2 = Entry(search_window, textvariable=street_text2)
        street_entry2.grid(row=12, column=1)
        street_entry2.insert(0, rows2[0][8])

        # 8.History :-
        global history_text2
        history_label2 = Label(search_window, text="History", font=('bold', 11))
        history_label2.grid(row=13, column=0)
        history_text2 = Text(search_window, height=8, width=20, font=("Helvetica", 10))
        history_text2.grid(row=13, column=1)
        history_text2.insert(1.0, rows2[0][10])

        # 9. Gender :-
        gender_label2 = Label(search_window, text="Gender :", font=('bold', 11), pady=10)
        gender_label2.grid(row=14, column=0)
        gender_label3 = Label(search_window, text=rows2[0][9], font=("bold", 11), pady=10)
        gender_label3.grid(row=14, column=1)

        # Add Treatment Button :-
        treatment_btn2 = Button(search_window, text='Add Treatment', width=12, command=add_treatment)
        treatment_btn2.grid(row=15, column=0, padx=10)

        # Save Edits Button :-       
        save_edits_btn = Button(search_window, text='Save Edits', command=save_edits)
        save_edits_btn.grid(row=15, column=1, pady=15)

        # View Treatment Button :-
        view_treatment_btn = Button(search_window, text='View Treatment', command=view_treatment)
        view_treatment_btn.grid(row=4, column=2, pady=15)


    search_text = StringVar()
    search_label = Label(search_window, text="Enter Patient's Id : ", font=('bold',11), pady=20)
    search_label.grid(row=0, column=0)
    search_entry = Entry(search_window, textvariable=search_text)
    search_entry.grid(row=0, column=1)
    search_click = Button(search_window, text='Search', width=10, command=search_id)
    search_click.grid(row=0, column=3, padx=10)

    search_by_menu = ttk.Combobox(search_window, value=["Search by","Patient's ID","National ID"])
    search_by_menu.current(0)
    search_by_menu.grid(row=0, column=2)

# ================================= End Of Search Screan =========================================    



# ================================ Start of Treatment Screen =====================================

def add_treatment():
    treatment_window = Tk()
    treatment_window.geometry('500x300')
    treatment_window.title('Treatment')

    def exit_treatment():
        treatment_window.destroy()

    def treatment():
        db.cur.execute('INSERT INTO patient_treatment VALUES (?, ?, ?)', (patientId_entry.get(), visitDate_entry.get(), treatment_text.get(1.0, END)))
        db.conn.commit()
        clear_treatment_text()

    def clear_treatment_text():
        patientId_entry.delete(0, END) 
        visitDate_entry.delete(0, END) 
        treatment_text.delete(1.0, END)

    patientId_text = StringVar()
    patientId_label = Label(treatment_window, text="Patient's ID", font=('bold', 12), pady=10)
    patientId_label.grid(row=0, column=0, sticky=W)  
    patientId_entry = Entry(treatment_window, textvariable=patientId_text)
    patientId_entry.grid(row=0, column=1, sticky=W)

    visitDate_text = StringVar()
    visitDate_label = Label(treatment_window, text="Visit date", font=('bold', 12), pady=10)
    visitDate_label.grid(row=1, column=0, sticky=W)  
    visitDate_entry = Entry(treatment_window, textvariable=visitDate_text)
    visitDate_entry.grid(row=1, column=1, sticky=W)

    treatment_label = Label(treatment_window, text="Treatment", font=('bold', 12))
    treatment_label.grid(row=2, column=0)
    treatment_text = Text(treatment_window, height=10, width=50, font=("Helvetica", 9))
    treatment_text.grid(row=2, column=1)

    addTreatment_btn = Button(treatment_window, text='Add', width=12, command=treatment)  
    addTreatment_btn.grid(row=3, column=0, pady=8,padx=5)

    clearTreatment_btn = Button(treatment_window, text='Clear text', width=12, command=clear_treatment_text)  
    clearTreatment_btn.grid(row=3, column=1, padx=5, sticky=W)

    exitTreatment_btn = Button(treatment_window, text='Exit', width=12, command=exit_treatment)  
    exitTreatment_btn.grid(row=0, column=1, padx=5, sticky=E)
                         

# ================================= End Of Treatment Screan =========================================    


# Create a window object:-
root = Tk()

# Create the Widgets:-
# 1.Name:-
name_text = StringVar()
name_label = Label(root, text="Patient's name", font=('bold', 14), pady=7)
name_label.grid(row=0, column=0, sticky=W)  # To place the 'Label' onto the window
name_entry = Entry(root, textvariable=name_text)
name_entry.grid(row=0, column=1)

# 2.L_Name:-
l_name_text = StringVar()
l_name_label = Label(root, text="Last name", font=('bold', 14))
l_name_label.grid(row=0, column=2, sticky=E)  
l_name_entry = Entry(root, textvariable=l_name_text)
l_name_entry.grid(row=0, column=3)

# 3.Phone No.:-
phone_text = StringVar()
phone_label = Label(root, text='Phone No.', font=('bold', 14))
phone_label.grid(row=1, column=2, sticky=E)
phone_entry = Entry(root, textvariable=phone_text)
phone_entry.grid(row=1, column=3)

# 4.National Id :-
nationalId_text = StringVar()
nationalId_label = Label(root, text='National Id', font=('bold', 14), pady=12)
nationalId_label.grid(row=1, column=0, sticky=E)
nationalId_entry = Entry(root, textvariable=nationalId_text)
nationalId_entry.grid(row=1, column=1)

# 5.Birth Year :-
birthYear_text = StringVar()
birthYear_label = Label(root, text='Birth Year', font=('bold', 14))
birthYear_label.grid(row=2, column=0, sticky=E)
birthYear_entry = Entry(root, textvariable=birthYear_text)
birthYear_entry.grid(row=2, column=1)

# 6.Job :-
job_text = StringVar()
job_label = Label(root, text="Patient's job", font=('bold', 14))
job_label.grid(row=2, column=2, sticky=E)
job_entry = Entry(root, textvariable=job_text)
job_entry.grid(row=2, column=3)

# 7.Address :-
address_label = Label(root, text="Addr :       ", font=('bold', 14), pady=12)
address_label.grid(row=4, column=0, sticky=E)

# 7. a) City :-
city_text = StringVar()
city_label = Label(root, text="City", font=('bold', 10))
city_label.grid(row=4, column=0, sticky=E)
city_entry = Entry(root, textvariable=city_text)
city_entry.grid(row=4, column=1)

# 7. b) street :-
street_text = StringVar()
street_label = Label(root, text="Street", font=('bold', 10), pady=14)
street_label.grid(row=5, column=0, sticky=E)
street_entry = Entry(root, textvariable=street_text)
street_entry.grid(row=5, column=1)

# 8.Gender :-
gender_label = Label(root, text="Gender", font=('bold', 14))
gender_label.grid(row=4, column=2, sticky=E)
gender_menu = ttk.Combobox(root, value=["Male","Female"])
gender_menu.current(0)
gender_menu.grid(row=4, column=3)

# 9.History :-
history_label = Label(root, text="History", font=('bold', 14))
history_label.grid(row=6, column=0)
history_text = Text(root, height=8, width=20, font=("Helvetica", 11))
history_text.grid(row=6, column=1)


# Patients List (Listbox) :-
patients_list = Listbox(root, height=11, width=90, border=0)
patients_list.grid(row=8, column=1, columnspan=3, rowspan=6, pady=10, padx=0)  # column=0 because we need to connect 3 columns together

# Create Scrollbar :-
scroll_bar = Scrollbar(root)
scroll_bar.grid(row=9, column=4)

scroll_bar2 = Scrollbar(root, orient=HORIZONTAL)
scroll_bar2.grid(row=14, column=2)

# Connect the 'Scrollbar' to the 'list' :-
patients_list.configure(yscrollcommand=scroll_bar.set)
patients_list.configure(xscrollcommand=scroll_bar2.set)

scroll_bar.configure(command=patients_list.yview)
scroll_bar2.configure(command=patients_list.xview)  # 'yview' to scroll through "Y" axis

# To Select what will we remove :-
patients_list.bind('<<ListboxSelect>>', select_item)

# Buttons :-
add_btn = Button(root, text='Add Patient', width=15, height=2, command=add_item)  # 'commend' to connect the 'button' to what it will do
add_btn.grid(row=6, column=2)

clear_btn = Button(root, text='Clear input', width=15, height=2, command=clear_text)
clear_btn.grid(row=6, column=3)

update_btn = Button(root, text='Update', width=12, command=update_item)
update_btn.grid(row=9, column=0)

remove_btn = Button(root, text='Remove Patient', width=12, command=remove_item)
remove_btn.grid(row=10, column=0)

search_btn = Button(root, text='Search', width=12, command=search)
search_btn.grid(row=0, column=4, sticky=W)

treatment_btn = Button(root, text='Add Treatment', width=12, command=add_treatment)
treatment_btn.grid(row=1, column=4, sticky=W)


root.title("Dental clinic")
root.geometry("800x590")

# Setting icon 
p1 = PhotoImage(file = '—Pngtree—cute_3696341.png') 
root.iconphoto(False, p1)

# Populate data :-
populate_list()

root.mainloop()

