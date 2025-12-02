# This is a sample Python script.

# Press Shift+F6 to execute it or replace it with your code.
"""
import phoneScan
import FileScan
import sys
phoneScan.get_phone_number()
FileScan.get_file_scan()

"""
# Below are code for the GUI
import sys
import ctypes
import tkinter as tk
from tkinter import filedialog
from tkinter import *
import MalShare
from MalShare import get_malshare_info

#Makes GUI less blurry
#if 'win' in sys.platform:
#    ctypes.windll.shcore.SetProcessDpiAwareness(1)

main = Tk() #Tkinter window

#Window styles
main.geometry("600x600") #window size
main.title("Global Search") #Title of window 

#sets logo at top bar
logo = PhotoImage(file='logo.png')
main.iconphoto(True,logo)
main.config(background="#4A4459") #background color


#Text for instructions
home = Label(main,
             text="Pick a service:", 
             font=('Courier New',12), 
             fg="white", 
             bg="#4A4459", 
             padx=10,
             pady=10)
home.pack()

#Functions for each API Windows
#MalShare window function
def malShare_window():
    new_window = tk.Toplevel(main)
    new_window.title("MalShare")
    new_window.geometry("600x600")
    new_window.config(background="#4A4459")

    def compute_sha256(path):
        import hashlib
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                h.update(chunk)
        return h.hexdigest()

    #Function to open file 
    def openFile():
        filepath = filedialog.askopenfilename()
        if not filepath:
            return
        print("Selected:", filepath)
        hash_value = compute_sha256(filepath)
        print("File hash:", hash_value)
        # Correct call
        get_malshare_info(file_hash=hash_value, save_path="malshare_result.json")
    #Button
    tk.Button(new_window, 
              text="Select a File", 
              command=openFile,
              font=('Courier New', 12), 
              bg="#00C3EB", 
              fg="black", 
              activebackground='#FF0000', 
              activeforeground='white',
              width=20).pack(pady=20)
    #Back Button
    def back():
        new_window.destroy()
        main.deiconify()
    back_button = Button(new_window, 
                           text="Back", 
                           command=back,
                           font=('Courier New', 12), 
                           bg="#00C3EB", 
                           fg="black", 
                           activebackground='#FF0000', 
                           activeforeground='white',
                           width=20)
    back_button.pack(pady=20)
    main.withdraw()  #closes main window

#URLScan Window Function
def urlScan_window():
    new_window = tk.Toplevel(main)
    new_window.title("URLScan")
    new_window.geometry("600x600")
    new_window.config(background="#4A4459")
    #Text in the Window
    tk.Label(new_window,
             text="Paste a url:", 
             font=('Courier New',12), 
             fg="white", 
             bg="#4A4459", 
             padx=10,
             pady=10).pack()
    #Text box for url
    entry = Entry(new_window, font=('Courier New', 12))
    entry.pack(pady=20)
    #Submit Button
    from URLScan import get_url_scan
    def on_submit():
        import json
        url_value = entry.get()        
        result = get_url_scan(url_value)
        output_box.delete("1.0", tk.END)
        output_box.insert("1.0", json.dumps(result, indent=4))
    submit_button = Button(new_window, 
                           text="Submit", 
                           command=on_submit,
                           font=('Courier New', 12), 
                           bg="#00C3EB", 
                           fg="black", 
                           activebackground='#FF0000', 
                           activeforeground='white',
                           width=20)
    submit_button.pack()
    #Output box
    output_box = tk.Text(new_window, height=20, width=70, font=('Courier New', 10))
    output_box.pack(pady=20)
    #Back Button
    def back():
        new_window.destroy()
        main.deiconify()
    back_button = Button(new_window, 
                           text="Back", 
                           command=back,
                           font=('Courier New', 12), 
                           bg="#00C3EB", 
                           fg="black", 
                           activebackground='#FF0000', 
                           activeforeground='white',
                           width=20)
    back_button.pack(pady=20)
    main.withdraw()  #closes main window

#WebOfTrust Function
def webOfTrust_window():
    new_window = tk.Toplevel(main)
    new_window.title("Web of Trust")
    new_window.geometry("600x600")
    new_window.config(background="#4A4459")
    #Text in the Window
    tk.Label(new_window,
             text="Check companies: ", 
             font=('Courier New',12), 
             fg="white", 
             bg="#4A4459", 
             padx=10,
             pady=10).pack()
    #Text box for url
    entry = Entry(new_window, font=('Courier New', 12))
    entry.pack(pady=20)
    #Submit Button
    from web_of_trust import get_wot_project
    def on_submit():
        import json
        url_value = entry.get().strip()
        result = get_wot_project(url_value)
        output_box.delete("1.0", tk.END)
        output_box.insert("1.0", json.dumps(result, indent=4))

    submit_button = Button(new_window, 
                           text="Submit", 
                           command=on_submit,
                           font=('Courier New', 12), 
                           bg="#00C3EB", 
                           fg="black", 
                           activebackground='#FF0000', 
                           activeforeground='white',
                           width=20)
    submit_button.pack()
#Output box~
    output_box = tk.Text(new_window, height=20, width=70, font=('Courier New', 10))
    output_box.pack(pady=20)
    #Back Button
    def back():
        new_window.destroy()
        main.deiconify()
    back_button = Button(new_window, 
                           text="Back", 
                           command=back,
                           font=('Courier New', 12), 
                           bg="#00C3EB", 
                           fg="black", 
                           activebackground='#FF0000', 
                           activeforeground='white',
                           width=20)
    back_button.pack(pady=20)
    main.withdraw()  #closes main window

