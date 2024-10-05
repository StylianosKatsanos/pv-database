# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 20:47:33 2024

@author: Admin
"""

import tkinter as tk 
from tkinter import ttk, Toplevel, Label, Entry, StringVar, Button, E

class TreeviewEdit(ttk.Treeview):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        
        self.bind("<Double-1>", self.on_double_click)
        
        self.click_modify = []
        
    def on_double_click(self, event):

        col_clicked =  self.identify_column(event.x)
        self.selected_iid = self.focus()
        
        selected_items = self.item(self.selected_iid)
        
        if col_clicked == "#0":
            selected_text = selected_items.get('text')
            heading_name = self.heading("#0")['text']
        else:
            col_index = int(col_clicked[1:]) - 1
            selected_value = selected_items.get("values")[col_index]
            selected_text = selected_items.get('text')
            heading_name = self.column(col_clicked)['id']
            main_heading_name = self.heading("#0")['text']
            self.entry_window(main_heading_name, selected_text, heading_name, selected_value)


        return self.click_modify
    
    
    def entry_window(self, mhname, stext, hname, svalue):
        self.trans = Toplevel()
        self.trans.title('Update Entry')
        Label(self.trans, text=mhname).grid(row=1, column=2)
        Entry(self.trans, textvariable=StringVar(
            self.trans, value=stext), state='readonly').grid(row=2, column=2)
        Label(self.trans, text=hname).grid(row=1, column=3)
        Entry(self.trans, textvariable=StringVar(
            self.trans, value=svalue), state='readonly').grid(row=2, column=3)
        Label(self.trans, text='New Value').grid(row=1, column=4)
        new_value_entry_widget = Entry(self.trans)
        new_value_entry_widget.grid(row=2, column=4)
        
        self.update_button = Button(self.trans, text='Update Entry', 
               command=lambda: self.assign_values(mhname, stext, hname, new_value_entry_widget.get())).grid(row=3, column=0, sticky=E)
        
        
        
        self.trans.mainloop()
        

    def assign_values(self, *args):
        
        for i in args:
            self.click_modify.append(i)
            
        self.trans.destroy()
        
        
        
            
        
        
    
    
        
if __name__ == "__main__":
    
    
    root = tk.Tk()
    
    column_names = ("a","b")
    
    treeview = TreeviewEdit(root, columns= column_names)
    treeview.pack(fill=tk.BOTH, expand=True)
    
    treeview.heading("#0", text="5")
    treeview.heading("a", text = "A")
    treeview.heading("b", text = "B")
    
    treeview.mainloop()