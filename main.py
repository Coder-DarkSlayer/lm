import mysql.connector
import pickle
from getpass import getpass
import os
from datetime import datetime,timedelta
import subprocess

# Public Decorator
dec="*"*159

# Creating Necessary files nad directories
try:
    os.makedirs(os.path.join('scripts','data','log'))
    os.makedirs(os.path.join('scripts','data','doccuments'))

except Exception:
    pass


if os.path.isfile(os.path.join('scripts','data','log','log.txt'))==False:
    with open(os.path.join('scripts','data','log','log.txt'),'a') as b:
        pass

if os.path.isfile(os.path.join('scripts','data','doccuments','userInfo.bin'))==False:
    with open(os.path.join('scripts','data','doccuments','userInfo.bin'),'a') as b:
        pass


def addSU(user,host,password):
    dbi = ''
    su = ''
    access = ''
    passwd = ''

    def newDB():
        while True:
            nonlocal dbi
            dbi=input(f"Enter the Library name you will work in \n\t(Don't enter any signs except '_' & it should be Unique): ")
            nonlocal su
            su=input(f"Enter your name as SuperUser(Admin) of '{dbi}' : ")
            nonlocal access
            access = input("Is your Library 'Private' or 'Public' : ")
            nonlocal passwd
            passwd = input("Enter the password of Library : ")
            
            try:
                mydb=mysql.connector.connect(
                    host=host,
                    user=user,
                    password=password
                )
                cur=mydb.cursor()
                cur.execute(f"create database {dbi}")
                mydb.commit()
                
                if mydb.is_connected():
                    print(f"Process Complete!!!")
                    break
                else:
                    mydb.rollback()
                    newDB()

            except Exception as e:
                mydb.rollback()
                print(f"Try Again!!! ERROR: {format(e)}\n")

    def existingDB():
        while True:
            nonlocal dbi
            dbi=input(f"Enter the Library name you will work in \n\t(Don't enter any signs except '_' & it should be Unique): ")
            nonlocal su
            su=input("Enter your name as SuperUser(Admin) : ")
            nonlocal access
            access = input("Is your Library Private or Public : ")
            nonlocal passwd
            passwd = input(f"Enter the password of {dbi} : ")

            try:
                mydb=mysql.connector.connect(
                    host=host,
                    user=user,
                    password=password
                )
                cur=mydb.cursor()
                query=cur.execute(f"use {dbi}")
                mydb.commit()
                if mydb.is_connected():
                    print(f"Process Complete!!!")
                    break
                else:
                    mydb.rollback()
                    existingDB()

            except Exception as e:
                mydb.rollback()
                print(f"Try Again!!! ERROR: {format(e)}\n")

    def createTab():
        while True:
            
            try:
                mydb=mysql.connector.connect(
                    host=host,
                    user=user,
                    password=password,
                    database=dbi
                )
                cur=mydb.cursor()
                start1=cur.execute(f"""create table BOOKS(S_NO INT NOT NULL AUTO_INCREMENT,BOOK_ID int not null,
                BOOK_NAME varchar(155) not null,AUTHOR varchar(55) not null,GENRE varchar(255) not null,
                RATED varchar(7) not null,SECTION varchar(55) not null,
                DATE_ADDED date not null,ENTRY_DATE timestamp not null default current_timestamp,primary key(BOOK_ID),unique key(S_NO))""")
                start2=cur.execute(f'''create table USERS(S_NO int not null auto_increment,USER_ID int not null,USER_F_NAME varchar(55) not null,
                USER_L_NAME varchar(55) not null,AGE tinyint not null,GENDER char(1) not null,MAIL varchar(55) not null,
                PHONE_NO varchar(15) not null,NO_OF_ISSUES int not null default 0,DATE_JOINED date not null,
                ADDRESS varchar(200) not null,ENTRY_DATE timestamp not null default current_timestamp,UNIQUE KEY(S_NO), PRIMARY KEY(USER_ID))''')
                start3=cur.execute(f'''create table ISSUES(S_NO int not null auto_increment,BOOK_ID int not null,
                USER_ID int not null,GENDER char(1) not null,MAIL varchar(100) not null,
                PHONE_NO varchar(15) not null,DATE_ISSUED date not null,ISSUE_COMPLETE varchar(3) not null default 'NO',
                DATE_GIVEN date,NOTIFIED tinyint not null default 0,UNIQUE KEY(S_NO),ENTRY_DATE timestamp not null default current_timestamp,
                CONSTRAINT booklink FOREIGN KEY (BOOK_ID) REFERENCES BOOKS(BOOK_ID),
                CONSTRAINT userlink FOREIGN KEY (USER_ID) REFERENCES USERS(USER_ID))''')
                mydb.commit()
                
                if mydb.is_connected():
                    break
                else:
                    mydb.rollback()
                    createTab()

            except mysql.connector.Error as e:
                mydb.rollback()
                print(f"\nTry Again!!! ERROR: {format(e)}\n")

    def fillSU(dbi, su , passwd , access , extra):
        try:
            mydb = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database = 'SUPERUSER'
            )

            cursor = mydb.cursor()
            cursor.execute(f"""insert into SUPERUSERS(LIBRARY_NAME,SU,AVAILABILITY,LIBRARY_PASSWORD,ACCESORY)
                            values("{dbi}","{su}","{access.capitalize()}","{passwd}","{extra}")""")
            mydb.commit()

            if mydb.is_connected():
                pass

        except Exception as e:
            mydb.rollback()
            print(f"Try Again!!! ERROR: {format(e)}")


    s=input("If you already have a database for Library enter 'yes' :")
    if s.lower()=='yes':
        n=input("Make sure that database is empty.")
        existingDB()
    else:
        newDB()


    createTab()

    no_of_days=int(input("\nHow much days you want allow book issue :"))
    
    def val():
        while True:
            try:
                global fine
                fine=int(input(f"Enter only Fine/day when {no_of_days} have passed :"))
                break
            except ValueError:
                print("Enter amount only not Currency!!!\n")
    val()
    finetype=input("Enter the Fine's Currency only!!! :")

    fillSU(dbi , su , passwd , access , str( str(no_of_days) + ' ' + str(fine) + ' ' + str(finetype) ))

    m=input(f"Hmmm... so, I guess That's it Good Luck!!....Scott signing off...\n")


def lmsIntro():
    dbh = ''
    dbusr = ''
    dbpwd = ''

    q=input("Umm... Hello Welcome to LMS (Library Management System).")

    w=input(f"Well... I guess you opened this program for first time,\nYou can call me \"Scott\", lemme settle and Explain the program for you.")

    
    z=input("Please Close Program If you enter something wrong and Open again or try Reset Option!!!")

    k=input("You can stop the program anytime by pressing 'Ctrl+C' so lets go!\n")

    def loopLogin():
        while True:
            try:
                nonlocal dbusr
                dbusr=input("Enter the User: ")
                nonlocal dbh
                dbh=input("Enter the Host of Database : ")
                nonlocal dbpwd
                dbpwd=getpass(prompt=f"Enter Password of Your User.\n\t[NOTE]: Password Will be hidden :")

                mydb=mysql.connector.connect(
                        host=dbh,
                        user=dbusr,
                        password=dbpwd,
                        database = 'performance_schema'
                    )

                if mydb.is_connected():
                    print(f"You're logged in!!!")
                    break
                else:
                    loopLogin()
            except Exception as e:
                print(f"Try Again!!! ERROR: {format(e)}")

    def SuperUser():
            try:
                mydb=mysql.connector.connect(
                    host=dbh,
                    user=dbusr,
                    password=dbpwd
                )
                cur=mydb.cursor()
                cur.execute(f"create database SUPERUSER")

                mydb.commit()

                if mydb.is_connected():
                    pass

                try:
                    datadb=mysql.connector.connect(
                        host=dbh,
                        user=dbusr,
                        password=dbpwd,
                        database = 'SUPERUSER'
                    )

                    cursor=datadb.cursor()
                    cursor.execute("""create table SUPERUSERS(
                            LIBRARY_NAME varchar(155) not null,SU varchar(55) not null,AVAILABILITY varchar(10) not null,
                            LIBRARY_PASSWORD varchar(30) not null,DATE_ADDED timestamp not null default current_timestamp,
                            ACCESORY varchar(200) not null,primary key(LIBRARY_NAME))""")
                    datadb.commit()
                    print()

                except Exception as k:
                    datadb.rollback()
                    print(f"Try Again!!! ERROR: {format(k)}")

            except Exception as e:
                mydb.rollback()
                print(f"Try Again!!! ERROR: {format(e)}")

    loopLogin()

    SuperUser()

    save_data={"dbms details":
                            {"user":dbusr,"host":dbh,"password":dbpwd}
                }
    
    with open(os.path.join('scripts','data','doccuments','userInfo.bin'),'wb')as f:
        pickle.dump(save_data,f)

    addSU(dbusr,dbh,dbpwd)


##################################################################################################################


try:
    with open(os.path.join('scripts','data','doccuments','userInfo.bin'),'rb')as e:
        login = pickle.load(e)

        User=login["dbms details"]["user"]
        Host=login["dbms details"]["host"]
        Password=login["dbms details"]["password"]

        link = mysql.connector.connect(
            host = Host,
            user = User,
            password = Password
        )
        cur = link.cursor()
        cur.execute("select * from SUPERUSER.SUPERUSERS")
        x = cur.fetchall()

except Exception:
    lmsIntro()
    with open(os.path.join('scripts','data','doccuments','userInfo.bin'),'rb')as e:
        login = pickle.load(e)

        User=login["dbms details"]["user"]
        Host=login["dbms details"]["host"]
        Password=login["dbms details"]["password"]


##################################################################################################################

