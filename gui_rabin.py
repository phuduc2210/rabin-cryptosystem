from tkinter import *
from src.rabin_cryptosystem import is_prime, is_number, get_num_from_file, chek_input, file_encrypt, file_decrypt, get_byte_from_file

#const
btn_width = 100 
btn_height = 40 
ent_width = 150
ent_height = 30
win_width = 600
win_height = 320

er = "Error"
er_num = r"It is not valid values "
no_file = r"You must to choose any file "  
dec_er = r"I couldn't read it! "

def main():

    def go_encrypt():
        encryption_frame()
        root.destroy()

    def go_decrypt():
        decryption_frame()
        root.destroy()

    root = Tk()
    root.geometry("{}x{}".format(win_width, win_height))
    root.title("Rabin cryptosystem")
    root.resizable(False, False)
    root.focus_force()
    
    fr_mainmenu = Frame(root, bg = "gray", width = win_width, \
                        height = win_height)

    fr_mainmenu.pack(fill="both", side="top", expand=True)

    btn_enc = Button(fr_mainmenu, text = "Encrypt", bg='pink', fg='black', command = go_encrypt)
    btn_dec = Button(fr_mainmenu, text = "Decrypt", bg='pink', fg='black', command = go_decrypt)

    btn_enc.place(relx=0.5, x = -btn_width // 2, \
                  rely=0.5, y = -btn_height, \
                  width=btn_width,height=btn_height)
    btn_dec.place(relx=0.5,  x = -btn_width // 2, \
                  rely=0.5, y = 1, \
                  width=btn_width, height=btn_height)
    
    root.mainloop()


