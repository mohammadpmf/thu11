from tkinter import ttk
import tkinter as tk

root = tk.Tk()
root.title('Products')
root.resizable(False, False)

treev = ttk.Treeview(root, selectmode='browse')
treev.grid(row=1, column=1, columnspan=10)

verscrlbar = ttk.Scrollbar(root, orient='vertical', command=treev.yview)
verscrlbar.grid(row=1, column=11, sticky='ns')
treev.configure(yscrollcommand=verscrlbar.set)

columns = ('1', '2', '3', '4', '5', '6')
treev['columns'] = columns
treev['show'] = 'headings'
for column in columns:
    treev.column(column, width=135, anchor='c')
treev.heading('1', text='Name')
treev.heading('2', text='Company')
treev.heading('3', text='Age rating')
treev.heading('4', text='Price')
treev.heading('5', text='Console')
treev.heading('6', text='Amount in Stock')

treev.insert('', 'end', text='R1', values=('GTA5', 'RockStar Games', '+17', 100, 'PS5', '90'))
treev.insert('', 'end', text='R1', values=('Clash Royale', 'Supercell', '+10', 5.99, 'Mobile', '345'))

root.mainloop()