
import tkinter as tk
from tkinter import *
import time
import threading
from yahoo_fin import stock_info
import yfinance as yf
from plyer import notification
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

VERSION = "v1.3.2"
EMAIL = ""
PASSWORD = ""


class interface():
    window = ""

    searching = 0
    searchingLoop = 0

    tickerLabel = ""
    tickerAcao = ""
    tickerAcaoVar = ""
    nomeLabel = ""
    nomeLabelVar = ""
    vMinLabel = ""
    vMinNumVar = ""
    vMinNum = ""
    vMaxLabel = ""
    vMaxNumVar = ""
    vMaxNum = ""
    verRLabel = ""
    segEntryVar = ""
    segEntry = ""
    buttonVar = ""
    button = ""
    detalhesVar = ""
    detalhes = ""
    statusLabelVar = ""
    statusLabel = ""
    emailLabel = ""
    emailEntryVar = ""
    emailEntry = ""

    def __init__(self):
        self.window = tk.Tk()
        self.window.eval('tk::PlaceWindow . center')
        self.window.title("Notificações de Ações")
        self.window.minsize(500, 215)
        self.window.configure(bg="black")

        self.tickerLabel = Label(
            self.window, text="Ticker", bg="black", fg="white")
        self.tickerLabel.place(x=20, y=30)

        self.tickerAcaoVar = StringVar()
        self.tickerAcao = Entry(
            self.window, width=15, textvariable=self.tickerAcaoVar, bg="black", fg="white")
        self.tickerAcao.place(x=160, y=30)
        self.tickerAcao.insert(0, "NOS.LS")

        self.nomeLabelVar = StringVar()
        self.nomeLabel = Label(
            self.window, textvariable=self.nomeLabelVar, bg="black", fg="white")
        self.nomeLabel.place(x=280, y=30)

        self.vMinLabel = Label(
            self.window, text="Valor minimo", bg="black", fg="white")
        self.vMinLabel.place(x=20, y=55)
        self.vMinNumVar = StringVar()
        self.vMinNum = Entry(
            self.window, width=15, textvariable=self.vMinNumVar, bg="black", fg="white")
        self.vMinNum.place(x=160, y=55)
        self.vMinNum.insert(0, 3.7)

        self.vMaxLabel = Label(
            self.window, text="Valor máximo", bg="black", fg="white")
        self.vMaxLabel.place(x=280, y=55)
        self.vMaxNumVar = StringVar()
        self.vMaxNum = Entry(
            self.window, width=15, textvariable=self.vMaxNumVar, bg="black", fg="white")
        self.vMaxNum.place(x=380, y=55)
        self.vMaxNum.insert(0, 4)

        self.verRLabel = Label(
            self.window, text="Frequência (minutos)", bg="black", fg="white")
        self.verRLabel.place(x=20, y=80)
        self.segEntryVar = StringVar()
        self.segEntry = Entry(
            self.window, textvariable=self.segEntryVar,  width=10, bg="black", fg="white")
        self.segEntry.place(x=160, y=80)
        self.segEntry.insert(0, 15)

        self.buttonVar = StringVar()
        self.buttonVar.set("Pesquisar")
        self.button = Button(self.window, textvariable=self.buttonVar, width=20,
                             height=2, bg="black", fg="white", command=self.comecarThread)
        self.button.place(x=330, y=155)

        self.detalhesVar = StringVar()
        self.detalhes = Label(
            self.window, textvariable=self.detalhesVar, bg="black", fg="white")
        self.detalhes.place(x=20, y=155)

        self.statusLabelVar = StringVar()
        self.statusLabelVar.set("Parado")
        self.statusLabel = Label(
            self.window, textvariable=self.statusLabelVar, bg="black", fg="red")
        self.statusLabel.place(x=20, y=175)

        self.emailLabel = Label(
            self.window, text="Email (opcional)", bg="black", fg="white")
        self.emailLabel.place(x=20, y=105)
        self.emailEntryVar = StringVar()
        self.emailEntry = Entry(
            self.window, width=25, textvariable=self.emailEntryVar, bg="black", fg="white")
        self.emailEntry.place(x=160, y=105)

        self.version = Label(
            self.window, text="Created by: Bruno Ferreira | " + VERSION, bg="black", fg="#3a3a3a")
        self.version.place(x=300, y=5)

    def comecarThread(self):
        t = threading.Thread(target=pesquisar)
        if self.searching:
            self.searching = 0
            self.setLabelStatus("Pesquisa concluida")
            self.buttonVar.set("Pesquisar")
            self.detalhesVar.set("")
        else:
            self.searching = 1
            self.button.config(state="disabled")
            t.start()

    def setLabelStatus(self, labelStatus):
        if(labelStatus == "Parado"):
            self.statusLabel.config(fg="red")
        else:
            self.statusLabel.config(fg="green")
        self.statusLabelVar.set(labelStatus)