def decryption_frame():

    def go_back():
        root.destroy()
        main()

    def get_dec_values(p, q, b):
        '''

        '''
        p = p.get()
        if is_number(p):
            p = int(p)
        else:
            p = 0

        q = q.get()
        if is_number(q):
            q = int(q)
        else:
            q = 0

        b = b.get()
        if is_number(b):
            b = int(b)
        else:
            b = 0

        n = p * q

        return (p, q, b, n)

    def decrypt():
        #const
        count_to_out = 40

        p, q, b, n = get_dec_values(p_enter, q_enter, b_enter)

        if chek_input(p=p, q=q, b=b, n=n):
            filename = open_file()
            if filename:
                
                decyphertext = file_decrypt(filename, p, q, b)
                if decyphertext:
                    nums = get_num_from_file(filename)
                    #Cho phép đầu vào
                    textbox.configure(state=NORMAL)
                    textbox_pl.configure(state=NORMAL)
                    textbox.delete(1.0, END)
                    textbox_pl.delete(1.0, END)
                    textbox_pl.insert(1.0, "Encrypted file(20 symb):\n")
                    textbox.insert(1.0, "Decyphered file(20 symb):\n")
                    i = 0
                    for num in nums:
                        textbox_pl.insert(END, str(num)+" ")
                        if i >= count_to_out:
                            break
                    i = 0
                    while (i <= count_to_out) and (i < len(decyphertext)):
                        textbox.insert(END, str(decyphertext[i])+" ")
                        i += 1
                    textbox.configure(state=DISABLED)
                    textbox_pl.configure(state=DISABLED)
                else:
                    show_error(dec_er)
            else:
                show_error(no_file)
        else:
            show_error(er_num)
        print(p, q, b, n)    

    root = Tk()
    root.geometry("{}x{}".format(win_width, win_height))
    root.title("Decryption")
    root.resizable(False, False)
    root.focus_force()

    #Frame
    fr_decrypt = Frame(root, bg="gray", width=win_width//2, \
                        height=win_height)

    fr_decrypt.pack(side="left")
    fr_out = Frame(root, bg="white", width=win_width//2, \
                   height=win_height)
    fr_out.pack(side="left")

    #Textbox
    textbox_pl = Text(fr_out, font="Arial 18", bg = "green", wrap=WORD, \
                      state=NORMAL)
    textbox = Text(fr_out, font="Arial 18", bg = "#c3aee2", wrap=WORD, \
                   state=NORMAL)
    textbox_pl.place(height=win_height//2, width=win_width//2)
    textbox.place(rely=.5,height=win_height//2, width=win_width//2)
    textbox_pl.insert(1.0, "Encrypted file(20 symb):\n")
    textbox.insert(1.0, "Decyphered file(20 symb):\n") 
    textbox.configure(state=DISABLED)
    textbox_pl.configure(state=DISABLED)
    scroll = Scrollbar(textbox, command=textbox.yview)
    textbox["yscrollcommand"] = scroll.set
    scroll.pack(side="right", fill="y")
    scroll_pl = Scrollbar(textbox_pl, command=textbox_pl.yview)
    textbox["yscrollcommand"] = scroll_pl.set
    scroll_pl.pack(side="right", fill="y")

    #Entry
    p_enter = Entry(fr_decrypt, font="Tahoma")
    p_enter.place(relx=.5, x=-ent_width//2, rely=.2, y = -ent_height, \
                  width=ent_width, height=ent_height)
    q_enter = Entry(fr_decrypt, font="Tahoma")
    q_enter.place(relx=.5, x=-ent_width//2, rely=.3,  \
                  width=ent_width, height=ent_height)
    b_enter = Entry(fr_decrypt, font="Tahoma")
    b_enter.place(relx=.5, x=-ent_width//2, rely=.4, y = ent_height, \
                  width=ent_width, height=ent_height)

    #Labels    
    lb_p = Label(fr_decrypt, text="P = ")
    lb_p.place(relx=.04, rely=.12)
    lb_q = Label(fr_decrypt, text="Q = ")
    lb_q.place(relx=.04, rely=.32)
    lb_b = Label(fr_decrypt, text="B = ")
    lb_b.place(relx=.04, rely=.52)
    
    #Buttons
    btn_back = Button(fr_decrypt, text="Back", bg='pink', fg='black', command = go_back)
    btn_back.place(relx=.5, x=-btn_width//2, rely=.8, width=btn_width, height=btn_height)
    btn_encrypt = Button(fr_decrypt, text="Decrypt", bg="pink", fg="black", command= decrypt)
    btn_encrypt.place(relx=.5, x=-btn_width//2, rely=.67, width=btn_width, height=btn_height)

def encryption_frame():

    def go_back():
        root.destroy()
        main()

    def get_enc_values(n, b):
        '''
        Nếu một giá trị không hợp lệ được nhập, nó sẽ trả về 0
        '''
        str_n = n.get()
        li_n = str_n.split("*")
        n = 1
        for num in li_n:
            num = num.strip()
            if is_number(num):
                if is_prime(int(num)) and (int(num) % 4 == 3):
                    n *= int(num)
                else:
                    n = 0
            else:
                n = 0

        b = b.get()
        if is_number(b):
            b = int(b)
        else:
            b = 0 

        return (n, b)
                       
    def encrypt():
        #const
        count_to_out = 40

        n, b  = get_enc_values(n_enter, b_enter)
        #if chek_input(p=p, q=q, b=b, n=n):

        if (0 < b < n) and (n >= 256):
            filename = open_file()
            if filename:
                cyphertext = file_encrypt(filename, n, b)
                if (cyphertext):
                    i = 0
                    by = get_byte_from_file(filename)
                    #Cho phép đầu vào:
                    textbox.configure(state=NORMAL)
                    textbox_pl.configure(state=NORMAL)
                    textbox.delete(1.0, END)
                    textbox_pl.delete(1.0, END)
                    textbox_pl.insert(1.0, "Plain file(20 symb):\n")
                    textbox.insert(1.0, "Ciphered file(20 symb):\n") 
                    while (i <= count_to_out) and (i < len(cyphertext)):
                        textbox.insert(END, str(cyphertext[i])+" ")
                        textbox_pl.insert(END, str(next(by))+" ")
                        i += 1
                    textbox.configure(state=DISABLED)
                    textbox_pl.configure(state=DISABLED)
                else:
                    show_error(dec_er)
            else:
                show_error(no_file)
        else:
            show_error(er_num)
        print(n, b)

    root = Tk()
    root.geometry("{}x{}".format(win_width, win_height))
    root.title("Encryption")
    root.resizable(False, False)
    root.focus_force()

    #Encrypt frame:
    fr_encrypt = Frame(root, bg = "gray", width = win_width // 2, \
                        height = win_height)

    fr_encrypt.pack(side="left")
    fr_out = Frame(root, bg="white", width=win_width//2, \
                   height=win_height)
    fr_out.pack(side="right")

    #Textbox
    textbox_pl = Text(fr_out, font="Arial 18", bg = "green", wrap=WORD, \
                      state=NORMAL)
    textbox = Text(fr_out, font="Arial 18", bg = "#c3aee2", wrap=WORD, \
                   state=NORMAL)
    textbox_pl.place(height=win_height//2, width=win_width//2)
    textbox.place(rely=.5,height=win_height//2, width=win_width//2)
    textbox_pl.insert(1.0, "Plain file(20 symb):") #Textbox PLain text
    textbox.insert(1.0, "Ciphered file(20 symb):") 
    textbox.configure(state=DISABLED)
    textbox_pl.configure(state=DISABLED)   
    scroll = Scrollbar(textbox, command=textbox.yview)
    textbox["yscrollcommand"] = scroll.set
    scroll.pack(side="right", fill="y")
    scroll_pl = Scrollbar(textbox_pl, command=textbox_pl.yview)
    textbox["yscrollcommand"] = scroll_pl.set
    scroll_pl.pack(side="right", fill="y")

    #Entry
    n_enter = Entry(fr_encrypt, font="Tahoma")
    n_enter.place(relx=.5, x=-ent_width//2, rely=.2, y = -ent_height, \
                  width=ent_width, height=ent_height)
    b_enter = Entry(fr_encrypt, font="Tahoma")
    b_enter.place(relx=.5, x=-ent_width//2, rely=.3, \
                  width=ent_width, height=ent_height)

    #Labels    
    lb_n = Label(fr_encrypt, text="N = ")
    lb_n.place(relx=.04, rely=.12)

    lb_b = Label(fr_encrypt, text="B = ")
    lb_b.place(relx=.04, rely=.32)

    #Buttons
    btn_back = Button(fr_encrypt, text="Back", bg='pink', fg='black', command = go_back)
    btn_back.place(relx=.5, x=-btn_width//2, rely=.8, width=btn_width, height=btn_height)
    btn_decrypt = Button(fr_encrypt, text="Encrypt", bg="pink", fg="black", command= encrypt)
    btn_decrypt.place(relx=.5, x=-btn_width//2, rely=.67, width=btn_width, height=btn_height)

def show_error(msg):
    from tkinter import messagebox
    root = Tk()
    root.withdraw() #cần một cửa sổ, nếu không, nó sẽ trống 
    messagebox.showerror(er, msg)
    print(msg)
    root.destroy()
    return 0

def open_file():
    '''

    '''
    from tkinter import filedialog
    root = Tk()
    root.withdraw()
    filename = filedialog.askopenfilename(initialdir = "/", title="Select file")
    print("Open: {}".format(filename))
    root.destroy()
    return filename


if __name__ == "__main__":
    main()

