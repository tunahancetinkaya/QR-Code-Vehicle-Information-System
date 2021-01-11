from tkinter import *
import sqlite3
import qrcode
from PIL import ImageTk, Image
import pyzbar.pyzbar as pyzbar
import smtplib
import cv2

qrkod = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4, )
ekran = Tk()
ekran.geometry('600x500')
ekran.title("QR Kod Araç Bilgi Sistemi")
veri = sqlite3.connect('test1.db')
isim = StringVar()
soyisim = StringVar()
email = StringVar()
marka = StringVar()
model = StringVar()
plaka = StringVar()
hasar = StringVar()

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN

isim1 = ""
soyisim1 = ""
email1 = ""
marka1 = ""
model1 = ""
plaka1 = ""
hasar1 = ""

def ilk():
    ekrantemizle()
    label1 = Label(ekran, text="QR Kod Araç Bilgi Sistemi", width=20, font=("bold", 20))
    label1.place(x=150, y=50)
    Button(ekran, text='Kayıt Ol', width=40, bg='brown', fg='white', command=register).place(x=150, y=150)
    Button(ekran, text='QR Kod Okut', width=40, bg='brown', fg='white', command=kamera).place(x=150, y=200)
    Button(ekran, text='QR Kod Öğren', width=40, bg='brown', fg='white', command=qrkodogren).place(x=150, y=250)
    Button(ekran, text='Plaka İle Devam Et', width=40, bg='brown', fg='white', command= plakaile).place(x=150, y=300)
    Button(ekran, text='Kapat', width=10, bg='brown', fg='white', command=kapat).place(x=500, y=0)

def qrkodogren():
    ekrantemizle()
    global plaka1
    label1 = Label(ekran, text="QR Kod Araç Bilgi Sistemi QR Kod Öğrenme", width=35, font=("bold", 20))
    label1.place(x=25, y=100)
    label_1 = Label(ekran, text="Plaka", width=20, font=("bold", 10))
    label_1.place(x=100, y=200)

    entry_1 = Entry(ekran, textvar=plaka)
    entry_1.place(x=260, y=200)
    Button(ekran, text='Plaka İle Devam Et', width=40, bg='brown', fg='white', command=qrkodyazdir).place(x=150, y=300)
    Button(ekran, text='Kapat', width=10, bg='brown', fg='white', command=kapat).place(x=500, y=0)
    Button(ekran, text='Menüye Dön', width=40, bg='brown', fg='white', command=ilk).place(x=150, y=400)

def kamera():
    global plaka1
    temp = 1
    data = ""
    while temp:
        _, frame = cap.read()
        decodedObjects = pyzbar.decode(frame)
        for obj in decodedObjects:
            data = obj.data.decode("utf-8")
            cv2.putText(frame, str(obj.data), (50, 50), font, 2,
                        (255, 0, 0), 3)

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        if key == 27:
            break

        oku = veri.execute("SELECT count(*) as 'giris' FROM kullanici where plaka='" + data + "'")
        for i in oku.fetchall():
            giris = i[0]
        if (giris == 1):
            plaka1=data
            temp = 0
            cv2.destroyAllWindows()
    mail()

def ekrantemizle():
    for widget in ekran.winfo_children():
        widget.destroy()

def plakaile():
    ekrantemizle()
    global plaka1
    label1 = Label(ekran, text="QR Kod Araç Bilgi Sistemi Plaka İle Uyarma", width=35, font=("bold", 20))
    label1.place(x=25, y=100)
    label_1 = Label(ekran, text="Plaka", width=20, font=("bold", 10))
    label_1.place(x=100, y=200)

    entry_1 = Entry(ekran, textvar=plaka)
    entry_1.place(x=260, y=200)
    Button(ekran, text='Plaka İle Devam Et', width=40, bg='brown', fg='white', command=plakaile2).place(x=150, y=300)
    Button(ekran, text='Kapat', width=10, bg='brown', fg='white', command=kapat).place(x=500, y=0)
    Button(ekran, text='Menüye Dön', width=40, bg='brown', fg='white', command=ilk).place(x=150, y=400)

def plakaile2():
    global isim1, plaka1, soyisim1, email1, marka1, model1, hasar1
    global isim, plaka, soyisim, email, marka, model, hasar
    plaka1 = plaka.get()
    vericek()
    mail()

