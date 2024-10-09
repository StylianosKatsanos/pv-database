# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 21:57:27 2024

@author: stkats
"""

from tkinter import Tk, Button, Label, LabelFrame, W, E,N,S, Entry, END, StringVar, Toplevel, Scrollbar, filedialog, BooleanVar
from tkinter import ttk


class Filter_Window:
    
    def __init__(self,root):
        self.text = ''
        self.root = root
        self.create_gui()
        self.filter = ()
        
        
    def create_gui(self):
        self.filter_choices()
        self.create_message_box()
        self.create_buttons()
        
    
    def create_message_box(self):
        self.filter_message = Label(self.root,text='', fg='red', justify="center", wraplength=420)
        self.filter_message.grid(row=7, column=1, columnspan=5, rowspan=2, sticky=W)
    
    
    def filter_choices(self):
        
        self.time_bool = BooleanVar()
        self.time_text = StringVar()
        self.irr_bool = BooleanVar()
        self.irr_text = StringVar()
        self.pr_bool = BooleanVar()
        self.pr_select = BooleanVar()
        self.ava_bool = BooleanVar()
        self.ava_select = BooleanVar()
        
        time_check = ttk.Checkbutton(self.root, variable=self.time_bool, text='Timestamp', onvalue=True, offvalue=False)
        irr_check = ttk.Checkbutton(self.root, variable=self.irr_bool, text='Irradiance', onvalue=True, offvalue=False)
        pr_check = ttk.Checkbutton(self.root, variable=self.pr_bool,text='PR Exclude')
        ava_check = ttk.Checkbutton(self.root, variable=self.ava_bool,text='AVA Exclude')
        
        time_check.grid(row=0, column=0, padx=8, pady=8,sticky='ew')
        irr_check.grid(row=1, column=0, padx=8, pady=8,sticky='ew')
        pr_check.grid(row=2, column=0, padx=8, pady=8,sticky='ew')
        ava_check.grid(row=3, column=0, padx=8, pady=8,sticky='ew')
        
        
        self.combobox_time = ttk.Combobox(self.root, textvariable=self.time_text,values=('>', '<', '=', 'between'))
        self.combobox_irr = ttk.Combobox(self.root, textvariable=self.irr_text, values=('>', '<', '=', 'between'))
        
        self.combobox_time.grid(row=0, column=1, columnspan=2, padx=8, pady=8, sticky='ew')
        self.combobox_irr.grid(row=1, column=1, columnspan=2, padx=8, pady=8, sticky='ew')
        
        self.entry_time_1  = Entry(self.root)
        self.entry_time_2  = Entry(self.root)
        label_time = Label(self.root, text='and')
        
        self.entry_time_1.grid(row=0, column=3)
        self.entry_time_2.grid(row=0, column=5)
        label_time.grid(row=0, column= 4)
       
        
        self.entry_irr_1  = Entry(self.root)
        self.entry_irr_2  = Entry(self.root)
        label_irr = Label(self.root, text='and')
       
        self.entry_irr_1.grid(row=1, column=3)
        self.entry_irr_2.grid(row=1, column=5)
        label_irr.grid(row=1, column= 4)
        
        
        
        pr_r1 = ttk.Radiobutton(self.root, text='1', value=True, variable=self.pr_select)
        pr_r2 = ttk.Radiobutton(self.root, text='0', value=False, variable=self.pr_select)
        ava_r1 = ttk.Radiobutton(self.root, text='1', value=True, variable=self.ava_select)
        ava_r2 = ttk.Radiobutton(self.root, text='0', value=False, variable=self.ava_select)

        pr_r1.grid(row=2, column=1,sticky='w')
        pr_r2.grid(row=2, column=2,sticky='w')
        ava_r1.grid(row=3, column=1,sticky='w')
        ava_r2.grid(row=3, column=2,sticky='w')
        
        
        
    def create_buttons(self):
        
        seperator = ttk.Separator(self.root, orient='horizontal')
        seperator.grid(row=6, column = 0, columnspan = 10, sticky='ew')
        
        text_button = Button(self.root, text="Filter Text : ", width='15', command=self.on_create_filter_button_clicked)
        self.load_button = Button(self.root, text="Apply", width='15')
        text_button.grid(row=7, column = 0, padx=8, pady=8, sticky='w')
        self.load_button.grid(row=9, column = 0, padx=8, pady=8, sticky='w')
        
    
        
    def on_create_filter_button_clicked(self):
        filtxt = self.create_filter_text()
        #filtxt, filpar = self.create_filter_text()
        #self.filter = (filtxt, filpar)
        self.filter = filtxt
        
        
    def create_filter_text(self):
        
        filter_text = ''
        
        if self.time_bool.get() == True or self.irr_bool.get() == True or self.pr_bool.get() == True or self.ava_bool.get() == True:
            filter_text += 'WHERE '
        
        
        if self.time_bool.get() == True:
            if str(self.combobox_time.get()) == 'between': 
                filter_text += 'Timestamp ' + 'BETWEEN ' + '"{}"'.format(str(self.entry_time_1.get())) + ' AND ' + '"{}"'.format(str(self.entry_time_2.get()))
            else:
                filter_text += 'Timestamp ' + str(self.combobox_time.get()) + '"{}"'.format(str(self.entry_time_1.get()))
            
            
        if self.irr_bool.get() == True:
            if filter_text != 'WHERE ':
                if str(self.combobox_irr.get()) == 'between':
                    filter_text += ' AND Irradiance ' + 'BETWEEN ' + str(self.entry_irr_1.get()) + ' AND ' + str(self.entry_irr_2.get())

                else:
                    filter_text += ' AND Irradiance ' + str(self.combobox_irr.get()) +  str(self.entry_irr_1.get())
            else:
                if str(self.combobox_irr.get()) == 'between':
                    filter_text += 'Irradiance ' + 'BETWEEN ' + str(self.entry_irr_1.get()) + ' AND ' + str(self.entry_irr_2.get())
                else:
                    filter_text += 'Irradiance ' + str(self.combobox_irr.get()) + str(self.entry_irr_1.get())
            
        if self.pr_bool.get() == True:
            if filter_text != 'WHERE ':
                filter_text += ' AND PR_Exclude=' + str(self.pr_select.get())
            else:
                filter_text += 'PR_Exclude=' + str(self.pr_select.get())
            
        if self.ava_bool.get() == True:
            if filter_text != 'WHERE ':
                filter_text += ' AND AVA=' + str(self.ava_select.get())
            else:
                filter_text += 'AVA=' + str(self.ava_select.get())
        
        
        self.filter_message['text'] = filter_text
        
        return filter_text
        
        
        
        
if __name__ == '__main__':
    root = Tk()
    root.title('Filter Window')
    root.geometry("600x250")
    root.resizable(width=False, height=False)
    application = Filter_Window(root)
    root.mainloop()
