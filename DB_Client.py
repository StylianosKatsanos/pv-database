from tkinter import Tk, Button, Label, LabelFrame, W, E,N,S, Entry, END, StringVar, Toplevel, Scrollbar, filedialog
from tkinter import ttk
import sqlite3
import pandas as pd
import csv
import datetime
from filter_window import Filter_Window
from treeview_edit import TreeviewEdit

class DB:

    def __init__(self,root):
        self.db_filename = ''
        self.table = ''
        self.root = root
        self.create_gui()
        self.filter = ''
        self.headers = []
        ttk.style = ttk.Style()
        ttk.style.configure("Treeview", font=('helvetica',10))
        ttk.style.configure("Treeview.Heading", font=('helvetica',12,'bold'))
        

#=--------------------------------------Execute SQLite queries--------------------------------------------------------=#
        
    def execute_db_query(self, query, parameters=()):
        with sqlite3.connect(self.db_filename) as conn:
            #print(conn)
            #print('You have successfully connected to the database and executed the query')
            cursor = conn.cursor()
            query_result = cursor.execute(query, parameters)
            conn.commit()
        return query_result

#=-----------------------------------------Create GUI-------------------------------------------------------------------=#
        
    def create_gui(self):
        self.create_message_area()
        self.create_label_frame()
        self.create_tree_view(())
        self.create_top()
        self.create_bottom_buttons()
        self.create_scrollbar()
    
    def create_label_frame(self):
        self.labelframe = LabelFrame(self.root, height=10, text='Data View', bg="sky blue", font="helvetica 10", takefocus=False)
        self.labelframe.grid(row=6, column=2, padx=8, pady=8, sticky='we', columnspan=10) 

    
    def create_message_area(self):
        self.message = Label(text='', fg='red', justify="center")
        self.message.grid(row=5, column=2, columnspan=10)
    
    def create_tree_view(self, params=()):
        self.tree = TreeviewEdit(self.labelframe,height=10,  
                                 columns=params[1:], style='Treeview', takefocus=False)
        self.tree.configure(selectmode="extended")
        self.tree.pack(fill="both",expand='yes')
        #self.tree.bind("<Double-1>", self.tree_double_click)  # Not yet implemented
        #self.tree.grid(row=6, column=2, columnspan=10)
        self.tree.column("#0",minwidth=150, stretch = True)
        self.tree.heading("#0", text='Timestamp', anchor=W)
        for i in params[1:]:
            self.tree.column(str(i),minwidth=150,width=50, stretch = True)
            self.tree.heading(str(i), text=str(i), anchor=W)


    
    def create_scrollbar(self):
        self.v_scrollbar = Scrollbar(orient='vertical', command=self.tree.yview)
        self.h_scrollbar = Scrollbar(orient='horizontal', command=self.tree.xview)
        self.v_scrollbar.grid(row=6, column=1, rowspan=5, sticky='sn')
        self.h_scrollbar.grid(row=10, column=1, columnspan=5, sticky='ew')
        
    def create_bottom_buttons(self):
        Button(text='Delete Selected', command=self.on_delete_entry_button_clicked ,bg="red",fg="white").grid(row=15, column=2, sticky=W, pady=10,padx=20)
        Button(text='Modify Selected', command=self.on_modify_entry_button_clicked,bg="purple",fg="white").grid(row=15, column=11, sticky=W)
        Button(text='Export CSV', command=self.on_export_csv_button_clicked , bg="green", fg="white").grid(row=15, column=5, sticky=W, pady=10, padx=20)
        Button(text='Import CSV', command=self.on_import_csv_button_clicked , bg="blue", fg="white").grid(row=15, column=10, sticky=W, pady=10, padx=20)
        Button(text='Filter', command=self.on_filter_entry_button_clicked, bg="white",fg="black").grid(row=16, column=2, sticky=W, pady=10,padx=20)
        Button(text='Clear Filter', command=self.on_clear_filter_button_clicked, bg="white",fg="black").grid(row=16, column=5, sticky=W, pady=10,padx=20)
    
    def create_top(self):
        Button(text='Connect', command=self.on_connect_button_clicked, bg="white",fg="black").grid(row=4, column=2, sticky=W, pady=10,padx=20)
        self.labelbase = Label(self.root, text='', bg = "white", font="helvetica 10")
        self.labelbase.grid(row=4, column=5, columnspan=2, sticky='ew')
        self.combobox_table = ttk.Combobox(self.root, textvariable=StringVar())
        self.combobox_table.grid(row=4, column=10, padx=8, pady=8, sticky='ew')
        Button(text='Refresh', command=self.refresh_view, bg="white",fg="black").grid(row=4, column=11, sticky=W, pady=10,padx=20)

    

#=--------------------------------------Button Functions -------------------------------------------------------------=#