def register():
    ekrantemizle()
    global isim
    label1 = Label(ekran, text="QR Kod Araç Bilgi Sistemi kayıt Ekranı", width=35, font=("bold", 20))
    label1.place(x=25, y=50)
    label_1 = Label(ekran, text="İsim", width=20, font=("bold", 10))
    label_1.place(x=80, y=130)

    entry_1 = Entry(ekran, textvar=isim)
    entry_1.place(x=240, y=130)

    label_2 = Label(ekran, text="Soyisim", width=20, font=("bold", 10))
    label_2.place(x=80, y=155)

    entry_2 = Entry(ekran, textvar=soyisim)
    entry_2.place(x=240, y=155)

    label_3 = Label(ekran, text="Email", width=20, font=("bold", 10))
    label_3.place(x=80, y=180)

    entry_3 = Entry(ekran, textvar=email)
    entry_3.place(x=240, y=180)

    label_4 = Label(ekran, text="Plaka", width=20, font=("bold", 10))
    label_4.place(x=80, y=205)

    entry_4 = Entry(ekran, textvar=plaka)
    entry_4.place(x=240, y=205)

    label_5 = Label(ekran, text="Araba markası", width=20, font=("bold", 10))
    label_5.place(x=80, y=230)

    entry_5 = Entry(ekran, textvar=marka)
    entry_5.place(x=240, y=230)

    label_6 = Label(ekran, text="Araba Modeli", width=20, font=("bold", 10))
    label_6.place(x=80, y=255)

    entry_6 = Entry(ekran, textvar=model)
    entry_6.place(x=240, y=255)

    label_7 = Label(ekran, text="Hasar Bilgisi", width=20, font=("bold", 10))
    label_7.place(x=80, y=280)

    entry_7 = Entry(ekran, textvar=hasar)
    entry_7.place(x=240, y=280)

    Button(ekran, text='Kayıt Ol', width=20, bg='brown', fg='white', command=registerr).place(x=300, y=400)
    Button(ekran, text='Menüye Dön', width=20, bg='brown', fg='white', command=ilk).place(x=100, y=400)
    Button(ekran, text='Kapat', width=10, bg='brown', fg='white', command=kapat).place(x=500, y=0)

def registerr():
    global isim, soyisim, marka, model, email, hasar, plaka
    isim = isim.get()
    soyisim = soyisim.get()
    email = email.get()
    plaka = plaka.get()
    marka = marka.get()
    model = model.get()
    hasar = hasar.get()

    with veri:
        cursor = veri.cursor()
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS kullanici (isim TEXT,soyisim TEXT,email TEXT,plaka TEXT,marka TEXT,model TEXT,hasar TEXT)')
    cursor.execute('INSERT INTO kullanici (isim,soyisim,email,plaka,marka,model,hasar) VALUES(?,?,?,?,?,?,?)',
                   (isim, soyisim, email, plaka, marka, model, hasar,))
    veri.commit()
    qrkodolustur()
    kayitson()

def kayitson():
    ekrantemizle()
    label1 = Label(ekran, text="QR Kod Araç Bilgi Sistemi", width=20, font=("bold", 20))
    label1.place(x=120, y=50)
    label1 = Label(ekran, text="Kayıt Oldunuz", width=20, font=("bold", 35))
    label1.place(x=50, y=150)
    Button(ekran, text='Menüye Dön', width=40, bg='brown', fg='white', command=ilk).place(x=150, y=300)


def qrkodyazdir():
    ekrantemizle()
    global plaka1, plaka
    plaka1 = plaka.get()
    load = Image.open('kodlar\{}.png'.format(plaka1))
    render = ImageTk.PhotoImage(load)
    img = Label(image=render)
    img.image = render
    img.place(x=150, y=20)
    Button(ekran, text='Kapat', width=10, bg='brown', fg='white', command=kapat).place(x=500, y=0)
    Button(ekran, text='Menüye Dön', width=10, bg='brown', fg='white', command=ilk).place(x=250, y=400)

def qrkodolustur():
    global plaka
    qrkod.add_data(plaka)
    qrkodimg = qrkod.make_image()
    qrkodimg.save("kodlar\{}.png".format(plaka))

def vericek():
    global isim1, plaka1, soyisim1, email1, marka1, model1, hasar1
    global isim, plaka, soyisim, email, marka, model, hasar
    oku = veri.execute("SELECT * FROM kullanici where plaka='" + plaka1 + "'")
    oku1 = oku.fetchall()
    isim1 = oku1[0][0]
    soyisim1 = oku1[0][1]
    email1 = oku1[0][2]
    plaka1 = oku1[0][3]
    marka1 = oku1[0][4]
    model1 = oku1[0][5]
    hasar1 = oku1[0][6]

def mail():
    global isim1, plaka1, soyisim1, email1, marka1, model1, hasar1
    global isim, plaka, soyisim, email, marka, model, hasar
    ekrantemizle()
    label1 = Label(ekran, text="QR Kod Araç Bilgi Sistemi", width=35, font=("bold", 20))
    label1.place(x=25, y=100)
    Button(ekran, text='Yanlis Park', width=40, bg='brown', fg='white', command=yanlispark).place(x=150, y=150)
    Button(ekran, text='Arac Bilgi', width=40, bg='brown', fg='white', command=aracbilgi).place(x=150, y=200)
    Button(ekran, text='Arac Cekme', width=40, bg='brown', fg='white', command=araccekme).place(x=150, y=250)
    Button(ekran, text='Acil', width=40, bg='brown', fg='white', command=acil).place(x=150, y=300)
    Button(ekran, text='kamera', width=40, bg='brown', fg='white', command=kamera).place(x=150, y=350)
    Button(ekran, text='Menüye Dön', width=40, bg='brown', fg='white', command=ilk).place(x=150, y=400)
    Button(ekran, text='Kapat', width=10, bg='brown', fg='white', command=kapat).place(x=500, y=0)

