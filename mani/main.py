from widgets import *

class App:
    def __init__(self):
        connection = MyConnection()
        # root
        self.root = Tk()
        self.root.geometry('500x300')
        self.root.title('App')
        self.root.configure(bg=BG)

        # root Buttons
        self.btn_management = Button(self.root, text='Management', cnf=config_btn, command=lambda: self.change_window(self.root, self.management_window))
        self.btn_search = Button(self.root, text="Search", cnf=config_btn, command=lambda: self.change_window(self.root, self.search_window))        
        self.btn_management.pack(cnf=conifg_btn_root_pack)
        self.btn_search.pack(cnf=conifg_btn_root_pack)

        # toplevels
        self.search_window = Toplevel(self.root)
        self.management_window = Toplevel(self.root)
        self.insert_window = Toplevel(self.management_window)
        self.update_window = Toplevel(self.management_window)
        self.delete_window = Toplevel(self.management_window)

        # withdrawing windows
        self.search_window.withdraw()
        self.management_window.withdraw()
        self.insert_window.withdraw()
        self.update_window.withdraw()
        self.delete_window.withdraw()

        # configuring backgrounds
        self.search_window.configure(bg=BG)
        self.management_window.configure(bg=BG)
        self.insert_window.configure(bg=BG)
        self.update_window.configure(bg=BG)
        self.delete_window.configure(bg=BG)

        # title
        self.search_window.title('Search game')
        self.management_window.title('Management')
        self.insert_window.title('Insert game')
        self.update_window.title('Update game')
        self.delete_window.title('Delete game')

        # wm protocol
        self.search_window.protocol("WM_DELETE_WINDOW", self.root.destroy)
        self.management_window.protocol("WM_DELETE_WINDOW", self.root.destroy)
        self.insert_window.protocol("WM_DELETE_WINDOW", self.root.destroy)
        self.update_window.protocol("WM_DELETE_WINDOW", self.root.destroy)
        self.delete_window.protocol("WM_DELETE_WINDOW", self.root.destroy)

        # geometry
        self.search_window.geometry('800x600')
        self.management_window.geometry('800x300')
        self.insert_window.geometry('800x600')
        self.update_window.geometry('1000x600')
        self.delete_window.geometry('400x300')

        # ----------------- Management window widgets -----------------
        self.btn_insert = Button(self.management_window, text="Add a Game", cnf=config_btn, command=lambda: self.change_window(self.management_window, self.insert_window))
        self.btn_delete = Button(self.management_window, text="Delete a Game", cnf=config_btn, command=lambda: self.change_window(self.management_window, self.delete_window))
        self.btn_update = Button(self.management_window, text="Update a game", cnf=config_btn, command=lambda: self.change_window(self.management_window, self.update_window))
        self.btn_back_management = Button(self.management_window, text="Back", cnf=config_btn, command=lambda: self.change_window(self.management_window, self.root))

        self.btn_insert.pack(cnf=conifg_btn_root_pack)
        self.btn_update.pack(cnf=conifg_btn_root_pack)
        self.btn_delete.pack(cnf=conifg_btn_root_pack)
        self.btn_back_management.pack(cnf=conifg_btn_root_pack)

        # ----------------- Insert window widgets -----------------
        insert_window = InsertWindow(self.insert_window, connection)
        insert_window.pack()
        self.btn_back_insert = Button(self.insert_window, text="Back", cnf=config_btn, command=lambda: self.change_window(self.insert_window, self.management_window))
        self.btn_back_insert.pack()

        # ----------------- Delete window widgets -----------------
        delete_window = DeleteWindow(self.delete_window, connection)
        delete_window.pack()
        self.btn_back_delete = Button(self.delete_window, text="Back", cnf=config_btn, command=lambda: self.change_window(self.delete_window, self.management_window))
        self.btn_back_delete.pack()

        # ----------------- Update window widgets -----------------
        update_winodw = UpdateWindow(self.update_window, connection)
        update_winodw.grid(row=0, column=0, padx=50, pady=20)
        self.btn_back_update = Button(self.update_window, text="Back", cnf=config_btn, command=lambda: self.change_window(self.update_window, self.management_window))
        self.btn_back_update.grid(row=1, column=0, padx=50)

        # runs the app
        self.root.mainloop()

    @staticmethod
    def change_window(current:Tk, previous: Tk):
        current.withdraw()
        previous.deiconify()


if __name__ == '__main__':
    App()

