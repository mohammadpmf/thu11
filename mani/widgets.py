from tkinter import *
from tkinter import messagebox, ttk, filedialog
from PIL import Image, ImageTk
from settings import *
import pymysql


class MyConnection:
    def __init__(self, user='root', password='root'):
        self.db = pymysql.connect(host='127.0.0.1', user=user, password=password)
        self.cursor = self.db.cursor()
        query = "CREATE SCHEMA IF NOT EXISTS `game`;"
        self.cursor.execute(query)
        query = "CREATE TABLE IF NOT EXISTS `game`.`games` (`id` INT UNSIGNED NOT NULL AUTO_INCREMENT,`name` VARCHAR(45) NOT NULL,`company` VARCHAR(40) NULL,`age` TINYINT UNSIGNED NULL,`price` INT UNSIGNED NOT NULL,`console` VARCHAR(30) NULL,`stock` SMALLINT UNSIGNED NOT NULL,`image` VARCHAR(200) NULL,PRIMARY KEY (`id`),UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE);"
        self.cursor.execute(query)

    def select(self, name):
        query = "SELECT * FROM `game`.`games` WHERE `name`=%s"
        values = name
        self.cursor.execute(query, values)
        return self.cursor.fetchone()

    def insert(self, name, company, age, price, console, stock, file_address):
        query = "INSERT INTO `game`.`games` (`name`, `company`, `age`, `price`, `console`, `stock`, `image`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = name, company, age, price, console, stock, file_address
        try:
            self.cursor.execute(query, values)
            self.db.commit()
            return 0
        except pymysql.err.Error as error:
            return error
    
    def delete(self, name):
        query = "DELETE FROM `game`.`games` WHERE `name`=%s"
        values = name
        result = self.cursor.execute(query, values)
        self.db.commit()
        return result
    
    def update(self, name, company, age, price, console, stock, file_address, oldname):
        query = "UPDATE `game`.`games` SET `name`=%s, `company`=%s, `age`=%s, `price`=%s, `console`=%s, `stock`=%s, `image`=%s WHERE `name`=%s;"
        values = name, company, age, price, console, stock, file_address, oldname
        try:
            self.cursor.execute(query, values)
            self.db.commit()
            return 0
        except pymysql.err.Error as error:
            return error


