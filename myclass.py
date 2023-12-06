from tkinter import *
from fallah import *
from tkinter import messagebox
import pymysql
from settings import *

class MyConeection():
    def __init__(self, user='root', password='root'):
        self.db = pymysql.connect(host='127.0.0.1', user=user, password=password)
        self.cursor = self.db.cursor()
        query = "CREATE SCHEMA IF NOT EXISTS `term4`;"
        self.cursor.execute(query)
        query = "CREATE TABLE IF NOT EXISTS `term4`.`games` (`id` INT UNSIGNED NOT NULL AUTO_INCREMENT,`name` VARCHAR(45) NOT NULL,`company` VARCHAR(40) NULL,`age` TINYINT UNSIGNED NULL,`price` INT UNSIGNED NOT NULL,`console` VARCHAR(30) NULL,`stock` SMALLINT UNSIGNED NOT NULL,`image` VARCHAR(200) NULL,PRIMARY KEY (`id`),UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE);"
        self.cursor.execute(query)
    
    def insert(self,name, price, stock, company=None, age=None, console=None, address=None):
        query = "INSERT INTO `term4`.`games` (`name`, `company`, `age`, `price`, `console`, `stock`, `image`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = name, company, age, price, console, stock, address
        try:
            self.cursor.execute(query, values)
            self.db.commit()
            return 0
        except pymysql.err.IntegrityError as error: 
            return error
        except pymysql.err.DataError as error:
            return error
    def get(self, values):
        query = "SELECT * FROM `term4`.`games` WHERE `name`=%s;"
        self.cursor.execute(query, values)
        return self.cursor.fetchone()

    def delete(self, values):
        query = "DELETE FROM `term4`.`games` WHERE `name`=%s;"
        result = self.cursor.execute(query, values)
        self.db.commit()
        return result

    def update(self, name, price, stock, old_name, company=None, age=None, console=None, address=None):
        query = "UPDATE `term4`.`games` SET `name`=%s, `price`=%s, `stock`=%s, `company`=%s, `age`=%s, `console`=%s, `image`=%s WHERE `name`=%s"
        values = name, price, stock, company, age, console, address, old_name
        result = self.cursor.execute(query, values)
        self.db.commit()
        return result

    def get_all(self):
        query = "SELECT * FROM `term4`.`games`;"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    


class AddGame(MyGame):
    def __init__(self, root, connection:MyConeection, bg='#333333', fg='orange', fg2='orange', text="Game Info", font=('Times', '20'), bd=1, labelanchor='n', relief='raised', abg="orange", afg="#333333", padx=5, pady=5):
        super().__init__(root, bg, fg, fg2, text, font, bd, labelanchor, relief, abg, afg, padx, pady)
        self.connection=connection
        self.btn_save = Button(self.frame, bg=bg, fg=fg2, font=font, bd=bd,
        activebackground=abg, activeforeground=afg, text='Save',
        command=self.save)
        self.btn_reset = Button(self.frame, bg=bg, fg=fg2, font=font, bd=bd,
        activebackground=abg, activeforeground=afg, text='Reset',
        command=self.reset)
        self.btn_save.grid(row=15, column=1, sticky='news', padx=padx, pady=pady)
        self.btn_reset.grid(row=15, column=3, sticky='news', padx=padx, pady=pady)

    def reset(self):
        super().reset()
        self.e_name.focus_set()
    
    def save(self):
        name = self.e_name.get()
        company = self.e_company.get()
        age = self.e_age.get()
        price = self.e_price.get()
        console = self.e_console_type.get()
        stock = self.e_stock.get()
        address = self.file_address
        if name == '':
            messagebox.showerror("Error", "You must choose a name for your game.")
            self.e_name.focus_set()
            return
        try:
            price = int(price)
            if price<0:
                messagebox.showerror("Error", "price can not be negative.")
                self.e_price.focus_set()
                return
        except:
            messagebox.showerror("Error", "You must Enter digits for price")
            self.e_price.delete(0, END)
            self.e_price.focus_set()
            return
        try:
            stock = int(stock)
            if stock<0:
                messagebox.showerror("Error", "stock can not be negative.")
                self.e_stock.focus_set()
                return
        except:
            messagebox.showerror("Error", "You must Enter digits for stock")
            self.e_stock.delete(0, END)
            self.e_stock.focus_set()
            return
        if company=='':
            company=None
        if age=='':
            age=None
        if console=='':
            console=None
        if address=='':
            address=None
        result = self.connection.insert(name, price, stock, company, age, console, address)
        if result==0:
            messagebox.showinfo("Success", f"Game {name} added succesfully to shop.")
        else:
            # messagebox.showerror("Error", f"Game {name} already exsits in shop. Not added.")
            messagebox.showerror("Error", result)

    def disable(self):
        self.e_name.configure(state='disabled', disabledbackground=BG)
        self.e_company.configure(state='disabled', disabledbackground=BG)
        self.e_age.configure(state='disabled')
        self.e_price.configure(state='disabled', disabledbackground=BG)
        self.e_console_type.configure(state='disabled', disabledbackground=BG)
        self.e_stock.configure(state='disabled', disabledbackground=BG)
        self.e_address.configure(state='disabled')
        self.btn_reset.configure(state='disabled')
        self.btn_save.configure(state='disabled')

    def enable(self):
        self.e_name.configure(state='normal')
        self.e_company.configure(state='normal')
        self.e_age.configure(state='readonly')
        self.e_price.configure(state='normal')
        self.e_console_type.configure(state='normal')
        self.e_stock.configure(state='normal')
        self.e_address.configure(state='normal')
        self.btn_reset.configure(state='normal')
        self.btn_save.configure(state='normal')


