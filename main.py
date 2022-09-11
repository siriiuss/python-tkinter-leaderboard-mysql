import mysql.connector
import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox




today = datetime.datetime.now()
sqlToday = today.strftime('%Y-%m-%d')

cnx = mysql.connector.connect(
    user="",
    password="",
    host="",
    port=3306,
    ssl_ca="",
    database="league",
    ssl_disabled=False)

maincursor = cnx.cursor()


def show():
    maincursor.execute("SELECT id, player,games_played,win,kills,assists,death,last_match,last_match_date,point FROM leaderboard order by point desc;")
    records = maincursor.fetchall()
    print(records)

    for i, (id, player, games_played, win, kills, assists, death, last_match, last_match_date, point) in enumerate(records, start=1):
        listBox.insert("", "end", values=(id, player, games_played, win, kills, assists, death, last_match, last_match_date, point))

root = tk.Tk()
root.title("Scoreboard")
label = tk.Label(root, text="Scoreboard", font=("Arial", 30)).grid(row=0, columnspan=3)


cols = ('id','Player', 'GP', 'W', 'K', 'A', 'D', 'LM', 'LM Date', 'P')
listBox = ttk.Treeview(root, columns=cols, show='headings', selectmode="browse")

for col in cols:
    listBox.heading(col, text=col)
    listBox.grid(row=1, columnspan=1)
    listBox.column(col, width=80, stretch=False)

name = tk.StringVar()
games_played = tk.StringVar()
wins = tk.StringVar()
kills = tk.StringVar()
assists = tk.StringVar()
deaths = tk.StringVar()
last_match = tk.StringVar()
last_match_date = tk.StringVar()
points = tk.StringVar()
id = tk.StringVar


def addplayer(listBox):
    global name
    f=Frame(root, width=170, height=105,background="grey")
    f.place(x=725,y=50)

    l1=Label(f, text="Player name", width=10, font=("Times", 11, 'bold'))
    e1=Entry(f, textvariable=name, width=25)
    l1.place(x=5,y=5)
    e1.place(x=5,y=35)

    def insert_data():
        global name
        nonlocal e1
        name = name.get()
        insertplayer = ("INSERT INTO leaderboard "
                         "(player, register_date) "
                         "VALUES (%s, %s)")
        playercreds=(name, sqlToday)
        maincursor.execute(insertplayer, playercreds)
        cnx.commit()
        messagebox.showinfo(title="Succesfully", message="Player succesfully added")
        e1.delete(0,END)
        f.destroy()
        listBox.insert('','end',values=(id, name,0,0,0,0,0,None,None,0))

    submitbutton = tk.Button(f, text="Add", command=insert_data)
    submitbutton.configure(font=('Times', 14, 'bold'), bg='green', fg='white', width=6)
    submitbutton.place(x=5, y=60)

    cancelbutton = tk.Button(f, text="Cancel", command=f.destroy)
    cancelbutton.configure(font=('Times', 14, 'bold'), bg='red', fg='white', width=6)
    cancelbutton.place(x=90, y=60)

def deleteplayer(listBox):
    messageboxdelete = tk.messagebox.askquestion(title="Delete player", message="Are you sure from delete player?")
    if messageboxdelete == "Yes":
        selected_item = listBox.selection()[0]
        print(listBox.item(selected_item)['values'])
        uid = listBox.item(selected_item)['values'][1]
        del_query = "DELETE FROM leaderboard where player=%s"
        sel_data = (uid,)
        maincursor.execute(del_query, sel_data)
        cnx.commit()
        listBox.delete(selected_item)
        messagebox.showinfo(title="Succesfully", message="Player succesfully removed")
    else:
        pass

