from tkinter import Tk, Button, Label, LabelFrame, W, E,N,S, Entry, END, StringVar, Toplevel, Scrollbar, filedialog, Label
from tkinter import ttk
import sqlite3
import pandas as pd
import csv
import datetime

class PV:

    db_filename = 'PV_Database.db'

    def __init__(self,root):
        self.root = root
        self.create_gui()
        ttk.style = ttk.Style()
        ttk.style.configure("Treeview", font=('helvetica',10))
        ttk.style.configure("Treeview.Heading", font=('helvetica',12,'bold'))
        
    def execute_db_query(self, query, parameters=()):
        with sqlite3.connect(self.db_filename) as conn:
            print(conn)
            print('You have successfully connected to the database')
            cursor = conn.cursor()
            query_result = cursor.execute(query, parameters)
            conn.commit()
        return query_result
        
    def create_gui(self):
        self.create_label_frame()
        self.create_message_area()
        self.create_tree_view()
        self.create_bottom_buttons()
        self.create_scrollbar()
        self.view_entries()
    
    def create_label_frame(self):
        labelframe = LabelFrame(self.root, text='Add New Entry', bg="sky blue", font="helvetica 10")
        labelframe.grid(row=0, column=5, columnspan=4, padx=8, pady=8, sticky='ew')
        Label(labelframe, text='Timestamp:', bg="green4", fg="white").grid(row=1, column=1, sticky=W, pady=2, padx=15)
        Label(labelframe, text='Y-M-D HH:MM', bg="sky blue").grid(row=1, column=3, sticky=W, pady=2, padx=15)
        self.timefield = Entry(labelframe)
        self.timefield.grid(row=1,column=2, sticky=W, padx=5,pady=2)
        Label(labelframe, text='Temperature:', bg="brown", fg="white").grid(row=2, column=1, sticky=W, pady=2, padx=15)
        self.tempfield = Entry(labelframe)
        self.tempfield.grid(row=2,column=2, sticky=W, padx=5,pady=2)
        Label(labelframe, text='Radiation:', bg="salmon1", fg="white").grid(row=3, column=1, sticky=W, pady=2, padx=15)
        self.irrfield = Entry(labelframe)
        self.irrfield.grid(row=3,column=2, sticky=W, padx=5,pady=2)
        Label(labelframe, text='Energy: ', bg="coral1", fg="white").grid(row=4, column=1, sticky=W, pady=2, padx=15)
        self.enfield = Entry(labelframe)
        self.enfield.grid(row=4,column=2, sticky=W, padx=5,pady=2)
        Button(labelframe, text='Add Entry', command=self.on_add_entry_button_clicked, bg="navy", fg="white").grid(row=5, column=2, sticky=E, padx=5, pady=5)
    
    
    def create_message_area(self):
        self.message = Label(text='', fg='red', justify="center")
        self.message.grid(row=2, column=5, columnspan=5, sticky=N)
    
    def create_tree_view(self):
        self.tree = ttk.Treeview(height=10,  
                                 columns=("temp","irr","energy"), style='Treeview')
        self.tree.configure(selectmode="extended")
        self.tree.grid(row=3, column=2, columnspan=10)
        self.tree.column("#0",minwidth=20,width=150, stretch = True)
        self.tree.column("temp",minwidth=20,width=150, stretch = True)
        self.tree.column("irr",minwidth=20,width=150, stretch = True)
        self.tree.column("energy",minwidth=20,width=150, stretch = True)
        self.tree.heading('#0', text='Timestamp', anchor=W)
        self.tree.heading("temp", text='Temperature', anchor=W)
        self.tree.heading("irr", text='Radiation', anchor=W)
        self.tree.heading("energy", text='Energy Output', anchor=W)
        
    def create_scrollbar(self):
        self.v_scrollbar = Scrollbar(orient='vertical', command=self.tree.yview)
        #self.h_scrollbar = Scrollbar(orient='horizontal', command=self.tree.xview)
        self.v_scrollbar.grid(row=3, column=1, rowspan=5, sticky='sn')
        #self.h_scrollbar.grid(row=10, column=1, columnspan=15, sticky='ew')
        
    def create_bottom_buttons(self):
        Button(text='Delete Selected', command=self.on_delete_entry_button_clicked ,bg="red",fg="white").grid(row=15, column=2, sticky=W, pady=10,padx=20)
        Button(text='Modify Selected', command=self.on_modify_entry_button_clicked,bg="purple",fg="white").grid(row=15, column=11, sticky=W)
        Button(text='Export CSV', command=self.on_export_csv_button_clicked , bg="green", fg="white").grid(row=15, column=5, sticky=W, pady=10, padx=20)
        Button(text='Import CSV', command=self.on_import_csv_button_clicked , bg="blue", fg="white").grid(row=15, column=8, sticky=W, pady=10, padx=20)
    
    def on_export_csv_button_clicked(self):
        self.transient = Toplevel()
        self.transient.title('Give Name:')
        Label(self.transient, text='Name:').grid(row=0, column=1)
        export_name_widget = Entry(self.transient)
        export_name_widget.grid(row=0, column=2)
        export_button = Button(self.transient, text='Export Name', command=lambda: self.export_csv(
            export_name_widget.get()))
        export_button.grid(row=1, column=2, sticky=E)
    
    def on_import_csv_button_clicked(self):
        file_to_import = self.BrowseFiles()
        self.import_csv(file_to_import)
        self.view_entries()
        
    
    def on_add_entry_button_clicked(self):
        self.add_new_entry()
        
    def on_delete_entry_button_clicked(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'No item selected to delete'
            return
        self.delete_entries()
        
    def on_modify_entry_button_clicked(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
            
        except IndexError as e:
            self.message['text'] = 'No item selected to modify'
            return
        self.open_modify_window()
        self.view_entries()
        
        
    def add_new_entry(self):
        if self.new_contacts_validated():
            query = 'INSERT INTO Austria_PV VALUES(?,?,?,?)'
            
            new_timestamp = datetime.datetime.strptime(self.timefield.get(),"%Y-%m-%d %H:%M")
            new_timestamp.strftime("%Y-%m-%d %H:%M")
            
            
            parameters = (self.timefield.get(),self.tempfield.get(),self.irrfield.get(),self.enfield.get())
            self.execute_db_query(query, parameters)
            self.message['text'] = 'New Contact {} added'.format(self.timefield.get())
            self.timefield.delete(0,END)
            self.tempfield.delete(0,END)
            self.irrfield.delete(0,END)
            self.enfield.delete(0,END)
            self.view_entries()
            
        else:
            self.message['text'] = 'Timestamp cannot be blank'
            self.view_entries()
        
    def new_contacts_validated(self):
        return len(self.timefield.get()) != 0 
       
    def view_entries(self):
        items = self.tree.get_children()
        for item in items:
            self.tree.delete(item)
        query = 'SELECT * FROM Austria_PV ORDER BY Timestamp desc'
        pv_entries = self.execute_db_query(query)
        for row in pv_entries:
            self.tree.insert('', 0, text=row[0], values=(row[1],row[2],row[3]))  
            
    def delete_entries(self):
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM Austria_PV WHERE Timestamp =?'
        self.execute_db_query(query, (name,))
        self.message['text'] = 'Entries for {} deleted'.format(name)
        self.view_entries()
        
    def open_modify_window(self):
        timestamp = self.tree.item(self.tree.selection())['text']
        old_temp = self.tree.item(self.tree.selection())['values'][0]
        old_irr = self.tree.item(self.tree.selection())['values'][1]
        old_en = self.tree.item(self.tree.selection())['values'][2]
        self.transient = Toplevel()
        self.transient.title('Update Entry')
        
        Label(self.transient, text='Timestamp:').grid(row=0, column=5)
        Entry(self.transient, textvariable=StringVar(
            self.transient, value=timestamp), state='readonly').grid(row=0, column=6)
        
        Label(self.transient, text='Temperature:').grid(row=1, column=5)
        Entry(self.transient, textvariable=StringVar(
            self.transient, value=old_temp), state='readonly').grid(row=1, column=6)
        new_temp_entry_widget = Entry(self.transient)
        new_temp_entry_widget.grid(row=1, column=7)
        
        Label(self.transient, text='Radiation:').grid(row=2, column=5)
        Entry(self.transient, textvariable=StringVar(
            self.transient, value=old_irr), state='readonly').grid(row=2, column=6)
        new_irr_entry_widget = Entry(self.transient)
        new_irr_entry_widget.grid(row=2, column=7)
        
        Label(self.transient, text='Energy:').grid(row=3, column=5)
        Entry(self.transient, textvariable=StringVar(
            self.transient, value=old_en), state='readonly').grid(row=3, column=6)
        new_en_entry_widget = Entry(self.transient)
        new_en_entry_widget.grid(row=3, column=7)
        
        
        Button(self.transient, text='Update Entry', command=lambda: self.update_entries(
            new_temp_entry_widget.get(), new_irr_entry_widget.get(), new_en_entry_widget.get(),
            old_temp, old_irr, old_en, timestamp)).grid(row=3, column=2, sticky=E)

            
        self.transient.mainloop()
        
        
    def update_entries(self, newtmp, newirr, newen, oldtmp, oldirr, olden, timestamp):
        
        if newtmp == '':
            newtmp = 0
            
        if newirr == '':
            newirr = 0
            
        if newen == '':
            newen = 0
        
        query = '''UPDATE Austria_PV SET AT_temperature=?, AT_radiation_direct_horizontal=?, AT_solar_generation_actual=? 
                    WHERE AT_temperature=? AND AT_radiation_direct_horizontal=? AND AT_solar_generation_actual=? AND Timestamp =?'''
        parameters = (newtmp, newirr, newen, oldtmp, oldirr, olden, timestamp)
        self.execute_db_query(query, parameters)
        self.transient.destroy()
        self.message['text'] = 'Entry of {} modified'.format(timestamp)
        self.view_entries()
    
    
    def export_csv(self, name):
        query = 'SELECT * FROM Austria_PV ORDER BY Timestamp desc'
        
        with sqlite3.connect(self.db_filename) as conn:
            print(conn)
            print('You have successfully connected to the database')
            df = pd.read_sql_query(query, conn,  parse_dates = 'Timestamp', index_col = 'Timestamp')
            export_name = name
            df.to_csv("{}.csv".format(export_name))
            conn.commit()
            self.message['text'] = "Succesfully exported file with name {}.csv".format(export_name)
        
        self.transient.destroy()
        
    def BrowseFiles(self):
        filename = filedialog.askopenfilename(initialdir = "/",
                                                   title = "Select a File",
                                                   filetypes = (("Text files",
                                                                 "*.txt*"),
                                                                ("CSV files",
                                                                 "*.csv"),
                                                                ("all files",
                                                                 "*.*")))
        
        return filename
        
    
    def import_csv(self, import_name):
        
        if  import_name == '':
            return True
        
        with open(import_name, newline='') as csvfile:
            
            reader = csv.DictReader(csvfile, delimiter=';')
            
            sql = ''' INSERT INTO Austria_PV (Timestamp,AT_temperature,AT_radiation_direct_horizontal,AT_solar_generation_actual)
                    VALUES(?,?,?,?);'''
            
            with sqlite3.connect(self.db_filename) as connx:  
            
                for row in reader:
                    my_line = tuple(row.values())
                    my_values = []
                    timestamp = datetime.datetime.strptime(my_line[0],"%d/%m/%Y %H:%M")
                    my_values.append(timestamp.strftime("%Y-%m-%d %H:%M"))
                    for i in my_line[1:]:
                        my_values.append(float(i))
            
                    cur = connx.cursor()
                    cur.execute(sql, my_values)
            
            connx.commit()
            return True
        
    
if __name__ == '__main__':
    root = Tk()
    root.title('PV Database')
    root.geometry("650x500")
    root.resizable(width=False, height=False)
    application = PV(root)
    root.mainloop()