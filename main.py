from settings import *
from myclass import *

def change_window(show_window: Tk, hide_window:Tk):
    show_window.deiconify()
    hide_window.withdraw()

connection = MyConeection()
root = Tk()
root.geometry('500x300')
root.config(bg=BG)
search_window = Toplevel(root)
management_window = Toplevel(root)
insert_window = Toplevel(management_window)
update_window = Toplevel(management_window)  
delete_window = Toplevel(management_window)
search_window.withdraw()
management_window.withdraw()
insert_window.withdraw()
update_window.withdraw()
delete_window.withdraw()
search_window.config(bg=BG)
management_window.config(bg=BG)
insert_window.config(bg=BG)
update_window.config(bg=BG)
delete_window.config(bg=BG)
search_window.protocol('WM_DELETE_WINDOW', root.destroy)
management_window.protocol('WM_DELETE_WINDOW', root.destroy)
insert_window.protocol('WM_DELETE_WINDOW', root.destroy)
update_window.protocol('WM_DELETE_WINDOW', root.destroy)
delete_window.protocol('WM_DELETE_WINDOW', root.destroy)
search_window.title('Search window')
management_window.title('Management window')
insert_window.title('Insert window')
update_window.title('Update window')
delete_window.title('Delete window')
search_window.geometry('1200x800')
management_window.geometry('800x300')
insert_window.geometry('800x600')
update_window.geometry('800x600')
delete_window.geometry('800x600')

##################### management window widgets ########################
btn_insert = Button(management_window, text='Add Game', cnf=config_btn,
    command=lambda:change_window(insert_window, management_window))
btn_update = Button(management_window, text='Update a Game', cnf=config_btn,
    command=lambda:change_window(update_window, management_window))
btn_delete = Button(management_window, text='Delete a Game', cnf=config_btn,
    command=lambda:change_window(delete_window, management_window))
btn_back_management = Button(management_window, text='Back', cnf=config_btn,
    command=lambda:change_window(root, management_window))
btn_insert.pack(cnf=config_btn_root_pack)
btn_update.pack(cnf=config_btn_root_pack)
btn_delete.pack(cnf=config_btn_root_pack)
btn_back_management.pack(cnf=config_btn_root_pack)
##################### End management window widgets ########################

##################### insert window widgets ########################
game = AddGame(insert_window, connection)
btn_back_insert = Button(insert_window, text='Back', cnf=config_btn,
    command=lambda:change_window(management_window, insert_window))
game.grid()
btn_back_insert.grid()  
##################### End insert window widgets ########################

##################### update window widgets ########################
def search_game_for_update():
    name = e_searching_game.get().strip()
    info = connection.get(name)
    print(info)
    if info in [(), None]:
        game_update.disable()
    else:
        game_update.enable()
        game_update.e_name.delete(0, END)
        game_update.e_company.delete(0, END)
        game_update.e_price.delete(0, END)
        game_update.e_console_type.delete(0, END)
        game_update.e_stock.delete(0, END)
        game_update.file_address=None
        game_update.set_picture()
        game_update.e_age.config(state='normal')
        game_update.e_age.delete(0, END)
        game_update.e_age.config(state='readonly')
        game_update.e_name.insert(0, info[1])
        if info[2] != None:
            game_update.e_company.insert(0, info[2])
        if info[3] != None:
            game_update.e_age.config(state='normal')
            game_update.e_age.insert(0, info[3])
            game_update.e_age.config(state='readonly')
        game_update.e_price.insert(0, info[4])
        if info[5] != None:
            game_update.e_console_type.insert(0, info[5])
        game_update.e_stock.insert(0, info[6])
        if info[7] != None:
            game_update.file_address=info[7]
            game_update.set_picture()
        game_update.prev_name = name

e_searching_game = Entry(update_window, cnf=config_entry)
btn_searching_game = Button(update_window, cnf=config_btn,
        text='Search this game', width=16,
        command=search_game_for_update)
game_update = UpdateGame(update_window, connection)
btn_back_update = Button(update_window, text='Back', cnf=config_btn,
    command=lambda:change_window(management_window, update_window))
e_searching_game.grid(row=0, column=1)
btn_searching_game.grid(row=0, column=2)
game_update.grid(row=1, column=1, columnspan=2)
btn_back_update.grid(row=2, column=1, columnspan=2)
##################### End update window widgets ########################


##################### delete window widgets ########################
def search_delete():
    name = entry_name_delete.get()
    info = connection.get(name)
    if info not in [(), None]:
        info = f"Game: {info[1]}\nCompany: {info[2]}\nAge: {info[3]}\nPrice: {info[4]}\nConsole: {info[5]}\nStock: {info[6]}"
    messagebox.showinfo("", info)
def delete_delete():
    name = entry_name_delete.get()
    temp = messagebox.askyesno("?", f"Delete {name}?")
    if temp:
        answer = connection.delete(name)
        if answer == 1:
            messagebox.showinfo("Success", f"Game {name} deleted successfully!")
        else:
            messagebox.showwarning("Warning", f"Game {name} is not in table!")
    else:
        messagebox.showinfo("OK", f"OK. I'll not delete {name}")

lable_name_delete = Label(delete_window, cnf=config_lbl, text="Which game you want to delete?")
entry_name_delete = Entry(delete_window, cnf=config_entry)
btn_search_delete_window = Button(delete_window, cnf=config_btn, text='Search', 
                        command=search_delete)
btn_delete_delete_window = Button(delete_window, cnf=config_btn, text='Delete',
                        command=delete_delete)
btn_back_delete = Button(delete_window, cnf=config_btn, text='Back',
                        command=lambda:change_window(management_window, delete_window))
lable_name_delete.grid(row=1, column=1)
entry_name_delete.grid(row=1, column=2)
btn_search_delete_window.grid(row=2, column=1)
btn_delete_delete_window.grid(row=2, column=2)
btn_back_delete.grid(row=3, column=1, columnspan=2, sticky='ew')
##################### End delete window widgets ########################

btn_management = Button(root, text='Management', cnf=config_btn,
    command=lambda:change_window(management_window, root))
btn_search = Button(root, text='Search', cnf=config_btn, 
    command=lambda:change_window(search_window, root))
btn_management.pack(cnf=config_btn_root_pack)
btn_search.pack(cnf=config_btn_root_pack)



treev = ttk.Treeview(search_window, selectmode ='browse')
treev.grid(row=1, column=1, columnspan=10)
verscrlbar = ttk.Scrollbar(search_window, orient ="vertical", command = treev.yview)
verscrlbar.grid(row=1, column=11, sticky='ns')
treev.configure(yscrollcommand = verscrlbar.set)
treev["columns"] = ("1", "2", "3" , "4" , "5" , "6" , "7")
treev['show'] = 'headings'
treev.column("1", width = 150, anchor ='c')
treev.column("2", width = 150, anchor ='c')
treev.column("3", width = 75 , anchor ='c')
treev.column("4", width = 100, anchor ='c')
treev.column("5", width = 100, anchor ='c')
treev.column("6", width = 75, anchor ='c')
treev.column("7", width = 200, anchor ='c')
treev.heading("1", text ="Name")
treev.heading("2", text ="Company")
treev.heading("3", text ="Age")
treev.heading("4", text ="price")
treev.heading("5", text ="console")
treev.heading("6", text ="stock")
treev.heading("7", text ="address")

all_games = connection.get_all()
for game in all_games:
    treev.insert("", 'end', text =game[0], values =(game[1:8]))
search_window.bind('<Escape>', lambda e:change_window(management_window, search_window))
mainloop()