def reset():
    inter.searching = 0
    inter.buttonVar.set("Pesquisar")
    inter.detalhesVar.set("")
    inter.setLabelStatus("Parado")


def pesquisar():
    inter.detalhesVar.set("")
    ticker = inter.tickerAcaoVar.get()
    vMin = inter.vMinNumVar.get()
    vMax = inter.vMaxNumVar.get()
    seg = inter.segEntryVar.get()
    mail = inter.emailEntryVar.get()

    if(float(vMin) and float(vMax) and float(seg)):
        if ticker:
            tempo = int(seg)*60
            while inter.searching == 1:
                print("A verificar...")
                verificarValorAcao(ticker, float(vMin), float(vMax), mail)
                inter.setLabelStatus(
                    "A verificar novamente em " + seg + " minutos...")
                inter.buttonVar.set("Parar")
                inter.button.config(state="normal")
                for t in range(tempo):
                    if inter.searching == 1:
                        time.sleep(1)
                    else:
                        print("parou")
                        break
            reset()
        else:
            print("Existem campos vazios! ")
    else:
        print("Existem numeros inválidos! ")


def verificarValorAcao(ticker, valorMin, valorMax, mail):
    inter.setLabelStatus("A pesquisar")
    nome = str(buscarNome(ticker))
    inter.nomeLabelVar.set(nome)
    valor = buscarValor(ticker)

    if(float(valor) >= valorMin and float(valor) <= valorMax):
        inter.detalhesVar.set(
            "Está dentro do intervalo (entre " + str(valorMin) + " e " + str(valorMax) + ")")
    elif(float(valor) < valorMin):
        inter.detalhesVar.set("Baixa de " + str(valor))
        reset()
        notificacao("Ação da " + nome, "Baixa de " + str(valor))
        if(mail):
            sendMail(ticker, nome, valorMin, valorMax, mail)
    else:
        inter.detalhesVar.set("Alta de " + str(valor))
        reset()
        notificacao("Ação da " + nome, "Alta de " + str(valor))
        if(mail):
            sendMail(ticker, nome, valorMin, valorMax, mail)


def buscarValor(ticker):
    val = stock_info.get_live_price("NOS.LS")
    return round(val, 3)


def buscarNome(ticker):
    acao = yf.Ticker(ticker)
    return acao.info['longName']


def notificacao(t, m):
    notification.notify(title=t, message=m, app_icon=None, timeout=100)


def sendMail(ticker, nome, vMin, vMax, email):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Alerta Ação da "+nome
    message["From"] = EMAIL
    message["To"] = email

    msm = "Olá,"
    msm2 = "Novo alerta da ação "+nome
    msm3 = "O seu valor saiu do intervalo definido ("+str(
        vMin)+" - "+str(vMax)+")"

    html = """\
    <html>
    <body>
        <p>"""+msm+"""<br>
        """+msm2+"""<br>
        """+msm3+"""<br>
        </p>
    </body>
    </html>
    """
    texto = MIMEText(html, "html")
    message.attach(texto)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(EMAIL, PASSWORD)
        server.sendmail(
            EMAIL, email, message.as_string()
        )


inter = interface()
inter.window.mainloop()