class UpdateGame(AddGame):
    def __init__(self, root, connection: MyConeection, bg='#333333', fg='orange', fg2='orange', text="Game Info", font=('Times', '20'), bd=1, labelanchor='n', relief='raised', abg="orange", afg="#333333", padx=5, pady=5):
        super().__init__(root, connection, bg, fg, fg2, text, font, bd, labelanchor, relief, abg, afg, padx, pady)
        self.e_old = Entry(self.frame, bg=bg, fg=fg2, font=font, bd=bd, insertbackground=fg2)
        self.btn_search = Button(self.frame, bg=bg, fg=fg2, font=font, bd=bd, activebackground=abg, activeforeground=afg, text='Search this game',command=self.search)
        self.btn_save.config(text='Update', command=self.update)
        self.e_old.grid(row=0, column=3)
        self.btn_search.grid(row=0, column=1)
    
    def search(self):
        old_name = self.e_old.get().strip()
        info = self.connection.get(old_name)
        print(info)
        if info in [(), None]:
            self.disable()
        else:
            self.enable()
            self.e_name.delete(0, END)
            self.e_company.delete(0, END)
            self.e_price.delete(0, END)
            self.e_console_type.delete(0, END)
            self.e_stock.delete(0, END)
            self.file_address=None
            self.set_picture()
            self.e_age.config(state='normal')
            self.e_age.delete(0, END)
            self.e_age.config(state='readonly')
            self.e_name.insert(0, info[1])
            if info[2] != None:
                self.e_company.insert(0, info[2])
            if info[3] != None:
                self.e_age.config(state='normal')
                self.e_age.insert(0, info[3])
                self.e_age.config(state='readonly')
            self.e_price.insert(0, info[4])
            if info[5] != None:
                self.e_console_type.insert(0, info[5])
            self.e_stock.insert(0, info[6])
            if info[7] != None:
                self.file_address=info[7]
                self.set_picture()
        
    def update(self):
        name = self.e_name.get()
        company = self.e_company.get()
        age = self.e_age.get()
        price = self.e_price.get()
        console = self.e_console_type.get()
        stock = self.e_stock.get()
        address = self.file_address
        old_name = self.e_old.get()
        if name == '':
            messagebox.showerror("Error", "You can not update name to nothing.")
            self.e_name.focus_set()
            return
        try:
            price = int(price)
            if price<0:
                messagebox.showerror("Error", "price can not be negative.")
                self.e_price.focus_set()
                return
        except:
            messagebox.showerror("Error", "You must Enter digits for price")
            self.e_price.delete(0, END)
            self.e_price.focus_set()
            return
        try:
            stock = int(stock)
            if stock<0:
                messagebox.showerror("Error", "stock can not be negative.")
                self.e_stock.focus_set()
                return
        except:
            messagebox.showerror("Error", "You must Enter digits for stock")
            self.e_stock.delete(0, END)
            self.e_stock.focus_set()
            return
        if company=='':
            company=None
        if age=='':
            age=None
        if console=='':
            console=None
        if address=='':
            address=None
        result = self.connection.update(name, price, stock, old_name, company, age, console, address)
        print(result)

        # if result==0:
        #     messagebox.showinfo("Success", f"Game {name} added succesfully to shop.")
        # else:
        #     # messagebox.showerror("Error", f"Game {name} already exsits in shop. Not added.")
        #     messagebox.showerror("Error", result)


