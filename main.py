import pypyodbc

from tkinter import *
from tkinter.ttk import Treeview
from tkinter.ttk import Frame, Notebook
from tkinter import messagebox

text_format = ("DejaVu Sans", 100)
window = Tk()
window.title("test bd")
tab_control = Notebook(window)

connection = pypyodbc.connect('Driver={SQL Server};'
                              'Server=DESKTOP-S152C1O\SQLEXPRESS;'
                              'Database=test;')
cursor = connection.cursor()

def spravka():
    f = open('Справка.txt', 'r', encoding="utf-8")
    rd = f.read()
    messagebox.showinfo('Справка', ""+str(rd)+"")

tab1 = Frame(tab_control)
tab2 = Frame(tab_control)
tab_control.add(tab1, text="Покупатели")
tab_control.add(tab2, text="Покупки")
tab_control.pack(expand=1, fill='both')

menu = Menu(window)

file_item = Menu(menu)
file_item.add_command(label='Справка', command=spravka)

menu.add_cascade(label='Файл', menu=file_item)

window.config(menu=menu)

rows = ('id', 'name', 'age')
table = Treeview(tab1, show="headings")
table.grid(column=0, row=0, columnspan=5)
table["columns"] = rows
table["displaycolumns"] = rows
for head in rows:
    table.column(head, anchor=CENTER)

rows1 = ('id_iszd', 'id', 'tovar', 'date')
table1 = Treeview(tab2, show="headings")
table1.grid(column=0, row=0, columnspan=5)
table1["columns"] = rows1
table1["displaycolumns"] = rows1
for head1 in rows1:
    table1.column(head1, anchor=CENTER)

table.heading(rows[0], text="Номер")
table.heading(rows[1], text="Имя")
table.heading(rows[2], text="Возраст")

table1.heading(rows1[0], text="Номер покупки")
table1.heading(rows1[1], text="Номер покупателя")
table1.heading(rows1[2], text="Товар")
table1.heading(rows1[3], text="Дата покупки")

def update_table(table):
    table.delete(*table.get_children())
    mySQLQuery = ("""SELECT * FROM dbo.pokupat""")
    cursor.execute(mySQLQuery)
    rows = cursor.fetchall()
    for i in rows:
        table.insert('', 'end', values=(i['id'], i['name'], i['age']))

def update_table1(table1):
    table1.delete(*table1.get_children())
    mySQLQuery4 = ("""SELECT * FROM dbo.pokupka""")
    cursor.execute(mySQLQuery4)
    rows = cursor.fetchall()
    for i in rows:
        table1.insert('', 'end', values=(i['id_iszd'], i['id'], i['tovar'], i['date']))

def add_data():
    mySQLQuery1 = f"insert into dbo.pokupat(id,name,age) values (N'"+txt.get()+"',N'"+txt1.get()+"',N'"+txt2.get()+"')"
    cursor.execute(mySQLQuery1)
    connection.commit()
    update_table(table)
    txt.delete(0, 'end')
    txt1.delete(0, 'end')
    txt2.delete(0, 'end')

def del_data():
    mySQLQuery2 = f"DELETE FROM dbo.pokupat WHERE id='"+txt3.get()+"'"
    cursor.execute(mySQLQuery2)
    connection.commit()
    update_table(table)
    txt3.delete(0, 'end')

def search_data():
    table.delete(*table.get_children())
    mySQLQuery3 = f"SELECT * FROM dbo.pokupat WHERE name='"+txt4.get()+"'"
    cursor.execute(mySQLQuery3)
    rows = cursor.fetchall()
    for i in rows:
        table.insert('', 'end', values=(i['id'], i['name'], i['age']))
    connection.commit()

def restart_data():
    update_table(table)

txt = Entry(tab1, width=20)
txt.grid(column=0, row=1)

txt1 = Entry(tab1, width=20)
txt1.grid(column=1, row=1)

txt2 = Entry(tab1, width=20)
txt2.grid(column=2, row=1)

txt3 = Entry(tab1, width=20)
txt3.grid(column=0, row=2)

txt4 = Entry(tab1, width=20)
txt4.grid(column=0, row=3)

btn = Button(tab1, text="Добавить", command=add_data)
btn.grid(column=3, row=1)

btn1 = Button(tab1, text="Удалить", command=del_data)
btn1.grid(column=1, row=2)

btn2 = Button(tab1, text="Найти", command=search_data)
btn2.grid(column=1, row=3)

btn3 = Button(tab1, text="Обновить", command=restart_data)
btn3.grid(column=4, row=3)

update_table(table)
update_table1(table1)

window.mainloop()
connection.close()