#=--------------------------------------Top Buttons & Included Functions -------------------------------------------------------------=#
    def on_connect_button_clicked(self):
        db_to_connect = self.BrowseFiles()
        self.db_filename = db_to_connect
        self.labelbase['text'] = db_to_connect.split('/')[-1:][0]
        if self.db_filename == '':
            return 
        else:
            self.get_tables()
    
    def get_tables(self):
        query = '''SELECT name FROM sqlite_master WHERE type = "table"'''
        
        db_names = self.execute_db_query(query)
        db_names = db_names.fetchall()
        db_tables = [i[0] for i in db_names]
        self.combobox_table.configure(values=db_tables)
    
    
    def refresh_view(self, tb=None):
        if self.db_filename == '':
            self.message['text'] = "No Database to refresh data"
            return
        else:
            if tb != None:
                query = 'SELECT name FROM pragma_table_info(' + '"' + tb + '"' +');'
            else:
                query = 'SELECT name FROM pragma_table_info(' + '"' + str(self.combobox_table.get()) + '"' +');'
            result = self.execute_db_query(query)
            self.headers = []
            for i in result.fetchall():
                self.headers.append(i[0])
            self.fill_headers(self.headers)
            self.view_entries()
            
            
    def fill_headers(self, params):
        self.tree.destroy()
        self.v_scrollbar.destroy()
        self.h_scrollbar.destroy()
        self.create_tree_view(params)
        self.create_scrollbar()
    
#=--------------------------------------Bottom Buttons & Included Functions-------------------------------------------------------------=#

    def on_delete_entry_button_clicked(self):
        self.message['text'] = ''
        if self.db_filename == '':
            self.message['text'] = "No Database from which to delete data"
            return
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'No item selected to delete'
            return
        self.delete_entries()

    def delete_entries(self):
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM ' + str(self.combobox_table.get()) + ' WHERE Timestamp =?'
        self.execute_db_query(query, (name,))
        self.message['text'] = 'Entries for {} deleted'.format(name)
        self.view_entries()

    def on_export_csv_button_clicked(self):
        if self.db_filename == '':
            self.message['text'] = "No Database from which to export data"
            return
        self.transient = Toplevel()
        self.transient.title('Give Name:')
        Label(self.transient, text='Name:').grid(row=0, column=1)
        export_name_widget = Entry(self.transient)
        export_name_widget.grid(row=0, column=2)
        export_button = Button(self.transient, text='Export Name', command=lambda: self.export_csv(
            export_name_widget.get()))
        export_button.grid(row=1, column=2, sticky=E)
        
    def export_csv(self, name):
        query = 'SELECT * FROM ' + str(self.combobox_table.get()) + ' ' + self.filter +  ' ORDER BY Timestamp desc'
        
        with sqlite3.connect(self.db_filename) as conn:
            print(conn)
            print('You have successfully connected to the database')
            df = pd.read_sql_query(query, conn,  parse_dates = 'Timestamp', index_col = 'Timestamp')
            export_name = name
            df.to_csv("{}.csv".format(export_name))
            conn.commit()
            self.message['text'] = "Succesfully exported file with name {}.csv".format(export_name)
        
        self.transient.destroy()
    
    def on_import_csv_button_clicked(self):
        if self.db_filename == '':
            self.message['text'] = "No Database to import data into"
            return
        file_to_import = self.BrowseFiles()
        self.import_csv(file_to_import)
        if self.db_filename == '':
            return
        else:
            self.view_entries()
        
    def import_csv(self, import_name):
        
       if  import_name == '' or  not self.db_filename:
           print('No database to import data into or correct file to import data from')
           return
       
       with open(import_name, newline='') as csvfile:
           
           header_string = '('
           values_string = '('
           
           for i in self.headers[:-1]:
               header_string += i + ','
               values_string += '?,'
           header_string += self.headers[-1] + ')'
           values_string += '?);'
               
           reader = csv.DictReader(csvfile, delimiter=';')
           
           sql =  'INSERT INTO '  + str(self.combobox_table.get()) + ' ' + header_string + ' VALUES' + values_string
           
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
    
    
    def on_modify_entry_button_clicked(self):
        # Use size of treeview.selection for if statement
        self.message['text'] = ''
        if len(self.tree.selection()) <= 0:
            self.message['text'] = 'No item selected to modify'
            return
        self.open_modify_window(len(self.tree.selection()))
        self.view_entries()   
        
    def open_modify_window(self):
        selected_items = self.tree.selection()
       timestamp = self.tree.item(selected_items[0])['text']
       self.transient = Toplevel()
       self.transient.title('Update Entry')
       Label(self.transient, text='Timestamp:').grid(row=0, column=0)
       Entry(self.transient, textvariable=StringVar(
           self.transient, value=timestamp), state='readonly').grid(row=0, column=1)
       self.combobox_mod = ttk.Combobox(self.transient, textvariable=StringVar(), values=self.headers[1:])
       self.combobox_mod.grid(row=1, column=1)
       new_value_entry_widget = Entry(self.transient)
       new_value_entry_widget.grid(row=1, column=2)
       
       if size > 1:
           timestamp2 = self.tree.item(selected_items[-1])['text']
           Entry(self.transient, textvariable=StringVar(
               self.transient, value=timestamp2), state='readonly').grid(row=0, column=2)
       
       Button(self.transient, text='Update Entry', command=lambda: self.update_entries(self.combobox_mod.get(),
           new_value_entry_widget.get(), timestamp, timestamp2)).grid(row=3, column=0, sticky=E)
           
       self.transient.mainloop()
 