def updateplayer(listBox):
    curItem = listBox.focus()
    values = listBox.item(curItem, "values")
    print(values)

    f=Frame(root, width=170, height=600,background="grey")
    f.place(x=725,y=50)

    l1=Label(f, text="Player", width=12, font=("Times", 11, 'bold'))
    e1=Entry(f, textvariable=name, width=25)
    l1.place(x=5,y=5)
    e1.place(x=5,y=35)

    l2=Label(f, text="Games Played", width=12, font=("Times", 11, 'bold'))
    e2=Entry(f, textvariable=games_played, width=25)
    l2.place(x=5,y=65)
    e2.place(x=5,y=95)

    l3=Label(f, text="Wins", width=12, font=("Times", 11, 'bold'))
    e3=Entry(f, textvariable=wins, width=25)
    l3.place(x=5,y=125)
    e3.place(x=5,y=155)

    l4=Label(f, text="Kill", width=12, font=("Times", 11, 'bold'))
    e4=Entry(f, textvariable=kills, width=25)
    l4.place(x=5,y=185)
    e4.place(x=5,y=215)

    l5=Label(f, text="Assist", width=12, font=("Times", 11, 'bold'))
    e5=Entry(f, textvariable=assists, width=25)
    l5.place(x=5,y=245)
    e5.place(x=5,y=275)

    l6=Label(f, text="Death", width=12, font=("Times", 11, 'bold'))
    e6=Entry(f, textvariable=deaths, width=25)
    l6.place(x=5,y=305)
    e6.place(x=5,y=335)

    l7=Label(f, text="Last Game(1/0)", width=12, font=("Times", 11, 'bold'))
    e7=Entry(f, textvariable=last_match, width=25)
    l7.place(x=5,y=365)
    e7.place(x=5,y=395)

    l8=Label(f, text="Last Game(Date)", width=12, font=("Times", 11, 'bold'))
    e8=Entry(f, textvariable=last_match_date, width=25)
    l8.place(x=5,y=425)
    e8.place(x=5,y=455)

    l9=Label(f, text="Points", width=12, font=("Times", 11, 'bold'))
    e9=Entry(f, textvariable=points, width=25)
    l9.place(x=5,y=485)
    e9.place(x=5,y=525)

    e1.insert(0, values[1])
    e2.insert(0, values[2])
    e3.insert(0, values[3])
    e4.insert(0, values[4])
    e5.insert(0, values[5])
    e6.insert(0, values[6])
    e7.insert(0, values[7])
    e8.insert(0, values[8])
    e9.insert(0, values[9])

    def update_data():
        global name,games_played,wins,kills,assists,deaths,last_match,last_match_date,points
        nonlocal e1,e2,e3,e4,e5,e6,e7,e8,e9,curItem,values

        uname = name.get()
        ugames_played = games_played.get()
        uwins = wins.get()
        ukills = kills.get()
        uassists = assists.get()
        udeaths = deaths.get()
        ulast_match = last_match.get()
        ulast_match_date = last_match_date.get()
        upoints = points.get()
        listBox.item(curItem,values=(values[0],uname, ugames_played,uwins,ukills,uassists,udeaths,ulast_match,ulast_match_date,upoints))
        maincursor.execute(
            "UPDATE leaderboard SET player=%s, kills=%s, win=%s, point=%s, last_match=%s, last_match_date=%s, games_played=%s, assists=%s, death=%s WHERE id=%s"
            , (uname, ukills, uwins, upoints, ulast_match, ulast_match_date, ugames_played, uassists, udeaths, values[0])
        )
        cnx.commit()
        messagebox.showinfo(title="Succesfully", message="Succesfully updated")

        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)
        e5.delete(0, END)
        e6.delete(0, END)
        e7.delete(0, END)
        e8.delete(0, END)
        e9.delete(0, END)

        f.destroy()

    # def cancel():
    #     for i in listBox.selection():
    #         listBox.selection_remove(i)
    #     f.destroy()

    sendbutton = tk.Button(f, text="Update", command=update_data)
    sendbutton.configure(font=('Times', 14, 'bold'), bg='green', fg='white', width=6)
    sendbutton.place(x=10, y=555)

    # cancelbutton = tk.Button(f, text="Cancel", command=f.destroy)
    # cancelbutton.configure(font=('Times', 14, 'bold'), bg='red', fg='white', width=6)
    # cancelbutton.place(x=90, y=555)


insertbutton = tk.Button(root, text="Add", command=lambda:addplayer(listBox))
insertbutton.configure(font =('calibri', 14, 'bold'), bg='green', fg='white', width=20)
insertbutton.place(x=20,y=300)

updatebutton = tk.Button(root, text="Update", command=lambda:updateplayer(listBox))
updatebutton.configure(font =('calibri', 14, 'bold'), bg='blue', fg='white', width=20)
updatebutton.place(x=480,y=300)

deletebutton = tk.Button(root, text="Remove", command=lambda:deleteplayer(listBox))
deletebutton.configure(font =('calibri', 14, 'bold'), bg='red', fg='white', width=20)
deletebutton.place(x=250,y=300)



show()
root.geometry("900x650")
root.mainloop()


maincursor.close()
cnx.close()