class InsertWindow:
    def __init__(self, root, connection: MyConnection, bg='#333333', fg='orange', fg2='orange', text="Add a game", font=('Times', 20), bd=1, labelanchor='n', relief='raised', abg="orange", afg="#333333", padx=5, pady=5):
        self.connection         = connection
        self.root               = root
        self.frame              = LabelFrame(self.root, bg=bg, fg=fg2, text=text, font=font, labelanchor=labelanchor)
        
        self.l_name             = Label(self.frame, text="Game Name: ", bg=bg, fg=fg, font=font, bd=bd, padx=padx*2, pady=pady*2)
        self.l_company          = Label(self.frame, text="Company: ", bg=bg, fg=fg, font=font, bd=bd, padx=padx, pady=pady)
        self.l_age              = Label(self.frame, text="Age Classification: ", bg=bg, fg=fg, font=font, bd=bd, padx=padx, pady=pady)
        self.l_price            = Label(self.frame, text="Price: ", bg=bg, fg=fg, font=font, bd=bd, padx=padx, pady=pady)
        self.l_console          = Label(self.frame, text="Console: ", bg=bg, fg=fg, font=font, bd=bd, padx=padx, pady=pady)
        self.l_stock            = Label(self.frame, text="Amount in stock: ", bg=bg, fg=fg, font=font, bd=bd, padx=padx, pady=pady)
        self.l_address          = Label(self.frame, text="Picture Address: ", bg=bg, fg=fg, font=font, bd=bd, padx=padx, pady=pady)

        self.e_name             = Entry(self.frame, bg=bg, fg=fg2, font=font, bd=bd, insertbackground=fg2)
        self.e_company          = Entry(self.frame, bg=bg, fg=fg2, font=font, bd=bd, insertbackground=fg2)
        self.e_age              = ttk.Combobox(self.frame, values=['', '+3', '+7', '+10', '+12', '+15', '+17', '+25'], foreground=fg2, justify='center', font=font, state='readonly')
        self.e_price            = Entry(self.frame, bg=bg, fg=fg2, font=font, bd=bd, insertbackground=fg2)
        self.e_console          = Entry(self.frame, bg=bg, fg=fg2, font=font, bd=bd, insertbackground=fg2)
        self.e_stock            = Entry(self.frame, bg=bg, fg=fg2, font=font, bd=bd, insertbackground=fg2)
        self.e_address          = Button(self.frame, bg=bg, fg=fg2, font=font, bd=bd, activebackground=abg, activeforeground=afg, text='...', command=self.seak_picture)
        self.file_address       = None
        
        self.btn_save           = Button(self.frame, bg=bg, fg=fg2, activebackground=abg, activeforeground=afg, font=font, bd=bd, text="Save", command=self.save)
        self.btn_reset          = Button(self.frame, bg=bg, fg=fg2, activebackground=abg, activeforeground=afg, font=font, bd=bd, text="Reset", command=self.reset)

        self.l_name             .grid(row=1,  column=1, sticky='news', padx=padx, pady=pady)
        self.l_company          .grid(row=3,  column=1, sticky='news', padx=padx, pady=pady)
        self.l_age              .grid(row=5,  column=1, sticky='news', padx=padx, pady=pady)
        self.l_price            .grid(row=7,  column=1, sticky='news', padx=padx, pady=pady)
        self.l_console          .grid(row=9,  column=1, sticky='news', padx=padx, pady=pady)
        self.l_stock            .grid(row=11, column=1, sticky='news', padx=padx, pady=pady)
        self.l_address          .grid(row=13, column=1, sticky='news', padx=padx, pady=pady)

        self.e_name             .grid(row=1,  column=3, sticky='news', padx=padx, pady=pady)
        self.e_company          .grid(row=3,  column=3, sticky='news', padx=padx, pady=pady)
        self.e_age              .grid(row=5,  column=3, sticky='news', padx=padx, pady=pady)
        self.e_price            .grid(row=7,  column=3, sticky='news', padx=padx, pady=pady)
        self.e_console          .grid(row=9,  column=3, sticky='news', padx=padx, pady=pady)
        self.e_stock            .grid(row=11, column=3, sticky='news', padx=padx, pady=pady)
        self.e_address          .grid(row=13, column=3, sticky='news', padx=padx, pady=pady)

        self.btn_save           .grid(row=15, column=1, sticky='news', padx=padx, pady=pady)
        self.btn_reset          .grid(row=15, column=3, sticky='news', padx=padx, pady=pady)

        combo_style = ttk.Style(self.root)
        combo_style.theme_create(f'madval_combostyle{self}', parent='alt',settings = {'TCombobox':{'configure':{'selectbackground': bg,'fieldbackground': bg,'background': bg}}})
        combo_style.theme_use(f'madval_combostyle{self}')
        combo_style.map('TCombobox', fieldbackground=[('readonly', bg)])
        combo_style.map('TCombobox', selectbackground=[('readonly', bg)])
        combo_style.map('TCombobox', selectforeground=[('readonly',  fg2)])
    
    def reset(self):
        self.e_name                 .delete(0, END)
        self.e_company              .delete(0, END)
        self.e_age                  .config(state='normal')
        self.e_age                  .delete(0, END)
        self.e_age                  .config(state='readonly')
        self.e_price                .delete(0, END)
        self.e_console              .delete(0, END)
        self.e_stock                .delete(0, END)
        self.file_address           = None
        self.e_address              .config(text='...', image='')
        self.e_name                 .focus_set()

    def seak_picture(self):
        self.file_address = filedialog.askopenfilename()
        self.set_picture()

    def set_picture(self):
        try:
            self.file_address = filedialog.askopenfilename()
            if self.file_address in [None, (), '']:
                self.file_address = None
                self.e_address.config(text='...', image='')
                return
            self.img = Image.open(self.file_address)
            self.img = self.img.resize((200, 200))
            self.img = ImageTk.PhotoImage(self.img)
            self.e_address.config(image=self.img)
        except:
            self.file_address = None
            self.e_address.config(text='...', image='')

    def grid(self, *args, **kwargs):
        self.frame.grid(*args, **kwargs)

    def place(self, *args, **kwargs):
        self.frame.place(*args, **kwargs)

    def pack(self, *args, **kwargs):
        self.frame.pack(*args, **kwargs)

    def save(self):
        name, company, age, price, console, stock, file_address = self.check_inputs()
        result = self.connection.insert(name, company, age, price, console, stock, file_address)
        if result == 0:
            messagebox.showinfo('Saved', 'Your game\'s info were saved.')
            self.reset()
            return
        messagebox.showerror('Error', result)

    def check_inputs(self):
        name          : str      = self.e_name          .get().strip()
        company       : str      = self.e_company       .get().strip()
        age           : str      = self.e_age           .get().strip()
        price         : str      = self.e_price         .get().strip()
        console       : str      = self.e_console       .get().strip()
        stock         : str      = self.e_stock         .get().strip()
        file_address  : str      = self.file_address

        if name == '':
            messagebox.showerror('Error', 'You must fill the name field')
            return 'err'
        if price == '':
            messagebox.showerror('Error', 'You must fill the price field')
            return 'err'
        try:
            price = float(price)
        except ValueError:
            messagebox.showerror('Error', 'Incorrect fromat for price')
            return 'err'
        if price < 0:
            messagebox.showerror('Error', 'Negative values are not allowed for price')
            return 'err'
        if stock == '':
            messagebox.showerror('Error', 'You must fill the stock field')
            return 'err'
        try:
            stock = int(stock)
        except ValueError:
            messagebox.showerror('Error', 'Incorrect format for stock')
            return 'err'
        if stock < 0:
            messagebox.showerror('Error', 'Negative values are not allowed for stock')
            return 'err'
        if company == '':
            company = None
        if age == '':
            age = None
        if console == '':
            console = None
        if file_address == '':
            file_address = None
        return name, company, age, price, console, stock, file_address