# Gives input In split
def capital(inputStr):
    inputStr=inputStr.split(',')
    inputStr=list(map(lambda x:x.title(),inputStr))
    inputStr=','.join(inputStr)
    return inputStr

# Login Function Per user
def loopLogin(syshost,sysuser,syspwd):
    i = 3
    while i > 0:
        try:
            global syslib
            syslib=input("Enter the Library name: ")
            
            mydb=mysql.connector.connect(
                    host=syshost,
                    user=sysuser,
                    password=syspwd,
                    database='SUPERUSER'
                )
            
            cursor = mydb.cursor()
            cursor.execute(f"""select LIBRARY_NAME,SU,AVAILABILITY,ACCESORY,LIBRARY_PASSWORD from SUPERUSERS where LIBRARY_NAME = '{syslib}'""")

            libinfo = cursor.fetchall()[0]
            
            if mydb.is_connected():
                syslib=libinfo[0]

                global syspref
                syspref=libinfo[2]

                global libpass
                libpass = libinfo[4]

                global fine_amount , currency , days
                fine_amount , currency , days = libinfo[3].split()[1] , libinfo[3].split()[2] , libinfo[3].split()[0]

                if syspref.lower() == 'private':
                    libp = input(f"'{syslib}' is Private Please enter the password :")
                    if libp== libpass:
                        break
                    else:
                        print("Wrong Pssword!!!\n")
        
        except Exception as e:
            print(f"User doesn't Exists!!!")
            i -= 1
    else:
        k = input("You Have Made Wrong Input thrice Program is Closing!!!")
        exit()

