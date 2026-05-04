import csv,os,pickle
import mysql.connector as con
mycon=con.connect(host='localhost',user='root',passwd='piyush676829')
cur=mycon.cursor()

# --- 1. Create the Database ---
try:
    cur.execute("CREATE DATABASE IF NOT EXISTS students")
    print("Database 'students' created or already exists.")
    mycon.commit()
    mycon.close()
    
    #connecting to the created/existing databse
    mycon=con.connect(host='localhost',user='root',passwd='piyush676829',database='students')
    cur=mycon.cursor()
except con.Error as e:
    print("Failed to create database:",e)
    mycon.close()

# --- 2. Create the Table if it doesn't exist---
try:
    table='''create table if not exists student(
    Name varchar(35) not null,
    AdmNo int(5) primary key,
    RollNo int(5) not null,
    Phone bigint not null,
    Address varchar(50) not null)'''
    cur.execute(table)
    print('Table created or already exists.')
    mycon.commit()

except con.Error as e:
    print('An SQL error occured:',e)

# Function now requires the connection and cursor
def add_student(mycon,cur):
    # --- 1. Open Pickle File ---
    f=open('C://Piyush//project//student.dat','ab')
    student={}
    n=int(input('Enter the number of students you want to add: '))
    for i in range(n):
        student['Name']=input('Enter the name of the student: ')
        student['AdmNo']=int(input('Enter the admission number of the student: '))
        student['RollNo']=int(input('Enter the roll  number of the  student: '))
        student['Phone']=int(input('Enter the phone number of the  student: '))
        student['Address']=input('Enter the address of the student: ')
        
        # --- 2. Save to Pickle File ---
        pickle.dump(student,f)
        print('Student added successfully to pickle file.')
        
        # --- 3. Save to SQL Database ---
        try:
            st="INSERT INTO student (Name, AdmNo, RollNo, Phone, Address) VALUES (%s, %s, %s, %s, %s)"
            cur.execute(st, (student['Name'], student['AdmNo'], student['RollNo'], student['Phone'], student['Address']))
            print('Student added successfully to SQL database.')
            
        except con.Error as e:
            print("An SQL error occurred:", e)

    mycon.commit() # Commit all SQL changes after the loop
    f.close() # Close the pickle file

# Function now reads from the pickle file
def display_all():
    f=open('C://Piyush//project//student.dat','rb')
    try:
        student={}
        found=False
        try:
            while True:
                student=pickle.load(f)
                print(student)
                found=True
        except EOFError:
            if found==True:
                print('Displayed all students (from pickle file). ')
            else:
                print('Records not found (in pickle file). ')
    except FileNotFoundError:
        print('File not found. ')
    f.close()

# Function now reads from the pickle file
def search_student(): # We keep 'cursor' as an argument
    f=open('C://Piyush//project//student.dat','rb')
    try:
        student={}
        admno=int(input('Enter the admission number to search: '))
        found=False
        try:
            while True:
                student=pickle.load(f)
                if student['AdmNo']==admno:
                    print(student)
                    found=True
        except EOFError:
            if found==True:
                print('Student found (in pickle file).')
            else:
                print('Student not found (in pickle file).')
    except FileNotFoundError:
        print('File not  found')
    f.close()

# Function now requires the connection and cursor
def delete_student(mycon,cur):
    # --- 1. Logic to delete from Pickle File ---
    f1=open('C://Piyush//project//temporary.dat','wb')
    f=open('C://Piyush//project//student.dat','rb')
    admno_to_delete = 0 # Variable to hold the admno
    try:
        student={}
        found=False
        admno=int(input('Enter the admission number to delete: '))
        admno_to_delete=admno # Store it for the SQL command
        try:
            while True:
                student=pickle.load(f)
                if  student['AdmNo']==admno:
                    found=True
                    # Don't write this student to the temp file
                else:
                    pickle.dump(student,f1)
        except EOFError:
            if found==False:
                print('student not found (in pickle file).')
            else:
                # --- 2. If found in pickle, now delete from SQL ---
                print('Student deleted successfully (from pickle file).')
                try:
                    st="DELETE FROM student WHERE AdmNo = %s"
                    cur.execute(st,(admno_to_delete,)) # Pass admno as a tuple
                    if cur.rowcount>0:
                        mycon.commit()
                        print("Student deleted from SQL database.")
                    else:
                        print("Student was not found in SQL database.")
                except con.Error as e: 
                    print("An SQL error occurred while deleting:", e)

    except FileNotFoundError:
        print('File not found.')
    f.close()
    f1.close()
    # --- 3. Complete the pickle file rewrite ---
    os.remove('C://Piyush//project//student.dat')
    os.rename('C://Piyush//project//temporary.dat','C://Piyush//project//student.dat')