class DeleteWindow:
    def __init__(self, root, connection: MyConnection, bg='#333333', fg='orange', fg2='orange', text="Delete a game", font=('Times', 20), bd=1, labelanchor='n', relief='raised', abg="orange", afg="#333333", padx=10, pady=10):
        self.connection         = connection
        self.root               = root
        self.frame              = LabelFrame(self.root, bg=bg, fg=fg2, text=text, font=font, labelanchor=labelanchor)

        self.e_name             = Entry(self.frame, bg=bg, fg=fg2, font=font, bd=bd, insertbackground=fg2)
        self.btn_search         = Button(self.frame, bg=bg, fg=fg2, activebackground=abg, activeforeground=afg, font=font, bd=bd, text="Search", command=self.search)
        self.btn_delete         = Button(self.frame, bg=bg, fg=fg2, activebackground=abg, activeforeground=afg, font=font, bd=bd, text="Delete", command=self.delete)

        self.e_name             .grid(row=1,  column=1, sticky='news', padx=padx, pady=pady)
        self.btn_search         .grid(row=2,  column=1, sticky='news', padx=padx, pady=pady)
        self.btn_delete         .grid(row=3,  column=1, sticky='news', padx=padx, pady=pady)
                 

    def grid(self, *args, **kwargs):
        self.frame.grid(*args, **kwargs)

    def place(self, *args, **kwargs):
        self.frame.place(*args, **kwargs)

    def pack(self, *args, **kwargs):
        self.frame.pack(*args, **kwargs)
    
    def search(self):
        game_name = self.e_name.get().strip()
        info = self.connection.select(game_name)
        if info not in [(), None]:
            self.showinfo(info)
            return
        messagebox.showerror('Error', 'No games found')

    def delete(self):
        answer = messagebox.askyesno('Confirmation', 'Are you sure you want to delete this game?')
        if answer:
            game_name = self.e_name.get().strip()
            result = self.connection.delete(game_name)
            if result == 1:
                messagebox.showinfo('Done', 'The game was deleted')
                self.e_name.delete(0, END)
                return
            messagebox.showerror('Error', 'Operation failed')

    def showinfo(self, info):
        window = Toplevel(self.root)
        window.title('Info')
        # self.btn_search.configure(state='disabled', disabledforeground='orange')
        # self.btn_delete.configure(state='disabled', disabledforeground='orange')
        view = ttk.Treeview(window, selectmode='browse')
        view.grid(row=1, column=1, columnspan=10)
        columns = ('1', '2', '3', '4', '5', '6')
        view['columns'] = columns
        view['show'] = 'headings'
        for column in columns:
            view.column(column, width=100, anchor='c')
        view.heading('1', text='Name')
        view.heading('2', text='Company')
        view.heading('3', text='Age rating')
        view.heading('4', text='Price')
        view.heading('5', text='Console')
        view.heading('6', text='Amount in Stock')
        view.insert('', 'end', text='R1', values=info)
        