# =============================================================================
#     def tree_double_click(self, event):
#         table = str(self.combobox_table.get())
#         mod_values = self.tree.on_double_click(event)
#         self.double_click_modify(table, mod_values)
#         
#     
#     def double_click_modify(self, tb, click_modify):
#         query = 'UPDATE ' + tb + ' SET ' + str(click_modify[2]) + '=?' + ' WHERE ' + str(click_modify[0]) + '=?'
#         parameters = (str(click_modify[3]), str(click_modify[1]))
#         self.execute_db_query(query, parameters)
# =============================================================================
              
                
#=-------------------------------------------Filter Buttons--------------------------------------------------------------=#  

        
    def on_filter_entry_button_clicked(self):
        self.transient = Toplevel()
        fw = Filter_Window(self.transient)
        fw.load_button.configure(command=lambda: self.get_filter(fw.filter))
        self.transient.mainloop()
        
    def on_clear_filter_button_clicked(self):
        self.filter = ''
        self.message['text'] = "Filter Cleared"
        
        
    def get_filter(self, given_fil):
        self.filter = given_fil
        self.transient.destroy()
        self.message['text']="Filter Created"
        
        
#=-----------------------------------------Other Functions------------------------------------------------------------=#

    def on_add_entry_button_clicked(self):
        self.add_new_entry()
        
        
    def add_new_entry(self):
        if self.new_contacts_validated():
            query = 'INSERT INTO contacts_list VALUES(NULL,?,?,?)'
            parameters = (self.namefield.get(),self.emailfield.get(),self.numfield.get())
            self.execute_db_query(query, parameters)
            self.message['text'] = 'New Contact {} added'.format(self.namefield.get())
            self.namefield.delete(0,END)
            self.emailfield.delete(0,END)
            self.numfield.delete(0,END)
            self.view_contacts()
            
        else:
            self.message['text'] = 'name,email and number cannot be blank'
            self.view_contacts()
        
    def new_contacts_validated(self):
        return len(self.namefield.get()) != 0 and len(self.emailfield.get()) !=0 and len(self.numfield.get()) !=0
        
    def view_entries(self):
        items = self.tree.get_children()
        for item in items:
            self.tree.delete(item)
        query = 'SELECT * FROM ' + str(self.combobox_table.get()) + ' ' + self.filter + ' ORDER BY Timestamp desc;'
        pv_entries = self.execute_db_query(query)
        for row in pv_entries:
            self.tree.insert('', 0, text=row[0] ,values=tuple(row[1:])) 
            
        
    def update_entries(self, param, newval, timestamp):
       #based on size of parameter (more timestamps) change query
       if timestamp2 != None:
           query = 'UPDATE ' + str(self.combobox_table.get()) + ' SET ' + str(param) + '=? WHERE Timestamp BETWEEN ? AND ?'
           parameters = (newval, timestamp, timestamp2)
       else:
           query = 'UPDATE ' + str(self.combobox_table.get()) + ' SET ' + str(param) + '=? WHERE Timestamp =?'
           parameters = (newval, timestamp)
       self.execute_db_query(query, parameters)
       self.transient.destroy()
       if timestamp2 !=None:
           self.message['text'] = 'Entries {} from {} until {} modified'.format(param, timestamp, timestamp2)
       else:
           self.message['text'] = 'Entry {} of {} modified'.format(param, timestamp)
       self.view_entries()
    
        
    def BrowseFiles(self):
        filename = filedialog.askopenfilename(initialdir = "/",
                                                   title = "Select a File",
                                                   filetypes = (("Database files",
                                                                 "*.db*"),
                                                                ("Text files",
                                                                 "*.txt*"),
                                                                ("CSV files",
                                                                 "*.csv"),
                                                                ("all files",
                                                                 "*.*")))
        
        return filename
    
    
if __name__ == '__main__':
    root = Tk()
    root.title('Database')
    root.geometry("750x450")
    root.resizable(width=False, height=False)
    application = DB(root)
    root.mainloop()