def kapat():
    ekran.destroy()

def aracbilgi():
    ekrantemizle()
    vericek()
    global isim1, plaka1, soyisim1, email1, marka1, model1, hasar1
    global isim, plaka, soyisim, email, marka, model, hasar
    label1 = Label(ekran, text="İsim", width=20, font=("bold", 15))
    label1.place(x=50, y=50)
    label1 = Label(ekran, text=isim1, width=20, font=("bold", 15))
    label1.place(x=200, y=50)
    label1 = Label(ekran, text="Soyisim", width=20, font=("bold", 15))
    label1.place(x=50, y=100)
    label1 = Label(ekran, text=soyisim1, width=20, font=("bold", 15))
    label1.place(x=200, y=100)
    label1 = Label(ekran, text="Email", width=20, font=("bold", 15))
    label1.place(x=50, y=150)
    label1 = Label(ekran, text=email1, width=40, font=("bold", 15))
    label1.place(x=200, y=150)
    label1 = Label(ekran, text="Plaka", width=20, font=("bold", 15))
    label1.place(x=50, y=200)
    label1 = Label(ekran, text=plaka1, width=20, font=("bold", 15))
    label1.place(x=200, y=200)
    label1 = Label(ekran, text="Marka", width=20, font=("bold", 15))
    label1.place(x=50, y=250)
    label1 = Label(ekran, text=marka1, width=20, font=("bold", 15))
    label1.place(x=200, y=250)
    label1 = Label(ekran, text="Model", width=20, font=("bold", 15))
    label1.place(x=50, y=300)
    label1 = Label(ekran, text=model1, width=20, font=("bold", 15))
    label1.place(x=200, y=300)
    label1 = Label(ekran, text="Hasar", width=20, font=("bold", 15))
    label1.place(x=50, y=350)
    label1 = Label(ekran, text=hasar1, width=20, font=("bold", 15))
    label1.place(x=200, y=350)
    Button(ekran, text='Menüye Dön', width=40, bg='brown', fg='white', command=ilk).place(x=150, y=400)
    Button(ekran, text='Kapat', width=10, bg='brown', fg='white', command=kapat).place(x=500, y=0)

def acil():
    global isim1, plaka1, soyisim1, email1, marka1, model1, hasar1
    global isim, plaka, soyisim, email, marka, model, hasar
    konu = "Acil"
    mesaj = "Acil bir olay icin aracinizin yanina gelmeniz gerekmektedir"
    mailmesaj = """
                Gonderen:   Qr Kod Arac Bilgi Sistemi
                Konu:       %s
                Mesaj:      %s
        """ % (konu, mesaj)
    mail = smtplib.SMTP("smtp.gmail.com", 587)

    mail.ehlo()
    mail.starttls()
    mail.login("qrkodaracbilgisistemi@gmail.com", "qrkodbilgi")
    mail.sendmail("qrkodaracbilgisistemi@gmail.com", email1, mailmesaj)

def araccekme():
    global isim1, plaka1, soyisim1, email1, marka1, model1, hasar1
    global isim, plaka, soyisim, email, marka, model, hasar
    konu = "Arac Cekme"
    mesaj = "Aracinizi yanlis yere park ettiniz lutfen 5 dakika icinde aracinizi bulundugu yerden aliniz"
    mailmesaj = """
                Gonderen:   Qr Kod Arac Bilgi Sistemi
                Konu:       %s
                Mesaj:      %s
        """ % (konu, mesaj)
    mail = smtplib.SMTP("smtp.gmail.com", 587)

    mail.ehlo()
    mail.starttls()
    mail.login("qrkodaracbilgisistemi@gmail.com", "qrkodbilgi")
    mail.sendmail("qrkodaracbilgisistemi@gmail.com", email1, mailmesaj)

def yanlispark():
    global isim1, plaka1, soyisim1, email1, marka1, model1, hasar1
    global isim, plaka, soyisim, email, marka, model, hasar
    konu = "yanlis park"
    mesaj = "aracinizi yanlis yere park ettiniz lutfen aracinizin yanina geliniz"
    mailmesaj = """
                Gonderen:   Qr Kod Arac Bilgi Sistemi
                Konu:       %s
                Mesaj:      %s
        """ % (konu, mesaj)
    mail = smtplib.SMTP("smtp.gmail.com", 587)

    mail.ehlo()
    mail.starttls()
    mail.login("qrkodaracbilgisistemi@gmail.com", "qrkodbilgi")
    mail.sendmail("qrkodaracbilgisistemi@gmail.com", email1, mailmesaj)

ilk()
ekran.mainloop()