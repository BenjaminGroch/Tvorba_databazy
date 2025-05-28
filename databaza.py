import sqlite3, time, hashlib

con = sqlite3.connect('users_file.db')     #Vytvaranie suboru ak nie je, ak je tak pripajanie na subor
cur = con.cursor()                         #Vytvaranie kurzoru na pracu v subore

cur.execute('''CREATE TABLE IF NOT EXISTS users_table
                    (username text PRIMARY KEY, password text, name text, last_login time)''')  #Vytvaranie tabulky do suboru + vytvaranie stlpcov

class Users:                               
    def __init__(self):
        pass

    def vytvaranie_pouzivatelov(self):
        print("Vytvarate noveh uzivatelske konto do databazi")
        username   = input("Zadajte svoje uzivatelske meno: ")
        password   = input("Zadajte svoje uzivatelske heslo: ")
        name       = input("Zadajte svoje meno: ")
        login_time = None                                                #login time je none lebo pri vytvarani sa uzivatel neprihlasuje automaticky
        sifrovane_heslo = hashlib.sha256(password.encode()).hexdigest()  #sifrovanie zadaneho hesla
        cur.execute('INSERT OR IGNORE INTO users_table VALUES (?, ?, ?, ?)',(username,sifrovane_heslo,name,login_time))    #Ukladanie udajov do tabulky uzivatelov
        con.commit
        print("Uzivatelske konto bolo uspesne vytvorene")

    def prihlasovanie(self):
        print("Prihlasujete sa do databazi")
        username   = input("Zadajte svoje uzivatelske meno: ")
        password   = input("Zadajte svoje uzivatelske heslo: ")
        cur.execute("SELECT password FROM users_table WHERE username = ?", (username,))                             #Kontrola ci je uzivatel v databaze
        heslo_v_databaze = cur.fetchone()                                                                           #Ukladanie hesla uzivatela do premennej (na kontrolu)
        if heslo_v_databaze:                                                                                        #Ak je heslo ulozene (True)
            ulozene = heslo_v_databaze[0]                                                                           #Meni heslo na string
            if ulozene == hashlib.sha256(password.encode()).hexdigest():                                            #Ak sa heslo s databazou zhoduje s zadanim heslom
                login_time = time.strftime("%H:%M:%S", time.localtime())                                            #Uklada momentalny cas
                cur.execute("UPDATE users_table SET last_login = ? WHERE username = ?", (login_time, username))     #Meni login time na momentalny cas
                cur.execute("SELECT name FROM users_table WHERE username = ?", (username,))                         #Berie meno s databazi (aby sme mohli privytat uzivatela)
                meno = cur.fetchone()
                print(f"Vitajte {meno[0]}")                                                                         #Vyta uzivatela
                rozhodnutie = input("Chceli by ste zmenit heslo? (ak ano prosim napiste 'ano'): ")
                if rozhodnutie == 'ano':
                    nove_heslo = input("Zadajte nove heslo: ")
                    nove_zasifrovane_heslo = hashlib.sha256(nove_heslo.encode()).hexdigest()                                  #sifruje nove heslo
                    cur.execute("UPDATE users_table SET password = ? WHERE username = ?", (nove_zasifrovane_heslo, username)) #meni stare heslo na nove
                    print("Uspesne ste zmenili heslo")
            else:
                print("Zadali ste nespravne heslo")
        else:
            print(f"Uzivatel s menom: {username} neexistuje")

u1 = Users()
u1.vytvaranie_pouzivatelov()
u1.prihlasovanie()

for row in cur.execute('''SELECT * FROM users_table'''):    #Vypis tabulky do cli
    print(row)
