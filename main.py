from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import random
import pyperclip
from cryptography.fernet import Fernet
from cryptography.fernet import Fernet



# def retrieve_password():
#     window2 = Tk()
#     window2.title("Password warehouse")
#     window2.minsize(width=200, height=400)
#     window2.config(padx=20, pady=50)
#     w = Label(master=window2, text="Click the name of a Domain to copy its password ")
#
#     with open('data.txt', 'r') as f:
#         passes = f.readlines()
#
#     k = 0
#     var = IntVar()
#     R = []
#     for i in passes:
#         domain = i.split('|')[0]
#         passencrypt = ''.join(i.split('|')[2])
#         print(passencrypt)
#         R.append(Radiobutton(window2, text=domain, variable=var, value=k))
#         R[k].pack(anchor=W)
#         k += 1
#     pyperclip.copy(fernet.decrypt(bytes(passencrypt, 'utf-8')))
#     window2.mainloop()


# read key and convert into byte
with open('key.txt') as f:
    refKey = ''.join(f.readlines())
    refKeybyt = bytes(refKey, 'utf-8')

fernet = Fernet(refKeybyt)

# decMessage = fernet.decrypt(encMessage).decode()
    # ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    password_list.extend([random.choice(letters) for _ in range(nr_letters)])
    password_list.extend([random.choice(symbols) for _ in range(nr_symbols)])
    password_list.extend([random.choice(numbers) for _ in range(nr_numbers)])

    for char in range(nr_numbers):
      password_list += random.choice(numbers)

    random.shuffle(password_list)

    password = "".join(password_list)
    entry3.delete(0,'end')
    entry3.insert(string=password,index=0)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    """
    Saves the password in data.txt file
    :return: None
    """
    website=entry1.get()
    email=entry2.get()
    password=entry3.get()
    if len(website)==0 or len(email)==0 or len(password)==0:
        messagebox.showwarning(title="Empty field(s)", message="One or more of the fields are empty. Please try again")
        return


    OK=messagebox.askokcancel(title=website,message=f" Verify the credentials you have entered before clicking OK.\n Email: {email}\n Password: {password}\n Is this ok?")
    if OK:

        with open('data.txt','a') as file:
            mypwdbyt = bytes(password, 'utf-8')
            encryptedPWD = fernet.encrypt(mypwdbyt)
            print(encryptedPWD)
            file.write(f"{website}|{email}|{password}\n")
            entry1.delete(0, 'end')
            entry3.delete(0, 'end')

        with open('encrypted_password','wb') as encrypted_file:
            encrypted_file.write(encryptedPWD)

        # Decrypt the data
        with open('encrypted_password', 'rb') as encrypted_file:
            encrypted_data = encrypted_file.read()
            decrypted_data = fernet.decrypt(encrypted_data)

        with open('decrypted_data.txt', 'wb') as decrypted_file:
            decrypted_file.write(decrypted_data)
        

    else:
        pass

# ---------------------------- UI SETUP ------------------------------- #

#--WINDOW--#
window = Tk()
window.title("Password manager")
window.minsize(width=400,height=400)
window.config(padx=50,pady=50)


#Image
canvas = Canvas(width=200,height=200)
image = PhotoImage(file="logo.png")
canvas.create_image(100,100,image=image)
canvas.grid(row=0,column=1)


#Website
label1 = Label(text="Website", font=("courier",10,"bold"))
label1.grid(row=1,column=0)

entry1 = Entry( window, width=52 )
entry1.grid(row=1,column=1,columnspan=2)
entry1.insert(0,"www.websitename.domain")
entry1.focus()

#Email
label2 = Label(text="Email/Username", font=("courier",10,"bold"))
label2.grid(row=2,column=0)

entry2 = Entry( window, width=52 )
entry2.grid(row=2,column=1,columnspan=2)
entry2.insert(0,"example@email.com")


#Password
label3 = Label(text="Password", font=("courier",10,"bold"))
label3.grid(row=3,column=0)

entry3 = Entry(window, width=30)
entry3.grid(row=3,column=1,sticky='ew')

button1 = ttk.Button(text="Generate password",command=password_generator)
button1.grid(row=3, column=2)


#Add button
button2 = ttk.Button(text="Add",width=52,command=save)
button2.grid(row=4, column=1,columnspan=2)

# #Add button
# button3 = ttk.Button(text="Retrieve password",width=52,command=retrieve_password)
# button3.grid(row=5, column=1,columnspan=2)


window.mainloop()

# ------------------------------------------------------ RETRIEVING PASSWORDS ------------------------------------------------#