#VeriPhone Function
def veriPhone():
    new_window = tk.Toplevel(main)
    new_window.title("VeriPhone")
    new_window.geometry("600x600")
    new_window.config(background="#4A4459")
    #Text for phone number 
    phone_label = tk.Label(new_window, text="Phone Number:", font=('Courier New',12), fg="white", bg="#4A4459", padx=10, pady=10)
    phone_label.pack(pady=(20, 0))
    #Text box for phone number 
    phone_entry = Entry(new_window, font=('Courier New', 12))
    phone_entry.pack(pady=10)
    #Text for country code 
    cc_label = tk.Label(new_window, text="Country Code(optional):", font=('Courier New',12), fg="white", bg="#4A4459", padx=10, pady=10)
    cc_label.pack(pady=(20, 0))
    #Text box for country code
    cc_entry = Entry(new_window, font=('Courier New', 12))
    cc_entry.pack(pady=10)
    #Submit Button
    from phoneScan import get_phone_number
    def on_submit():
        import json
        number = phone_entry.get().strip()
        country = cc_entry.get().strip()
        data = {
            "number": number,
            "country_code": country if country else None
        }
        result = get_phone_number(data)
        output_box.delete("1.0", tk.END)
        output_box.insert("1.0", json.dumps(result, indent=4))
    submit_button = Button(new_window, 
                           text="Submit", 
                           command=on_submit,
                           font=('Courier New', 12), 
                           bg="#00C3EB", 
                           fg="black", 
                           activebackground='#FF0000', 
                           activeforeground='white',
                           width=20)
    submit_button.pack(pady=10)
    #Output box
    output_box = tk.Text(new_window, height=20, width=70, font=('Courier New', 10))
    output_box.pack(pady=20)
    #Back Button
    def back():
        new_window.destroy()
        main.deiconify()
    back_button = Button(new_window, 
                           text="Back", 
                           command=back,
                           font=('Courier New', 12), 
                           bg="#00C3EB", 
                           fg="black", 
                           activebackground='#FF0000', 
                           activeforeground='white',
                           width=20)
    back_button.pack(pady=20)
    main.withdraw()  #closes main window

#Function for virus total 
def virusTotal_window():
    new_window = tk.Toplevel(main)
    new_window.title("Virus Total")
    new_window.geometry("600x600")
    new_window.config(background="#4A4459")
    #Text in the Window
    tk.Label(new_window,
             text="URL or Files", 
             font=('Courier New',12), 
             fg="white", 
             bg="#4A4459", 
             padx=10,
             pady=10).pack()
    #File open
    from FileScan import get_file_scan
    import json
    from tkinter import filedialog
    def openFile():
        filepath = filedialog.askopenfilename()
        if not filepath:
            return 
        try: 
            result = get_file_scan(filepath)
        except Exception as e:
            result = {"error": str(e)}
        output_box.delete("1.0", tk.END)
        output_box.insert("1.0", json.dumps(result, indent=4))
    button = tk.Button(new_window,
                    text="Open", 
                    command=openFile,
                    font=('Courier New', 12), 
                    bg="#00C3EB", 
                    fg="black", 
                    activebackground='#FF0000', 
                    activeforeground='white',
                    width=20)
    button.pack(pady=40)
    #Output box
    output_box = tk.Text(new_window, height=20, width=70, font=('Courier New', 10))
    output_box.pack(pady=20)
    #Back Button
    def back():
        new_window.destroy()
        main.deiconify()
    back_button = Button(new_window, 
                           text="Back", 
                           command=back,
                           font=('Courier New', 12), 
                           bg="#00C3EB", 
                           fg="black", 
                           activebackground='#FF0000', 
                           activeforeground='white',
                           width=20)
    back_button.pack(pady=20)
    main.withdraw()  #closes main window

#Main window buttons
malShare = Button(main, 
                  text='Malshare', 
                  command=malShare_window, 
                  font=('Courier New', 12), 
                  bg="#00C3EB", 
                  fg="black", 
                  activebackground='#FF0000', 
                  activeforeground='white',
                  width=20).pack(pady=5)

urlScan = Button(main,text='URLScan',
                 command=urlScan_window,
                 font=('Courier New', 12),  
                 bg="#00C3EB", 
                 fg="black", 
                 activebackground='#FF0000', 
                 activeforeground='white',
                 width=20).pack(pady=20)

webOfTrust = Button(main,
                    text='WebofTrust',
                    command=webOfTrust_window,
                    font=('Courier New', 12), 
                    bg="#00C3EB", 
                    fg="black", 
                    activebackground='#FF0000', 
                    activeforeground='white',
                    width=20)
webOfTrust.pack(pady=0)

veriPhone = Button(main,
                   text='Veriphone',
                   command=veriPhone,
                   font=('Courier New', 12), 
                   bg="#00C3EB", 
                   fg="black", 
                   activebackground='#FF0000', 
                   activeforeground='white',
                   width=20).pack(pady=20)

virusTotal = Button(main,
                    text='VirusTotal',
                    command=virusTotal_window,
                    font=('Courier New', 12), 
                    bg="#00C3EB", 
                    fg="black", 
                    activebackground='#FF0000', 
                    activeforeground='white',
                    width=20).pack(pady=10)

End = Button(main,text='Exit')
End.config(command=main.quit,
           font=('Courier New', 12), 
           bg="#00C3EB", 
           fg="black", 
           activebackground='#FF0000', 
           activeforeground='white',
           width=20)
End.pack(pady=20)
#ends application

main.mainloop()