class UpdateWindow(InsertWindow):
    def __init__(self, root, connection: MyConnection, bg='#333333', fg='orange', fg2='orange', text="Update a game", font=('Times', 20), bd=1, labelanchor='n', relief='raised', abg="orange", afg="#333333", padx=5, pady=5):
        super().__init__(root, connection, bg, fg, fg2, text, font, bd, labelanchor, relief, abg, afg, padx, pady)
        self.disable()
        self.btn_save.configure(text="Update", command=self.update)
        
        self.frame2 = Frame(self.root, bg=bg)
        self.l_search_game = Label(self.frame2, text="Search games to be updated: ", bg=bg, fg=fg, font=font, bd=bd, padx=padx*2, pady=pady*2)
        self.e_search_game = Entry(self.frame2, bg=bg, fg=fg2, font=font, bd=bd, insertbackground=fg2)
        self.btn_search = Button(self.frame2, text="Search", cnf=config_btn, command=self.search)
        
        self.frame2.grid(row=0, column=1)
        self.l_search_game.grid(row=0, column=1)
        self.e_search_game.grid(row=1, column=1)
        self.btn_search.grid(row=2, column=1)
    
    def disable(self):
        self.e_name.configure(state='disabled', disabledbackground=BG)
        self.e_company.configure(state='disabled', disabledbackground=BG)
        self.e_age.configure(state='disabled')
        self.e_price.configure(state='disabled', disabledbackground=BG)
        self.e_console.configure(state='disabled', disabledbackground=BG)
        self.e_stock.configure(state='disabled', disabledbackground=BG)
        self.e_address.configure(state='disabled')
        self.btn_save.configure(state='disabled')
        self.btn_reset.configure(state='disabled')

    def enable(self):
        self.e_name.configure(state='normal')
        self.e_company.configure(state='normal')
        self.e_age.configure(state='readonly')
        self.e_price.configure(state='normal')
        self.e_console.configure(state='normal')
        self.e_stock.configure(state='normal')
        self.e_address.configure(state='normal')
        self.btn_save.configure(state='normal')
        self.btn_reset.configure(state='normal')

    def showinfo(self, info):
        self.e_name.insert(0, info[1])
        if info[2] != None:
            self.e_company.insert(0, info[2])
        if info[3] != None:
            self.e_age.config(state='normal')
            self.e_age.insert(0, info[3])
            self.e_age.config(state='readonly')
        self.e_price.insert(0, info[4])
        if info[5] != None:
            self.e_console.insert(0, info[5])
        self.e_stock.insert(0, info[6])
        if info[7] != None:
            self.file_address = info[7]
    
    def search(self):
        self.enable()
        self.reset()
        game_name = self.e_search_game.get().strip()
        info = self.connection.select(game_name)
        if info in [(), None]:
            self.disable()
            messagebox.showerror('Error', 'Game Not Found!')
        else:
            self.showinfo(info)
            messagebox.showinfo('Found', 'The game was found.\nNow you can update tha game.')

    def update(self):
        info = self.check_inputs()
        old_name = self.e_search_game.get().strip()
        for i in info:
            if i == 'err':
                return
        name, company, age, price, console, stock, file_address = info[0], info[1], info[2], info[3], info[4], info[5], info[6]
        answer = messagebox.askyesno('Confirmation', 'Are you sure you want to update this game?')
        if answer:
            result = self.connection.update(name, company, age, price, console, stock, file_address, old_name)
            if result == 0:
                messagebox.showinfo('Done', 'The game was updated')
                self.e_search_game.delete(0, END)
                self.reset()
                return
            messagebox.showerror('Error', f'Operation failed\n{result}')