# Fine of user
def fine(syshost,sysuser,syspwd,sysdb,days_count,fine_amount,currency):
    try:
        to_find_date=(datetime.now()-timedelta(days=days_count)).date()
        connection=mysql.connector.connect(host=syshost,database=sysdb,user=sysuser,password=syspwd)
        cur=connection.cursor()
        cur.execute(f"""select i.BOOK_ID,i.USER_ID,b.BOOK_NAME,i.DATE_ISSUED,i.MAIL,i.PHONE_NO from ISSUES i inner join BOOKS b on i.BOOK_ID=b.BOOK_ID where i.DATE_ISSUED<=date('{to_find_date}') and i.ISSUE_COMPLETE='NO' and i.NOTIFIED<5""")
        res=cur.fetchall()

        if len(res)!=0:
            try:
                subprocess.call(["ffplay","-nodisp","-autoexit","notifications\\notification.wav"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            except Exception:
                pass
            for i in res:
                print(dec)
                print(f"""[NOTIFICATION]: Book ID: '{i[0]}', Book: '{i[2]}' issued by User ID: '{i[1]}' has passed issue limit.\n\t\t Contact User on '{i[4]}' | '{i[5]}'.\n\t\t User has a fine of '{fine_amount*((to_find_date-i[3]).days)} {currency}'""")
                try:
                    connection1=mysql.connector.connect(host=syshost,database=sysdb,user=sysuser,password=syspwd)
                    cur=connection1.cursor()
                    cur.execute(f"update ISSUES set NOTIFIED = NOTIFIED + 1 where BOOK_ID={i[0]} and USER_ID={i[1]}")
                    connection1.commit()
                except mysql.connector.Error:
                    pass
            print(dec)
        else:
            pass
    except Exception:
        pass

# Creating log files
def log(fxn):
    with open(os.path.join('scripts','data','log','log.txt'),'a') as f:
        time_and_zone=datetime.now().strftime("%d/%m/%y %I:%M:%S %p")
        f.write(f"{fxn} at {time_and_zone}\n")
        f.close()

# Adds Book to Database
def addBook(syshost,sysuser,syspwd,sysdb,fxn,bookInfoList): 

    try: 
        connection = mysql.connector.connect(host=syshost,database=sysdb,user=sysuser,password=syspwd) 
        insert_query = (f"""insert into BOOKS(BOOK_ID,BOOK_NAME,AUTHOR,GENRE,RATED,SECTION,DATE_ADDED)
        values({bookInfoList[0]},"{bookInfoList[1]}","{bookInfoList[2].replace(",",'/')}","{capital(bookInfoList[3])}",
        "{bookInfoList[4].upper()}","{bookInfoList[5].capitalize()}",str_to_date("{bookInfoList[6]}",'%Y-%m-%d'))""") 
        cursor = connection.cursor() 
        result = cursor.execute(insert_query) 
        connection.commit() 

        if connection.is_connected:
            print ("Record inserted successfully into Book Info. table.")
            log(f"Book ID: {bookInfoList[0]}, Name: '{bookInfoList[1]}' was added")
    except mysql.connector.Error as e: 
        connection.rollback()
        print(f"ERROR: \n\t{format(e)}\n") 
    finally:
        cursor.close()
        connection.close() 
        print("MySQL connection is closed")
        res=input()
        fxn()

# Shows Book Details
def showBookDetails(syshost,sysuser,syspwd,sysdb,BookID,BookName,fxn):
    
    try: 
        connection = mysql.connector.connect(host=syshost,database=sysdb,user=sysuser,password=syspwd) 
        cur=connection.cursor()
        cur.execute(f"select BOOK_NAME,BOOK_ID,AUTHOR,GENRE,RATED,SECTION,DATE_ADDED from BOOKS where BOOK_ID={BookID}")
        result=cur.fetchall()
        if len(result)==0:
            print("No such Book's Present or Wrong BOOK ID!!!")
        else:
            print (f"""\n*******DETAILS OF BOOK*******\n\tBook's name is '{result[0][0]}'.\n\tBook's ID is '{result[0][1]}'.\n\tWritten by '{result[0][2]}'.\n\tConatining Genres '{result[0][3]}'.\n\tIt's '{result[0][4]}' Rated.\n\tPresent in '{result[0][5]}' Section.\n\tCame here on '{result[0][6]}'.\n""")
            log(f"Book ID: {BookID} details were viewed")
            
    except mysql.connector.Error as e: 
        connection.rollback()
        try: 
            connection = mysql.connector.connect(host=syshost,database=sysdb,user=sysuser,password=syspwd) 
            cur=connection.cursor()
            cur.execute(f"select BOOK_NAME,BOOK_ID,AUTHOR,GENRE,RATED,SECTION,DATE_ADDED from BOOKS where BOOK_ID={BookID} and lower(BOOK_NAME) = '{BookName.lower()}'")
            result=cur.fetchall()
            
            print (f"""\t***DETAILS OF BOOK***\n\tBook's name is '{result[0][0]}'.\n\tBook's ID is '{result[0][1]}'.\n\tWritten by '{result[0][2]}'.\n\tConatining Genres '{result[0][3]}'.\n\tIt's '{result[0][4]}' Rated.\n\tPresent in '{result[0][5]}' Section.\n\tCame here on '{result[0][6]}'.\n""")
            log(f"Book ID: {BookID} details were viewed")
                
        except mysql.connector.Error as e: 
            connection.rollback()
            print(f"ERROR: {format(e)}\n\tTRY AGAIN!!!")
    finally:
        cur.close()
        connection.close() 
        print("MySQL connection is closed")
        res=input() 
        fxn()

# Remove Book from Database
def removeBook(syshost,sysuser,syspwd,sysdb,BookID,BookName,fxn): 
    
    try: 
        connection = mysql.connector.connect(host=syshost,database=sysdb,user=sysuser,password=syspwd) 
        insert_query = (f"""delete from BOOKS where BOOK_ID={BookID}""") 
        cursor = connection.cursor() 
        result = cursor.execute(insert_query) 
        connection.commit() 

        if connection.is_connected:
            print ("Record deleted successfully from Book Info. table.")
            log(f"Book ID: {BookID} named {BookName} was removed")
            
    except mysql.connector.Error: 
        connection.rollback()
        try: 
            connection = mysql.connector.connect(host=syshost,database=sysdb,user=sysuser,password=syspwd) 
            insert_query = (f"""delete from BOOKS where BOOK_ID={BookID},BOOK_NAME='{BookName}'""") 
            cursor = connection.cursor() 
            result = cursor.execute(insert_query) 
            connection.commit() 

            if connection.is_connected:
                print ("Record deleted successfully from Book Info. table.")
                log(f"Book ID: {BookID} named {BookName} was removed")
                
        except mysql.connector.Error as e: 
            connection.rollback()
            print(f"ERROR: {format(e)}\n\tTRY AGAIN!!!") 
    finally:
        cursor.close()
        connection.close() 
        print("MySQL connection is closed")
        res=input()
        fxn()

# Renames the Book
def changeBookName(syshost,sysuser,syspwd,sysdb,BookID,BookName,BookNewName,fxn): 
    
    try: 
        connection = mysql.connector.connect(host=syshost,database=sysdb,user=sysuser,password=syspwd) 
        insert_query = (f"""update BOOKS set BOOK_NAME="{BookNewName}" where BOOK_ID={BookID}""") 
        cursor = connection.cursor() 
        result = cursor.execute(insert_query) 
        connection.commit() 

        if connection.is_connected:
            print ("Record updated successfully into Book Info. table.")
            log(f"Book ID: {BookID} was renamed {BookNewName} from {BookName}")
            
    except mysql.connector.Error as e: 
        connection.rollback()
        try: 
            connection = mysql.connector.connect(host=syshost,database=sysdb,user=sysuser,password=syspwd) 
            insert_query = (f"""update BOOKS set BOOK_NAME="{BookNewName}" where BOOK_ID={BookID} and lower(BOOK_NAME)='{BookName.lower()}'""") 
            cursor = connection.cursor() 
            result = cursor.execute(insert_query) 
            connection.commit() 

            if connection.is_connected:
                print ("Record updated successfully into Book Info. table.")
                log(f"Book ID: {BookID} was renamed {BookNewName} from {BookName}")
                
        except mysql.connector.Error as e: 
            connection.rollback()
            print(f"ERROR: {format(e)}\n\tTRY AGAIN!!!") 
    finally:
        cursor.close()
        connection.close() 
        print("MySQL connection is closed") 
        res=input()
        fxn()

# Modifies Book Info
def modifyBookDetails(syshost,sysuser,syspwd,sysdb,fxn,bookInfoList): 
    
    try: 
        connection = mysql.connector.connect(host=syshost,database=sysdb,user=sysuser,password=syspwd) 
        insert_query = (f"""update BOOKS set BOOK_NAME="{bookInfoList[1]}",AUTHOR="{bookInfoList[2]}",GENRE="{capital(bookInfoList[3])}",
        RATED="{bookInfoList[4].upper()}",SECTION="{bookInfoList[5]}",DATE_ADDED=str_to_date("{bookInfoList[6]}",'%Y-%m-%d')
            where BOOK_ID={bookInfoList[0]}""") 

        cursor = connection.cursor() 
        result = cursor.execute(insert_query) 
        connection.commit() 

        if connection.is_connected:
            print ("Record modified successfully into Book Info. table.") 
            log(f"Book ID: {bookInfoList[0]} details were modified")
    except mysql.connector.Error as e: 
        connection.rollback()
        print(f"ERROR: {format(e)}") 
    finally:
        cursor.close()
        connection.close() 
        print("MySQL connection is closed")
        res=input()
        fxn()

# Changes Book's ID
def changeBookID(syshost,sysuser,syspwd,sysdb,BookID,BookNewID,BookName,fxn): 
    
    try: 
        connection = mysql.connector.connect(host=syshost,database=sysdb,user=sysuser,password=syspwd) 
        insert_query = (f"""update BOOKS set BOOK_ID={BookNewID} where BOOK_ID={BookID}""") 
        cursor = connection.cursor() 
        result = cursor.execute(insert_query) 
        connection.commit() 

        if connection.is_connected:
            print ("Record updated successfully into Book Info. table.")
            log(f"Book ID: {BookID} was modified to {BookNewID}")

    except mysql.connector.Error as e: 
        connection.rollback()
        try: 
            connection = mysql.connector.connect(host=syshost,database=sysdb,user=sysuser,password=syspwd) 
            insert_query = (f"""update BOOKS set BOOK_ID={BookNewID} where lower(BOOK_NAME) = '{BookName.lower()}',BOOK_ID={BookID}""") 
            cursor = connection.cursor() 
            result = cursor.execute(insert_query) 
            connection.commit() 

            if connection.is_connected:
                print ("Record updated successfully into Book Info. table.")
                log(f"Book ID: {BookID} was modified to {BookNewID}")
                
        except mysql.connector.Error as e: 
            connection.rollback()
            print(f"ERROR: {format(e)}\n\tTRY AGAIN!!!") 
    finally:
        cursor.close()
        connection.close() 
        print("MySQL connection is closed")
        res=input()
        fxn()

# Searches Book in Database
def searchBookName(syshost,sysuser,syspwd,sysdb,BookName,fxn):
    
    try:
        connection=mysql.connector.connect(host=syshost,database=sysdb,user=sysuser,password=syspwd)
        cur=connection.cursor()
        cur.execute(f"select BOOK_ID,BOOK_NAME from BOOKS where  lower(BOOK_NAME)='{BookName.lower()}'")
        res=cur.fetchall()
        if len(res)!=0:
            print(f"""\n[FOUND]: Review...""")
            for n in res:
                print(f"\t\tBook ID :{n[0]}")
            print("to get Desired Book\n")
            
        else:
            print("\nNothing Found Try again!!!....")

    except Exception as e:
        print(f"Search Interruped ERROR:\n\t{format(e)}")

    finally:
        cur.close()
        connection.close() 
        print("MySQL connection is closed")
        res=input()
        fxn()

# find Books According to Genre
def findGenreBooks(syshost,sysuser,syspwd,sysdb,Genre,fxn):
    try:
        connection = mysql.connector.connect(host=syshost,database=sysdb,user=sysuser,password=syspwd)
        cursor = connection.cursor()
        cursor.execute(f"""select GENRE,BOOK_ID from BOOKS where lower(GENRE) like lower("%{Genre}%")""")
        result=cursor.fetchall()

        if len(result)==0:
            print("Nothing Found!!!")
        else:
            print("Found These books:\n")
            for i in result:
                print(f"\t\tBook ID :{i[1]}")
            print("That's All...\n")
        log(f"{Genre.capitalize()} Genre was searched ")

    except Exception as e:
        print(f"ERROR: {format(e)}\n\tTRY AGAIN!!!") 
    finally:
        cursor.close()
        connection.close() 
        print("MySQL connection is closed") 
        res=input()
        fxn()

# Adds User to Database
def addUser(syshost,sysuser,syspwd,sysdb,fxn,userInfoList):

    try: 
        connection = mysql.connector.connect(host=syshost,database=sysdb,user=sysuser,password=syspwd) 
        insert_query = (f"""insert into USERS(USER_ID,USER_F_NAME,USER_L_NAME,AGE,GENDER,MAIL,DATE_JOINED,ADDRESS,PHONE_NO)
        values({userInfoList[0]},"{userInfoList[1].capitalize()}","{userInfoList[2].capitalize()}",
        {userInfoList[3]},"{str(userInfoList[4]).upper()}","{userInfoList[5]}",
        str_to_date("{userInfoList[6]}",'%Y-%m-%d'),"{userInfoList[7]}",'{userInfoList[8]}')""") 
        cursor = connection.cursor() 
        cursor.execute(insert_query)
        connection.commit() 

        if connection.is_connected:
            print ("Record inserted successfully into User Info. table.")
            log(f"User ID: {userInfoList[0]}, Name: '{userInfoList[1].capitalize()} {userInfoList[8].capitalize()}' was added")
    except mysql.connector.Error as e: 
        connection.rollback()
        print(f"ERROR: {format(e)}") 
    finally:
        cursor.close()
        connection.close() 
        print("MySQL connection is closed") 
        res=input()
        fxn()

# Shows User Info
def showUserDetails(syshost,sysuser,syspwd,sysdb,UserID,UserFirstName,UserLastName,fxn):
    
    try: 
        connection = mysql.connector.connect(host=syshost,database=sysdb,user=sysuser,password=syspwd)
        cur=connection.cursor()
        cur.execute(f"select USER_F_NAME,USER_L_NAME,USER_ID,AGE,GENDER,MAIL,PHONE_NO,NO_OF_ISSUES,DATE_JOINED,ADDRESS from USERS where USER_ID={UserID}")
        result=cur.fetchall()

        if len(result)==0:
            print("No such User's Present or Wrong USER ID!!!")
        else:
            print (f"""\n\t******DETAILS OF USER******\n\tUser's name is '{result[0][0]} {result[0][1]}'.\n\tUser's ID is '{result[0][2]}'.\n\tAge is '{result[0][3]}' Years.\n\tGender '{result[0][4]}'.\n\tUser's e-Mail '{result[0][5]}'.\n\tPhone Number is '{result[0][6]}'.\n\tHas issued '{result[0][7]}' Books.\n\tJoined on '{result[0][8]}'.\n\tAddress is '{result[0][9]}'.""")
            log(f"User ID: {UserID} details were viewed")
            
    except mysql.connector.Error: 
        connection.rollback()
        try: 
            connection = mysql.connector.connect(host=syshost,database=sysdb,user=sysuser,password=syspwd) 
            cur=connection.cursor()
            cur.execute(f"""select USER_F_NAME,USER_L_NAME,USER_ID,AGE,GENDER,MAIL,PHONE_NO,NO_OF_ISSUES,DATE_JOINED,ADDRESS from USERS where USER_ID={UserID},lower(USER_F_NAME)="{UserFirstName.lower()}",lower(USER_L_NAME)='{UserLastName.lower()}'""")
            result=cur.fetchall() 
            
            print (f"""\t***DETAILS OF USER***\n\tUser's name is '{result[0][0]} {result[0][1]}'.\n\tUser's ID is '{result[0][2]}'.\n\tAge is '{result[0][3]}' Years.\n\tGender '{result[0][4]}'.\n\tUser's e-Mail '{result[0][5]}'.\n\tPhone Number is '{result[0][6]}'.\n\tHas issued '{result[0][7]}' Books.\n\tJoined on '{result[0][8]}'.\n\tAddress is '{result[0][9]}'.""")
            log(f"User ID: {UserID} details were viewed")
                
        except mysql.connector.Error as e: 
            connection.rollback()
            print(f"ERROR: {format(e)}\n\tTRY AGAIN!!!") 
    finally:
        cur.close()
        connection.close() 
        print("MySQL connection is closed") 
        res=input()
        fxn()

# Remove User from Database
def removeUser(syshost,sysuser,syspwd,sysdb,UserID,UserFirstName,UserLastName,fxn): 
        
    try: 
        connection = mysql.connector.connect(host=syshost,database=sysdb,user=sysuser,password=syspwd) 
        insert_query = (f"""delete from USERS where USER_ID={UserID}""") 
        cursor = connection.cursor() 
        result = cursor.execute(insert_query) 
        connection.commit() 

        if connection.is_connected:
            print ("Record deleted successfully from User Info. table.")
            log(f"User ID: {UserID} was removed")
            
    except mysql.connector.Error: 
        connection.rollback()
        try: 
            connection = mysql.connector.connect(host=syshost,database=sysdb,user=sysuser,password=syspwd) 
            insert_query = (f"""delete from USERS where USER_ID={UserID},lower(USER_F_NAME)='{UserFirstName.lower()}',lower(USER_L_NAME)='{UserLastName.lower()}'""") 
            cursor = connection.cursor() 
            result = cursor.execute(insert_query) 
            connection.commit() 

            if connection.is_connected:
                print ("Record deleted successfully from User Info. table.")
                log(f"User ID: {UserID} was removed")
                
        except mysql.connector.Error as e: 
            connection.rollback()
            print(f"ERROR: {format(e)}\n\tTRY AGAIN!!!") 
    finally:
        cursor.close()
        connection.close() 
        print("MySQL connection is closed")
        res=input()
        fxn()

# Renames the User
def changeUserName(syshost,sysuser,syspwd,sysdb,UserID,UserName,UserNewName,fxn): 
    
    try: 
        connection = mysql.connector.connect(host=syshost,database=sysdb,user=sysuser,password=syspwd) 
        insert_query = (f"""select USER_ID from USERS where USER_ID={UserID}""") 
        cursor = connection.cursor()
        cursor.execute(insert_query)
        result=cursor.fetchall()
        if len(result) ==0:
            print("User's not in Database!!!")
            fxn()
        else:
            pass
    except mysql.connector.Error:
        pass

    try: 
        connection = mysql.connector.connect(host=syshost,database=sysdb,user=sysuser,password=syspwd) 
        insert_query = (f"""update USERS set USER_F_NAME="{UserNewName[0].capitalize()}",USER_L_NAME="{UserNewName[1].capitalize()}" where USER_ID={UserID}""") 
        cursor = connection.cursor() 
        result = cursor.execute(insert_query) 
        connection.commit() 

        if connection.is_connected:
            print ("Record inserted successfully into User Info. table.")
            log(f"User ID: {UserID} was renamed '{UserNewName[0]} {UserNewName[1]}'")
            
    except mysql.connector.Error as e: 
        connection.rollback()
        try: 
            connection = mysql.connector.connect(host=syshost,database=sysdb,user=sysuser,password=syspwd) 
            insert_query = (f"""update USERS set USER_F_NAME="{UserNewName[0].capitalize()}",USER_L_NAME="{UserNewName[1].capitalize()}" where USER_ID={UserID} and USER_F_NAME='{UserName[0]}' and USER_L_NAME='{UserName[1]}'""") 
            cursor = connection.cursor() 
            result = cursor.execute(insert_query) 
            connection.commit() 

            if connection.is_connected:
                print ("Record inserted successfully into User Info. table.")
                log(f"User ID: {UserID} was renamed '{UserNewName[0]} {UserNewName[1]}'")
                
        except mysql.connector.Error as e: 
            connection.rollback()
            print(f"ERROR: {format(e)}\n\tTRY AGAIN!!!") 
    finally:
        cursor.close()
        connection.close() 
        print("MySQL connection is closed")
        res=input()
        fxn()

# Changes User's ID
def changeUserID(syshost,sysuser,syspwd,sysdb,UserID,UserNewID,fxn): 
    
    try: 
        connection = mysql.connector.connect(host=syshost,database=sysdb,user=sysuser,password=syspwd) 
        insert_query = (f"""update USERS set USER_ID={UserNewID} where USER_ID={UserID}""") 
        cursor = connection.cursor() 
        result = cursor.execute(insert_query) 
        connection.commit() 

        if connection.is_connected:
            print ("Record changed successfully from User Info. table.")
            log(f"User ID: {UserID} was modified to {UserNewID}")
            
    except mysql.connector.Error as e: 
        connection.rollback()
        print(f"ERROR: {format(e)}\n\tTRY AGAIN!!!") 
    finally:
        cursor.close()
        connection.close() 
        print("MySQL connection is closed")
        res=input()
        fxn()

# Changes User's e-Mail
def changeUserMail(syshost,sysuser,syspwd,sysdb,UserID,UserNewMail,fxn): 
    
    try: 
        connection = mysql.connector.connect(host=syshost,database=sysdb,user=sysuser,password=syspwd) 
        insert_query = (f"""update USERS set MAIL='{UserNewMail}' where USER_ID={UserID}""") 
        cursor = connection.cursor() 
        result = cursor.execute(insert_query) 
        connection.commit() 

        if connection.is_connected:
            print ("Record changed successfully from User Info. table.")
            log(f"User ID: {UserID} e-Mail was renewed {UserNewMail}")
        
    except mysql.connector.Error as e: 
        connection.rollback()
        print(f"ERROR: {format(e)}\n\tTRY AGAIN!!!") 
    finally:
        cursor.close()
        connection.close() 
        print("MySQL connection is closed")
        res=input() 
        fxn()

# Changes User's Phone No.
def changeUserPhone(syshost,sysuser,syspwd,sysdb,UserID,UserName,UserNewPhone,fxn): 
    
    try: 
        connection = mysql.connector.connect(host=syshost,database=sysdb,user=sysuser,password=syspwd) 
        insert_query = (f"""select USER_ID from USERS where USER_ID={UserID}""") 
        cursor = connection.cursor()
        cursor.execute(insert_query)
        result=cursor.fetchall()
        if len(result) ==0:
            print("User's not in Database!!!")
            fxn()
        else:
            pass
    except mysql.connector.Error:
        pass

    try: 
        connection = mysql.connector.connect(host=syshost,database=sysdb,user=sysuser,password=syspwd) 
        insert_query = (f"""update USERS set PHONE_NO='{UserNewPhone}' where USER_ID={UserID}""") 
        cursor = connection.cursor() 
        result = cursor.execute(insert_query) 
        connection.commit() 

        if connection.is_connected:
            print ("Record changed successfully from User Info. table.")
            log(f"User ID: {UserID} Phone no. was renewed {UserNewPhone}")
            
    except mysql.connector.Error as e: 
        connection.rollback()
        try: 
            connection = mysql.connector.connect(host=syshost,database=sysdb,user=sysuser,password=syspwd) 
            insert_query = (f"""update USERS set PHONE_NO='{UserNewPhone}' where USER_ID={UserID},lower(USER_F_NAME)='{UserName[0].lower()}',lower(USER_L_NAME)='{UserName[1].lower()}'""") 
            cursor = connection.cursor() 
            result = cursor.execute(insert_query) 
            connection.commit() 

            if connection.is_connected:
                print ("Record changed successfully from User Info. table.")
                log(f"User ID: {UserID} Phone no. was renewed {UserNewPhone}")
                
        except mysql.connector.Error as e: 
            connection.rollback()
            print(f"ERROR: {format(e)}\n\tTRY AGAIN!!!") 
    finally:
        cursor.close()
        connection.close() 
        print("MySQL connection is closed")
        res=input()
        fxn()

# Modifies User Info
def modifyUserDetails(syshost,sysuser,syspwd,sysdb,fxn,userInfoList): 
    
    try: 
        connection = mysql.connector.connect(host=syshost,database=sysdb,user=sysuser,password=syspwd) 
        insert_query = (f"""update USERS set USER_F_NAME="{userInfoList[1].capitalize()}",USER_L_NAME="{userInfoList[2].capitalize()}",
        AGE={userInfoList[3]},GENDER="{userInfoList[4].upper()}",MAIL="{userInfoList[5]}",
        DATE_JOINED=str_to_date("{userInfoList[6]}",'%Y-%m-%d'),ADDRESS="{userInfoList[7]}",
        PHONE_NO='{userInfoList[8]}' where USER_ID={userInfoList[0]}""") 
        cursor = connection.cursor() 
        result = cursor.execute(insert_query) 
        connection.commit() 

        if connection.is_connected:
            print ("Record modified successfully into User Info. table.") 
            log(f"User ID: {userInfoList[0]} details were modified")
    except mysql.connector.Error as e: 
        connection.rollback()
        print(f"ERROR: {format(e)}") 
    finally:
        cursor.close()
        connection.close() 
        print("MySQL connection is closed")
        res=input()
        fxn()

# Searches User in Database
def searchUser(syshost,sysuser,syspwd,sysdb,UserFirstName,UserLastName,fxn):
    
    try:
        connection=mysql.connector.connect(host=syshost,database=sysdb,user=sysuser,password=syspwd)
        cur=connection.cursor()
        cur.execute(f"""select USER_ID from USERS where lower(USER_F_NAME)='{UserFirstName.lower()}' and lower(USER_L_NAME)='{UserLastName.lower()}'""")
        res=cur.fetchall()
        if len(res)!=0:
            print()
            print(f"""[FOUND]: Review:""")
            for i in res:
                print(f"\t\tUser ID '{i[0]}'")
            print("to get Desired User.")
            print()
        else:
            print()
            print("Nothing Found Try again.....")
            print()

    except Exception as e:
        print(f"Search Interruped ERROR:\n\t{format(e)}")

    finally:
        cur.close()
        connection.close() 
        print("MySQL connection is closed")
        res=input()
        fxn()

# Adds Issue
def addIssue(syshost,sysuser,syspwd,sysdb,BookID,UserID,fxn,issueDate):  
    
    content=[]
    def getList():
        try:
            connection = mysql.connector.connect(host=syshost,database=syslib,user=sysuser,password=syspwd) 
            insert_query1 =f"select GENDER,MAIL,PHONE_NO from USERS where USER_ID={UserID}"
            cur=connection.cursor()
            cur.execute(insert_query1)
            result=cur.fetchall()
            nonlocal content
            for i in result[0]:
                content.append(i)
            if connection.is_connected:
                pass
        except mysql.connection.Error:
            print("Something's messed up in entry")
        finally:
            cur.close()
            connection.close()
    getList()

    try: 
        connection = mysql.connector.connect(host=syshost,database=sysdb,user=sysuser,password=syspwd) 
        insert_query = (f"""insert into ISSUES(BOOK_ID,USER_ID,GENDER,MAIL,PHONE_NO,DATE_ISSUED)
        values({BookID},{UserID},'{content[0]}','{content[1]}','{content[2]}',str_to_date("{issueDate}",'%Y-%m-%d'))""") 
        cursor = connection.cursor()
        cursor.execute(insert_query) 
        connection.commit() 

        if connection.is_connected:
            print ("Record inserted successfully into Issue Info. table.")
            connection1 = mysql.connector.connect(host=syshost,database=sysdb,user=sysuser,password=syspwd)
            cursor = connection1.cursor()
            cursor.execute(f"update USERS set NO_OF_ISSUES=NO_OF_ISSUES+1 where USER_ID={UserID}")
            connection1.commit()

            log(f"Book ID: {BookID} issuesd by User: {UserID} was added")


    except mysql.connector.Error as e: 
        connection.rollback()
        print(f"ERROR: {format(e)}\n\tTRY AGAIN!!!") 
    finally:
        cursor.close()
        connection.close() 
        print("MySQL connection is closed") 
        res=input()
        fxn()

# shows active issues
def showActiveIssue(syshost,sysuser,syspwd,sysdb,BookID,UserID,fxn):

    try: 
        connection = mysql.connector.connect(host=syshost,database=sysdb,user=sysuser,password=syspwd) 
        cur=connection.cursor()
        cur.execute(f"select b.BOOK_NAME,i.BOOK_ID,u.USER_F_NAME,u.USER_L_NAME,i.USER_ID,i.GENDER,i.DATE_ISSUED from ISSUES i inner join USERS u on i.USER_ID = u.USER_ID inner join BOOKS b on i.BOOK_ID = b.BOOK_ID where i.USER_ID={UserID} and i.BOOK_ID={BookID} and ISSUE_COMPLETE='NO'")
        result=cur.fetchall() 

        if len(result)==0:
            print("No such Issues had been made!!!")

        print (f"""\n\t********DETAILS OF ISSUE********\n\tBook's name is '{result[0][0]}'.\n\tBook's ID is '{result[0][1]}'.\n\tUser's Name is '{result[0][2]} {result[0][3]}'.\n\tUser's ID is '{result[0][4]}'.\n\tUser's Gender is '{result[0][5]}'.\n\tIssued on '{result[0][6]}'.\n""")
        log(f"Book ID: {BookID} issues details were viewed")
            
    except mysql.connector.Error as e: 
        connection.rollback()
        print(f"ERROR: {format(e)}\n\tTRY AGAIN!!!")
    finally:
        cur.close()
        connection.close() 
        print("MySQL connection is closed")
        res=input()
        fxn()

# shows complete issues
def showCompleteIssue(syshost,sysuser,syspwd,sysdb,BookID,UserID,fxn):

    try: 
        connection = mysql.connector.connect(host=syshost,database=sysdb,user=sysuser,password=syspwd) 
        cur=connection.cursor()
        cur.execute(f"select b.BOOK_NAME,i.BOOK_ID,u.USER_F_NAME,u.USER_L_NAME,i.USER_ID,i.GENDER,i.DATE_ISSUED,i.DATE_GIVEN from ISSUES i inner join USERS u on i.USER_ID = u.USER_ID inner join BOOKS b on i.BOOK_ID = b.BOOK_ID where i.USER_ID={UserID} and i.BOOK_ID={BookID} and i.ISSUE_COMPLETE='YES'")
        result=cur.fetchall() 

        if len(result)==0:
            print("No such Issues had been made!!!")

        print (f"""\n\t********DETAILS OF ISSUE********\n\tBook's name is '{result[0][0]}'.\n\tBook's ID is '{result[0][1]}'.\n\tUser's Name is '{result[0][2]} {result[0][3]}'.\n\tUser's ID is '{result[0][4]}'.\n\tUser's Gender is '{result[0][5]}'.\n\tIssued on '{result[0][6]}'.\n\tReturned on '{result[0][7]}'.\n""")
        log(f"Book ID: {BookID} completed issues details were viewed")
            
    except mysql.connector.Error as e: 
        connection.rollback()
        print(f"ERROR: {format(e)}\n\tTRY AGAIN!!!")
    finally:
        cur.close()
        connection.close() 
        print("MySQL connection is closed")
        res=input()
        fxn()

# Remove Issue
def removeIssue(syshost,sysuser,syspwd,sysdb,BookID,UserID,fxn,returnDate): 
        
    try: 
        connection = mysql.connector.connect(host=syshost,database=sysdb,user=sysuser,password=syspwd) 
        insert_query = (f"""update ISSUES set ISSUE_COMPLETE='YES',DATE_GIVEN=str_to_date("{returnDate}",'%Y-%m-%d') where BOOK_ID={BookID} and USER_ID={UserID}""") 
        cursor = connection.cursor() 
        cursor.execute(insert_query) 
        connection.commit() 

        if connection.is_connected:
            print ("Record Updated successfully in Issue Info. table.")
            log(f"Book ID: {BookID} issued by User: {UserID} was Complete")
            
    except mysql.connector.Error as e: 
        connection.rollback()
        print(f"ERROR: {format(e)}\n\tTRY AGAIN!!!")
    finally:
        cursor.close()
        connection.close() 
        print("MySQL connection is closed")
        res=input()
        fxn()

# Main Option screen
def MainScreen():
    optionMainScreen=input("""\n**********Chose A Activity**********
            \n\t1). Manage Books
            \n\t2). Manage Users
            \n\t3). Manage Issues
            \n\t4). Manage SuperUsers
            \n\t5). Exit\n:""")

    if optionMainScreen=='1' or optionMainScreen.lower()=='manage books':
        fine(Host,User,Password,syslib,days,fine_amount,currency)
        BookScreen()

    elif optionMainScreen=='2' or optionMainScreen.lower()=='manage users':
        fine(Host,User,Password,syslib,days,fine_amount,currency)
        UserScreen()

    elif optionMainScreen=='3' or optionMainScreen.lower()=='manage issues':
        fine(Host,User,Password,syslib,days,fine_amount,currency)
        IssueScreen()

    elif optionMainScreen=='4' or optionMainScreen.lower()=='manage superusers':
        dat = getpass(prompt=f"\nEnter Superuser Access Password (Server Password)\n\t[NOTE]: Password Will be hidden :")
        print()
        if dat == Password:
            SU(syslib)
        else:
            print("Wrong Password!!!")
            MainScreen()

    elif optionMainScreen=='5' or optionMainScreen.lower()=='exit':
        exit()

    else:
        print(f"{dec}\nPlease type activity no. or name....")
        fine(Host,User,Password,syslib,days,fine_amount,currency)
        MainScreen()

# Book option screen
def BookScreen():
    optionBookScreen=input("""**********Chose A Activity**********
            \n\t1). Show Book Details
            \n\t2). Add Book
            \n\t3). Remove Book
            \n\t4). Rename Book
            \n\t5). Modify Book
            \n\t6). Change Book ID
            \n\t7). Search Book
            \n\t8). Search Genre
            \n\t9). Go Back
            \n\t10). Exit\n:""")
            
    if optionBookScreen=='1' or optionBookScreen.lower()=='show book details':
        fine(Host,User,Password,syslib,days,fine_amount,currency)
            
        ###################################################################################

        print("Enter Details of Book to Show.") 
        book_id=input("Enter Book ID. (Not Empty!)\n\t:")
        book_name=input("Enter Book's Name. (Not Empty!)\n\t:")

        showBookDetails(Host,User,Password,syslib,book_id,book_name,MainScreen)

        ###################################################################################

    elif optionBookScreen=='2' or optionBookScreen.lower()=='add book':
        fine(Host,User,Password,syslib,days,fine_amount,currency)

        ###################################################################################

        print("Enter Details of Book") 
        book_id=input("Enter Book ID. (Not Empty!)\n\t:")

        try: 
            connection = mysql.connector.connect(host=Host,database=syslib,user=User,password=Password) 
            insert_query = (f"""select BOOK_ID from BOOKS where BOOK_ID={book_id}""") 
            cursor = connection.cursor()
            cursor.execute(insert_query)
            result=cursor.fetchall()
            if len(result) !=0:
                print("Book's Already Present Sorry!!!")
                MainScreen()
            else:
                pass
        except ValueError:
            pass

        book_name=input("Enter name to Book. (Not Empty!)\n\t:") 
        author=input("Enter Book's Author(s) Name. (Leave empty if unknown!)\n\t(If multiple Authors Enter ',' seperated):") 
        if author.strip(' ') in ['',' ']:
            author='NOT ADDED'

        genres=input("Enter Genres of book. (',' seperated)\n\t:")
        if genres.strip(' ') in ['',' ']:
            genres='-'

        rated=input("Enter the Censorship type of book. (Leave empty if None!)\n\t:")
        if rated.strip(' ') in ['',' ']:
            rated='NONE'

        section=input("Enter the Book Section Book's kept in.\n\t:")
        if section.strip(' ') in ['',' ']:
            section='NOT ASSIGNED YET'

        date_added=input("Enter Date when book arrived (Leave Empty if Today!)\n\t(FORMAT: YYYY-MM-DD):")
        if date_added.strip(' ') in ['',' ']:
            date_added=datetime.now().strftime("%Y-%m-%d")

        infoList=[book_id,book_name,author,genres,rated,section,date_added]

        addBook(Host,User,Password,syslib,MainScreen,infoList)

        ##################################################################################

    elif optionBookScreen=='3' or optionBookScreen.lower()=='remove book':
        fine(Host,User,Password,syslib,days,fine_amount,currency)

        ###################################################################################

        print("Enter Details of Book to Remove.") 
        book_id=input("Enter Book ID. (Not Empty!)\n\t:")


        try: 
            connection = mysql.connector.connect(host=Host,database=syslib,user=User,password=Password) 
            insert_query = (f"""select BOOK_ID from BOOKS where BOOK_ID={book_id}""") 
            cursor = connection.cursor()
            cursor.execute(insert_query)
            result=cursor.fetchall()
            if len(result) ==0:
                print("Book's not in Database!!!")
                MainScreen()
            else:
                pass
        except Exception:
            pass

        book_name=input("Enter Book's  Name. (Not Empty!)\n\t:")

        removeBook(Host,User,Password,syslib,book_id,book_name,MainScreen)

        ###################################################################################

    elif optionBookScreen=='4' or optionBookScreen.lower()=='rename book':
        fine(Host,User,Password,syslib,days,fine_amount,currency)

        ###################################################################################

        print("Enter Details of Book's to Rename.") 
        book_id=input("Enter Book's ID. (Not Empty!)\n\t:")


        try: 
            connection = mysql.connector.connect(host=Host,database=syslib,user=User,password=Password) 
            insert_query = (f"""select BOOK_ID from BOOKS where BOOK_ID={book_id}""") 
            cursor = connection.cursor()
            cursor.execute(insert_query)
            result=cursor.fetchall()
            if len(result) ==0:
                print("Book's Not in Database!!!")
                MainScreen()
            else:
                pass
        except Exception:
            pass

        old_book_name=input("Enter Book's Old Name. (Not Empty!)\n\t:")
        new_book_name=input("Enter Book's New Name. (Not Empty!)\n\t:")

        changeBookName(Host,User,Password,syslib,book_id,old_book_name,new_book_name,MainScreen)

        ###################################################################################

    elif optionBookScreen=='5' or optionBookScreen.lower()=='modify book':
        fine(Host,User,Password,syslib,days,fine_amount,currency)
            
        ###################################################################################

        print("Enter Details of Book to Modify") 
        book_id=input("Enter Book ID. (Not Empty!)\n\t:")


        try: 
            connection = mysql.connector.connect(host=Host,database=syslib,user=User,password=Password) 
            insert_query = (f"""select BOOK_ID from BOOKS where BOOK_ID={book_id}""") 
            cursor = connection.cursor()
            cursor.execute(insert_query)
            result=cursor.fetchall()
            if len(result) ==0:
                print("No such book in Database!!!")
                MainScreen()
            else:
                pass
        except Exception:
            pass


        book_name=input("Enter name to Book. (Not Empty!)\n\t:") 
        author=input("Enter Book's Author's Name. (Leave empty if unknown!)\n\t:") 
        if author.strip(' ') in ['',' ']:
            author='NOT ADDED'

        genre=input("Enter Genres of book. (',' seperated)\n\t:")
        if genre.strip(' ') in ['',' ']:
            genre='-'

        rated=input("Enter the Censorship type of book. (Leave empty if None!)\n\t:")
        if rated.strip(' ') in ['',' ']:
            rated='NONE'

        section=input("Enter the Book Section Book's kept in.\n\t:")
        if section.strip(' ') in ['',' ']:
            section='NOT ASSIGNED YET'

        date=input("Enter Date when book arrived (Leave Empty if Today!)\n\t(YYYY-MM-DD):")
        if date.strip(' ') in ['',' ']:
            date=datetime.now().strftime("%Y-%m-%d")

        infoList=[book_id,book_name,author,genre,rated,section,date]

        modifyBookDetails(Host,User,Password,syslib,MainScreen,infoList)

            ###################################################################################

    elif optionBookScreen=='6' or optionBookScreen.lower()=='change book id':
        fine(Host,User,Password,syslib,days,fine_amount,currency)

        ###################################################################################

        print("Enter Details of Book's to change ID.") 
        old_book_id=input("Enter Book's Current ID. (Not Empty!)\n\t:")


        try: 
            connection = mysql.connector.connect(host=Host,database=syslib,user=User,password=Password) 
            insert_query = (f"""select BOOK_ID from BOOKS where BOOK_ID={old_book_id}""") 
            cursor = connection.cursor()
            cursor.execute(insert_query)
            result=cursor.fetchall()
            if len(result) ==0:
                print("Book's not in Database!!!")
                MainScreen()
            else:
                pass
        except mysql.connector.Error:
            pass

        new_book_id=input("Enter Book's New ID. (Not Empty!)\n\t:")
        book_name=input("Enter Book's name. (Not Empty!)\n\t:")
        changeBookID(Host,User,Password,syslib,old_book_id,new_book_id,book_name,MainScreen)

        ###################################################################################

    elif optionBookScreen=='7' or optionBookScreen.lower()=='search book':
        fine(Host,User,Password,syslib,days,fine_amount,currency)

        ###################################################################################

        book_name=input("Enter Name of Book to find\n\t(Enter The name you filled) :")
        searchBookName(Host,User,Password,syslib,book_name,MainScreen)

        ###################################################################################

    elif optionBookScreen=='8' or optionBookScreen.lower()=='search genre':
        fine(Host,User,Password,syslib,days,fine_amount,currency)

        ###################################################################################

        genre=input("Enter Genre. (To Search!)\n\t:")
        findGenreBooks(Host,User,Password,syslib,genre,MainScreen)

        ###################################################################################

    elif optionBookScreen=='9' or optionBookScreen.lower()=='go back':
        fine(Host,User,Password,syslib,days,fine_amount,currency)
        MainScreen()

    elif optionBookScreen=='10' or optionBookScreen.lower()=='exit':
        exit()

    else:
        print(f"{dec}\nPlease type activity no. or name....")
        fine(Host,User,Password,syslib,days,fine_amount,currency)
        MainScreen()

# Issue option screen
def IssueScreen():
    optionIssueScreen=input("""**********Chose A Activity**********
            \n\t1). Show Active Issue Details
            \n\t2). Show Complete Issue Details
            \n\t3). Add Issue
            \n\t4). Remove Issue
            \n\t5). Go Back
            \n\t6). Exit\n:""")
            
    if optionIssueScreen=='1' or optionIssueScreen.lower()=='show active issue details':
        fine(Host,User,Password,syslib,days,fine_amount,currency)

        ###################################################################################
        print("Enter Details of Issue to Show.")
        user_id=input("Enter User ID. (Not Empty!)\n\t:")
        book_id=input("Enter Book ID. (Not Empty!)\n\t:")
        showActiveIssue(Host,User,Password,syslib,book_id,user_id,MainScreen)
            
        ###################################################################################

    elif optionIssueScreen=='2' or optionIssueScreen.lower()=='show complete issue details':
        fine(Host,User,Password,syslib,days,fine_amount,currency)
            
        ###################################################################################

        print("Enter Details of Issue to Show.")
        user_id=input("Enter User ID. (Not Empty!)\n\t:")
        book_id=input("Enter Book ID. (Not Empty!)\n\t:")
        showCompleteIssue(Host,User,Password,syslib,book_id,user_id,MainScreen)

        ###################################################################################

    elif optionIssueScreen=='3' or optionIssueScreen.lower()=='add issue':
        fine(Host,User,Password,syslib,days,fine_amount,currency)

        ###################################################################################

        print("Enter Details of Issue..") 
        book_id=input("Enter Book ID to  Issue. (Not Empty!)\n\t:")
        user_id=input("Enter User ID. (Not Empty!)\n\t:")

        try: 
            connection = mysql.connector.connect(host=Host,database=syslib,user=User,password=Password) 
            insert_query = (f"""select BOOK_ID from BOOKS where BOOK_ID={book_id}""") 
            cursor = connection.cursor()
            cursor.execute(insert_query)
            result=cursor.fetchall()
            if len(result) == 0:
                print("Book's Not Present in Database!!!")
                MainScreen()
            else:
                pass
        except Exception:
            pass

        try: 
            connection = mysql.connector.connect(host=Host,database=syslib,user=User,password=Password) 
            insert_query = (f"""select BOOK_ID from ISSUES where BOOK_ID={book_id} and ISSUE_COMPLETE='NO'""") 
            cursor = connection.cursor()
            cursor.execute(insert_query)
            result=cursor.fetchall()
            if len(result) != 0:
                print("Book's Already Issued Sorry!!!")
                MainScreen()
            else:
                pass
        except Exception:
            pass

        try: 
            connection = mysql.connector.connect(host=Host,database=syslib,user=User,password=Password) 
            insert_query = (f"""select USER_ID from USERS where USER_ID={user_id}""") 
            cursor = connection.cursor()
            cursor.execute(insert_query)
            result=cursor.fetchall()
            if len(result) ==0:
                print("User's not in Database!!!")
                MainScreen()
            else:
                pass
        except Exception:
            pass

        date=input("Enter Date when book was issued.\n\t(FORMAT: YYYY-MM-DD ; Leave empty for Today's date):")
        if len(date)==0:
            date=datetime.now().strftime("%Y-%m-%d")
        addIssue(Host,User,Password,syslib,book_id,user_id,MainScreen,date)

        ###################################################################################

    elif optionIssueScreen=='4' or optionIssueScreen.lower()=='remove issue':
        fine(Host,User,Password,syslib,days,fine_amount,currency)

        ###################################################################################

        print("Enter Details of Issue to Remove.")
        book_id=input("Enter Book's ID. (Not Empty!)\n\t:")
        user_id=input("Enter User's ID. (Not Empty!)\n\t:")

        try: 
            connection = mysql.connector.connect(host=Host,database=syslib,user=User,password=Password) 
            insert_query = (f"""select BOOK_ID from BOOKS where BOOK_ID={book_id}""") 
            cursor = connection.cursor()
            cursor.execute(insert_query)
            result=cursor.fetchall()
            if len(result) == 0:
                print("Book's Not Present in Database!!!")
                MainScreen()
            else:
                pass
        except Exception:
            pass
        try: 
            connection = mysql.connector.connect(host=Host,database=syslib,user=User,password=Password) 
            insert_query = (f"""select USER_ID from USERS where USER_ID={user_id}""") 
            cursor = connection.cursor()
            cursor.execute(insert_query)
            result=cursor.fetchall()
            if len(result) ==0:
                print("User's not in Database!!!")
                MainScreen()
            else:
                pass
        except Exception:
            pass

        try:
            connection = mysql.connector.connect(host=Host,database=syslib,user=User,password=Password) 
            insert_query = (f"""select BOOK_ID from ISSUES where BOOK_ID={book_id} and USER_ID={user_id} and ISSUE_COMPLETE='NO'""") 
            cursor = connection.cursor()
            cursor.execute(insert_query)
            result=cursor.fetchall()
            if len(result) == 0:
                print("Book's Not Issued Sorry!!!")
                MainScreen()
            else:
                pass
        except Exception:
            pass

        date=input("Enter Date when book was Returned.\n\t(FORMAT: YYYY-MM-DD ; Leave empty for Today's date):")
        if len(date)==0:
            date=datetime.now().strftime("%Y-%m-%d")
        removeIssue(Host,User,Password,syslib,book_id,user_id,MainScreen,date)

        ###################################################################################

    elif optionIssueScreen=='5' or optionIssueScreen.lower()=='go back':
        fine(Host,User,Password,syslib,days,fine_amount,currency)
        MainScreen()

    elif optionIssueScreen=='6' or optionIssueScreen.lower()=='exit':
        exit()

    else:
        print(f"{dec}\nPlease type activity no. or name....")
        fine(Host,User,Password,syslib,days,fine_amount,currency)
        MainScreen()

# User Option screen
def UserScreen():
    optionUserScreen=input("""**********Chose A Activity**********
        \n\t1). Show User Details
        \n\t2). Add User
        \n\t3). Remove User
        \n\t4). Rename User
        \n\t5). Change e-Mail
        \n\t6). Change Phone Number
        \n\t7). Modify User
        \n\t8). Change User ID
        \n\t9). Search User
        \n\t10). Go Back
        \n\t11). Exit\n:""")
        
    if optionUserScreen=='1' or optionUserScreen.lower()=='show user details':
        fine(Host,User,Password,syslib,days,fine_amount,currency)

        ###################################################################################

        print("Enter Details of User to Show.") 
        user_id=input("Enter User ID. (Not Empty!)\n\t:")

        fname=input("Enter User's First name . (Not Empty!)\n\t:")
        lname=input("Enter User's last name . (Not Empty!)\n\t:")
        showUserDetails(Host,User,Password,syslib,user_id,fname,lname,MainScreen)

        ###################################################################################

    elif optionUserScreen=='2' or optionUserScreen.lower()=='add user':
        fine(Host,User,Password,syslib,days,fine_amount,currency)

        ###################################################################################

        print("Enter Details of User") 
        user_id=input("Enter User ID. (Not Empty!)\n\t:")

        try: 
            connection = mysql.connector.connect(host=Host,database=syslib,user=User,password=Password) 
            insert_query = (f"""select USER_ID from USERS where USER_ID={user_id}""") 
            cursor = connection.cursor()
            cursor.execute(insert_query)
            result=cursor.fetchall()
            if len(result) != 0:
                print("User's Already Present Sorry!!!")
                MainScreen()
            else:
                pass
        except Exception:
            pass

        fname=input("Enter first name to User. (Not Empty!)\n\t:") 
        lname=input("Enter last name to User. (Leave empty if none)\n\t:") 
        if len(lname)==0:
            lname=' '

        try:
            age=int(input("Enter User's Age.\n\t:"))
        except Exception:
            print("Age is given in Intergers....")
            MainScreen()

        gender=input("Enter User's Gender(M/F/U).(Type only one Word)\n\t:")
        if gender.strip(' ') in ['',' ']:
            gender='-'
        elif gender.lower()=='male':
            gender='M'
        elif gender.lower()=='female':
            gender='F'
        elif gender.lower()=='undefied':
            gender='U'
        else:
            pass

        email=input("Enter the User's e-Mail. (Leave empty if None!)\n\t:")
        if email.strip(' ') in ['',' ']:
            email="NOT ADDED YET"

        date=input("Enter Date when User Joined. (Leave Empty if Today!)\n\t(FORMAT: YYYY-MM-DD):")
        if date.strip(' ') in ['',' ']:
            date=datetime.now().strftime("%Y-%m-%d")

        address=input("Enter the User's Address. (Leave empty if None!)\n\t:")
        if address.strip(' ') in ['',' ']:
            address="NOT GIVEN YET"

        phone=input("Enter the User's Phone No.\n\t:")
        if len(phone)!=10:
            print(f"Phone is Short for a phone number so it's left empty")
            phone='000-000-0000'

        infoList=[user_id,fname,lname,age,gender,email,date,address,phone]

        addUser(Host,User,Password,syslib,MainScreen,infoList)

        ###################################################################################

    elif optionUserScreen=='3' or optionUserScreen.lower()=='remove user':
        fine(Host,User,Password,syslib,days,fine_amount,currency)
        ###################################################################################

        print("Enter Details of User to Remove.") 
        user_id=input("Enter User ID. (Not Empty!)\n\t:")

        
        try: 
            connection = mysql.connector.connect(host=Host,database=syslib,user=User,password=Password) 
            insert_query = (f"""select USER_ID from USERS where USER_ID={user_id}""") 
            cursor = connection.cursor()
            cursor.execute(insert_query)
            result=cursor.fetchall()
            if len(result) ==0:
                print("User's not in Database!!!")
                MainScreen()
            else:
                pass
        except Exception:
            pass
  
        fname=input("Enter User's First Name. (Not Empty!)\n\t:")
        lname=input("Enter User's Last Name. (Leave empty if none)\n\t:")
        if len(lname)==0:
            lname=' '
        removeUser(Host,User,Password,syslib,user_id,fname,lname,MainScreen)

        ###################################################################################

    elif optionUserScreen=='4' or optionUserScreen.lower()=='rename user':
        fine(Host,User,Password,syslib,days,fine_amount,currency)
        ###################################################################################

        print("Enter Details of User's to Rename.") 
        user_id=input("Enter User's ID. (Not Empty!)\n\t:")

         
        try: 
            connection = mysql.connector.connect(host=Host,database=syslib,user=User,password=Password) 
            insert_query = (f"""select USER_ID from USERS where USER_ID={user_id}""") 
            cursor = connection.cursor()
            cursor.execute(insert_query)
            result=cursor.fetchall()
            if len(result) ==0:
                print("User's not in Database!!!")
                MainScreen()
            else:
                pass
        except mysql.connector.Error:
            pass

        old_fname=input("Enter User's current First Name. (Not Empty!)\n\t:")
        old_lname=input("Enter User's current Last Name. (Not Empty!)\n\t:")
        new_fname=input("Enter User's New First Name (Not Empty!)\n\t:")
        new_lname=input("Enter User's New Last Name (Not Empty!)\n\t:")
        changeUserName(Host,User,Password,syslib,user_id,[old_fname,old_lname],[new_fname,new_lname],MainScreen)

        ###################################################################################

    elif optionUserScreen=='5' or optionUserScreen.lower()=='change email' or optionUserScreen.lower()=='change e-mail':
        fine(Host,User,Password,syslib,days,fine_amount,currency)
        ###################################################################################

        print("Enter Details of User's to Change Mail.") 
        user_id=input("Enter User's ID. (Not Empty!)\n\t:")
         
        try: 
            connection = mysql.connector.connect(host=Host,database=syslib,user=User,password=Password) 
            insert_query = (f"""select USER_ID from USERS where USER_ID={user_id}""") 
            cursor = connection.cursor()
            cursor.execute(insert_query)
            result=cursor.fetchall()
            if len(result) ==0:
                print("User's not in Database!!!")
                MainScreen()
            else:
                pass
        except Exception:
            pass

        new_email=input("Enter new e-Mail You want to assign.  (Leave empty if None!)\n\t:")
        if new_email.strip(' ') in ['',' ']:
            new_email="NOT ADDED YET"
        changeUserMail(Host,User,Password,syslib,user_id,new_email,MainScreen)

        ###################################################################################

    elif optionUserScreen=='6' or optionUserScreen.lower()=='change phone number':
        fine(Host,User,Password,syslib,days,fine_amount,currency)

        ###################################################################################

        print("Enter Details of User's to Change Phone No...") 
        user_id=input("Enter User's ID. (Not Empty!)\n\t:")

        try: 
            connection = mysql.connector.connect(host=Host,database=syslib,user=User,password=Password) 
            insert_query = (f"""select USER_ID from USERS where USER_ID={user_id}""") 
            cursor = connection.cursor()
            cursor.execute(insert_query)
            result=cursor.fetchall()
            if len(result) ==0:
                print("User's not in Database!!!")
                MainScreen()
            else:
                pass
        except Exception:
            pass

        fname=input("Enter the First name of the User.\n\t:")
        lname=input("Enter the Last name of the User.\n\t:")
        phone=input("Enter the User's new Phone No.\n\t:")
        if len(phone)!=10:
            print(f"Phone is Short for a phone number so it's left empty")
            phone='000-000-0000'
        changeUserPhone(Host,User,Password,syslib,user_id,[fname,lname],phone,MainScreen)

        ###################################################################################

    elif optionUserScreen=='7' or optionUserScreen.lower()=='modify user':
        fine(Host,User,Password,syslib,days,fine_amount,currency)

        ###################################################################################

        print("Enter Details of User to Modify") 
        user_id=input("Enter User ID. (Current, Not Empty!)\n\t:")

        try: 
            connection = mysql.connector.connect(host=Host,database=syslib,user=User,password=Password) 
            insert_query = (f"""select USER_ID from USERS where USER_ID={user_id}""") 
            cursor = connection.cursor()
            cursor.execute(insert_query)
            result=cursor.fetchall()
            if len(result) ==0:
                print("User's not in Database!!!")
                MainScreen()
            else:
                pass
        except Exception:
            pass

        fname=input("Enter first name to User. (Not Empty!)\n\t:") 
        lname=input("Enter last name to User. (Not Empty!)\n\t:") 
        age=input("Enter User's Age. (Leave empty if unknown!)\n\t:") 
        if age.strip(' ') in ['',' ']:
            age='-'

        gender=input("Enter User's Gender(M/F/U).\n\t:")
        if gender.strip(' ') in ['',' ']:
            gender='-'
        elif gender.lower()=='male':
            gender='m'
        elif gender.lower()=='female':
            gender='f'

        email=input("Enter the User's e-Mail. (Leave empty if None!)\n\t:")
        if email.strip(' ') in ['',' ']:
            email="NOT ADDED YET"

        date=input("Enter Date when User Joined. (Leave Empty if Today!)\n\t(FORMAT: YYYY-MM-DD):")
        if date.strip(' ') in ['',' ']:
            date=datetime.now().strftime("%Y-%m-%d")

        address=input("Enter the User's Address. (Leave empty if None!)\n\t:")
        if address.strip(' ') in ['',' ']:
            address="NOT GIVEN YET"
        
        phone=input("Enter the User's Phone No.\n\t:")
        if len(phone)!=10:
            print(f"Phone is Short for a phone number so it's left empty")
            phone='000-000-0000'

        infoList=[user_id,fname,lname,age,gender,email,date,address,phone]

        modifyUserDetails(Host,User,Password,syslib,MainScreen,infoList)

        ###################################################################################

    elif optionUserScreen=='8' or optionUserScreen.lower()=='change user id':
        fine(Host,User,Password,syslib,days,fine_amount,currency)

        ###################################################################################

        print("Enter Details of User's to Change ID.") 
        user_id=input("Enter User's Old ID. (Not Empty!)\n\t:")

        try: 
            connection = mysql.connector.connect(host=Host,database=syslib,user=User,password=Password) 
            insert_query = (f"""select USER_ID from USERS where USER_ID={user_id}""") 
            cursor = connection.cursor()
            cursor.execute(insert_query)
            result=cursor.fetchall()
            if len(result) ==0:
                print("User's not in Database!!!")
                MainScreen()
            else:
                pass
        except Exception:
            pass
        
        new_user_id=input("Enter User's New ID. (Not Empty!)\n\t:")
        
        changeUserID(Host,User,Password,syslib,user_id,new_user_id,MainScreen)

        ###################################################################################

    elif optionUserScreen=='9' or optionUserScreen.lower()=='search user':
        fine(Host,User,Password,syslib,days,fine_amount,currency)

        ###################################################################################

        fname=input("Enter the First name of the User you wanna find..... \n\t:")
        lname=input("Enter the Last name of the User you wanna find..... \n\t:")
        searchUser(Host,User,Password,syslib,fname,lname,MainScreen)

        ###################################################################################

    elif optionUserScreen=='10' or optionUserScreen.lower()=='go back':
        fine(Host,User,Password,syslib,days,fine_amount,currency)
        MainScreen()

    elif optionUserScreen=='11' or optionUserScreen.lower()=='exit':
        exit()

    else:
        print(f"{dec}\nPlease type activity no. or name....")
        fine(Host,User,Password,syslib,days,fine_amount,currency)
        MainScreen()

# SuperUser Option screen
def SU(syslib):
    opt_sec=input("""**********Chose a Activity**********
        \n\t1). Show All Libraries
        \n\t2). Remove a Library
        \n\t3). Make a Library
        \n\t4). Change Library
        \n\t5). Reset Program
        \n\t6). Go Back
        \n\t7). Exit\n:""")

    if opt_sec=='1' or opt_sec.lower()=='show all libraries':

        fine(Host,User,Password,syslib,days,fine_amount,currency)
        try:
            takedb = mysql.connector.connect(
                        host=Host,
                        user=User,
                        password=Password,
                        database = 'SUPERUSER'
                    )

            cursor = takedb.cursor()
            cursor.execute("""select LIBRARY_NAME,SU,AVAILABILITY,DATE_ADDED from SUPERUSERS""")
            data = cursor.fetchall()

            for i,j in enumerate(data):
                print(f"Library {i+1} has details :\n\tName is '{j[0]}'.\n\tAdmin of library is '{j[1]}'.\n\tLibrary is '{j[2].capitalize()}'.\n\tIt was added on '{j[3]}'.\n")
        except Exception as e:
            print(f"An Error occured '{format(e)}'")     
        finally:
            MainScreen()
        
    elif opt_sec=='2' or opt_sec.lower()=='remove a library':

        fine(Host,User,Password,syslib,days,fine_amount,currency)
        try:
            libs = input("Enter Library's name to delete :")
            sure=input(f"Are you sure You want to remove the '{libs}' Database?.\n\t(yes/no):")
            confirm=input("Get Library access by password :")
            if sure.lower()=='yes' and confirm == libpass:
                mydb=mysql.connector.connect(
                        host=Host,
                        user=User,
                        password=Password,
                        database = 'SUPERUSER'
                    )
                cur=mydb.cursor()
                cur.execute(f"drop database {libs}")
                cur.execute(f"delete from SUPERUSERS where LIBRARY_NAME='{libs}'")
                mydb.commit()
                if mydb.is_connected():
                    print("Removal Complete Restart Again!!!")

                loopLogin(Host,User,Password)
                MainScreen()
                    
            else:
                print("Try Again!!!")
                MainScreen()
        except mysql.connector.Error as e:
            print(f"ERROR :{format(e)}\nTry Again!!!")
        finally:
            mydb.close()
            MainScreen()
    
    elif opt_sec=='3' or opt_sec.lower()=='make a library':

        fine(Host,User,Password,syslib,days,fine_amount,currency)
        try:
            addSU(User,Host,Password)
            MainScreen()
        except Exception as e:
            print(f"Error Occured {format(e)}")

    elif opt_sec=='4' or opt_sec.lower()=='change library':
        name = input("Enter name of the Library :")

        try:
            takedb = mysql.connector.connect(
                        host=Host,
                        user=User,
                        password=Password,
                        database = 'SUPERUSER'
                    )

            cursor = takedb.cursor()
            cursor.execute(f"""select LIBRARY_NAME,lower(AVAILABILITY),LIBRARY_PASSWORD from SUPERUSERS where LIBRARY_NAME='{name}'""")
            data = cursor.fetchall()

            if data[0][1]=='private':
                check = input(f"Enter password of {data[0][0]}")
                if data[0][2]==check:
                    syslib = data[0][0]
                    print(f"Library Changed to {syslib}")
                else:
                    print("Wrong Password!!!")
                    MainScreen()
            else:
                syslib = data[0][0]
                print(f"Library Changed to {syslib}")
                MainScreen()
            
        except Exception as e:
            print(f"An Error occured '{format(e)}'")
            MainScreen()

    elif opt_sec=='5' or opt_sec.lower()=='reset program':

        try:
            sure=input("Are you sure You want to remove all the Library Databases?.\n\t(yes/no):")
            confirm=getpass(prompt=f"\nEnter Superuser Access Password (Server Password)\n\t[NOTE]: Password Will be hidden :")
            if sure.lower()=='yes' and confirm == Password:
                print("\nWait it'll take some time.....")
                takedb = mysql.connector.connect(
                        host=Host,
                        user=User,
                        password=Password,
                        database = 'SUPERUSER'
                    )

                cursor = takedb.cursor()
                cursor.execute("""select LIBRARY_NAME from SUPERUSERS""")
                data = cursor.fetchall()

                for i in data:
                    mydb=mysql.connector.connect(
                            host=Host,
                            user=User,
                            password=Password
                        )

                    cur=mydb.cursor()
                    cur.execute(f"drop database {i[0]}")
                    mydb.commit()
                
                takedb = mysql.connector.connect(
                        host=Host,
                        user=User,
                        password=Password,
                        database = 'SUPERUSER'
                    )

                cursor = takedb.cursor()
                cursor.execute("""drop database SUPERUSER""")
                takedb.commit()

                if mydb.is_connected():
                    os.remove(os.path.join('scripts','data','doccuments','userInfo.bin'))
                    os.remove(os.path.join('scripts','data','log','log.txt'))
                    k = input("Removal Complete Restart Again!!!")
                    
            else:
                print("Try Again!!!")
                MainScreen()
        
        except mysql.connector.Error as e:
            print(f"ERROR :{format(e)}\nTry Again!!!")
        
        finally:
            mydb.close()
            MainScreen()
    
    elif opt_sec=='6' or opt_sec.lower()=='go back':

        fine(Host,User,Password,syslib,days,fine_amount,currency)
        MainScreen()
    
    elif opt_sec=='7' or opt_sec.lower()=='exit':

        exit()

    else:

        print(f"{dec}\nPlease type activity no. or name....")
        fine(Host,User,Password,syslib,days,fine_amount,currency)
        MainScreen() 

# Program execution
if __name__=="__main__":
    print(f"{dec}\n\t\t\t\t\t\t\t   WELCOME TO LIBRARY MANAGEMENT SYSTEM.\n{dec}\n")
    loopLogin(Host,User,Password)
    fine(Host,User,Password,syslib,days,fine_amount,currency)
    MainScreen()