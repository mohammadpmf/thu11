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
search_window.geometry('800x600')
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

##################### delete window widgets ########################
def search_delete():
    name = entry_name_delete.get()
    info = connection.get(name)
    if info not in [(), None]:
        info = f"Game: {info[1]}\nCompany: {info[2]}\nAge: {info[3]}\nPrice: {info[4]}\nConsole: {info[5]}\nStock: {info[6]}"
    messagebox.showinfo("", info)
def delete_delete():
    name = entry_name_delete.get()
    answer = connection.delete(name)
    if answer == 1:
        messagebox.showinfo("Success", f"Game {name} deleted successfully!")
    else:
        messagebox.showwarning("Warning", f"Game {name} is not in table!")

lable_name_delete = Label(delete_window, text="Which game you want to delete?")
entry_name_delete = Entry(delete_window)
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
mainloop()