# Function now requires the connection and cursor
def update_student(mycon,cur):
    # --- 1. Logic to update Pickle File ---
    f=open('C://Piyush//project//student.dat','rb')
    f1=open('C://Piyush//project//temporary.dat','wb')
    try:
        student={}
        found=False
        admno=int(input('Enter the admission number to update: '))
        try:
            while True:
                student=pickle.load(f)
                if student['AdmNo']==admno:
                    # Get new data
                    new_phone=int(input('Enter the new phone number of the studbet: '))
                    new_address=input('Enter the new address of the  student: ')
                    
                    # Update dictionary before saving to pickle
                    student['Phone'] = new_phone
                    student['Address'] = new_address
                    pickle.dump(student,f1)
                    found=True
                    
                    # --- 2. Now Update in SQL Database ---
                    try:
                        st="UPDATE student SET Phone = %s, Address = %s WHERE AdmNo = %s"
                        cur.execute(st,(new_phone, new_address, admno))
                        if cur.rowcount>0:
                            mycon.commit()
                            print("Student updated successfully in SQL database.")
                        else:
                            print("Student was not found in SQL database (no update).")
                    except con.Error as e:
                        print("An SQL error occurred while updating:", e)
                else:
                    pickle.dump(student,f1)
        except EOFError:
            if found==True:
                print('Student Updated Successfully (in pickle file).')
            else:
                print('Student Not found (in pickle file).')
    except FileNotFoundError:
        print('File Not Found')
    f.close()
    f1.close()
    # --- 3. Complete the pickle file rewrite ---
    os.remove('C://Piyush//project//student.dat')
    os.rename('C://Piyush//project//temporary.dat','C://Piyush//project//student.dat')

# Function now reads from pickle and exports to CSV
def export(): # We keep 'cursor' as an argument
    f=open('C://Piyush//project//student.dat','rb')
    f1=open('C://Piyush//project//student.csv','w',newline='')
    try:      
        wob=csv.writer(f1)
        wob.writerow(['Name','AdmNo','RollNo','Phone','Address'])
        found=False
        student={}
        try:
            while True:
                # Read from pickle
                student=pickle.load(f)
                # Write to CSV
                wob.writerow([student['Name'],student['AdmNo'],student['RollNo'],student['Phone'],student['Address']])
                found=True
        except EOFError:
            if found==True:
                print('Successfully exported to csv format (from pickle file).')
            else:
                print('Could not export, sorry (pickle file empty)!')
    except FileNotFoundError:
        print('File Not Found')
    f.close()
    f1.close()

def menu():
    
    print('----------STUDENT DATABSE MANAGEMENT SYSTEM BY PIYUSH SAHU----------')
    print('----(Using Pickle File + MySQL Database + CSV Export)----')
    print('----1.Add student (Pickle + SQL)---- ')
    print('----2.Display all the added students (from Pickle)---- ')
    print('----3.Search student by admission number (from Pickle)---- ')
    print('----4.Delete student (Pickle + SQL)---- ')
    print('----5.Update student (Pickle + SQL)---- ')
    print('----6.Export to csv (from Pickle)---- ')
    print('----7.EXIT----')
    
    while True:
        try:
            choice=int(input('\nEnter your choice: '))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        
        if choice==1:
            add_student(mycon,cur)
        elif choice==2:
            display_all()
        elif choice==3:
            search_student()
        elif choice==4:
            delete_student(mycon,cur)
        elif choice==5:
            update_student(mycon,cur)
        elif choice==6:
            export()
        elif choice==7:
            print('Exiting the program. Goodbye!')
            mycon.close()
            break
            
menu()
