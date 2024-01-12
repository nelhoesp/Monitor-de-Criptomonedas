# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import requests
import yfinance as yf
import mplfinance as mpf
import pandas as pd

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.resizable(0, 0)
        self.title("Crypto Monitor")
        
        self.var_base = tk.IntVar()
        
        frm = tk.Frame(self)
        frm.pack(padx=10, pady=10)
        
        frm1 = tk.Frame(frm)
        frm2 = tk.LabelFrame(frm, text="Price Historic Chart")
        frm1.pack(side=tk.LEFT, padx=5, pady=5)
        frm2.pack(side=tk.LEFT, padx=5, pady=5)
        frm_1 = tk.LabelFrame(frm1, text="Price Realtime")
        frm_2 = tk.LabelFrame(frm1, text="Historic Data")
        frm_1.pack(side=tk.TOP, padx=0, pady=5)
        frm_2.pack(side=tk.TOP, padx=0, pady=5)
        
        self.SELECTED = False
        self.ant_valor = 0
        self.act_valor = 0
        
        #-------------------Price Realtime
        
        cryptos = ['Bitcoin', 'Ethereum', 'Chainlink', 'Binance Coin', 'Litecoin', 'Dogecoin']
        self.diminutivos = {'Bitcoin':'btc-usd',
                       'Ethereum':'eth-usd',
                       'Chainlink':'link-usd',
                       'Binance Coin':'bnb-usd',
                       'Litecoin':'ltc-usd',
                       'Dogecoin':'doge-usd'}
        
        self.lblSel = tk.Label(frm_1, text="Select Token:")
        self.cboToken = ttk.Combobox(frm_1, state='readonly', values=cryptos)
        self.lblCash = tk.Label(frm_1, text="0 USD", width=12, anchor=tk.E, fg="green", font=("Helvetica", 13, "bold"))
        self.lblsmall = tk.Label(frm_1, text="0.00 0.00%")
        self.cboToken.bind("<<ComboboxSelected>>", self.crypto_selected)
        
        self.lblSel.grid(row=0, column=0, padx=5, pady=5)
        self.cboToken.grid(row=0, column=1, padx=5, pady=5)
        self.lblCash.grid(row=0, column=2, padx=5, pady=5, sticky=tk.E)
        self.lblsmall.grid(row=1, column=2, padx=5, pady=5, sticky=tk.E)
        
        #-------------------Historic Data
        
        self.scroll = tk.Scrollbar(frm_2)
        self.scroll.pack(side=tk.RIGHT,fill=tk.Y)
        
        self.table = ttk.Treeview(frm_2, columns=(1, 2), height=16, yscrollcommand=self.scroll.set)
        self.table.pack()
        self.scroll.config(command=self.table.yview)
        
        self.table.heading("#0", text="Date")
        self.table.heading("#1", text="Open")
        self.table.heading("#2", text="Close")
        
        self.table.column("#0", width=119, minwidth=110, stretch=tk.NO)
        self.table.column("#1", width=119, minwidth=80, stretch=tk.NO)
        self.table.column("#2", width=119, minwidth=80, stretch=tk.NO)
        
        #-------------------Price Historic Chart
        
        self.fig = mpf.figure(style='default',figsize=(6, 4.4))
        self.fig.set_facecolor("#F0F0F0")
        self.ax = self.fig.subplots()
        self.ax.set_title("Historic Price", fontsize=12)
        self.ax.set_ylabel("Price", weight='normal', fontsize=9)
        self.ax.set_facecolor("white")
        self.ax.grid(color='lightgrey', linestyle='dashed')
        self.ax.tick_params(labelsize=9)
        
        self.graph = FigureCanvasTkAgg(self.fig, master=frm2)
        self.graph.get_tk_widget().pack(expand=True, fill=tk.BOTH)
        
        self.update_price()
        
    def crypto_selected(self, event):
        self.SELECTED = True
        self.table.delete(*self.table.get_children())
        
        self.coin = self.diminutivos.get(self.cboToken.get())
        
        token_data = yf.Ticker(self.coin)
        df = token_data.history(period='1mo')
        
        contador = 0
        
        for date, openn, close in zip(df.index.strftime('%d-%m-%Y'),df['Open'],df['Close']):
            if contador % 2 == 0:
                self.table.insert("", tk.END, text=date, values=[f"{openn:>27,.2f}", f"{close:>27,.2f}"], tags='par')
                contador+=1
            else:
                self.table.insert("", tk.END, text=date, values=[f"{openn:>27,.2f}", f"{close:>27,.2f}"], tags='impar')
                contador+=1
        
        self.table.tag_configure('par',background='light grey')
        self.table.tag_configure('impar',background='white')    
        self.ax.cla()
        self.ax.set_title(f"{self.cboToken.get()} Historic Price", fontsize=12)
        self.ax.set_ylabel("Price", weight='normal', fontsize=9)
        self.ax.grid(linestyle='dashed')
        self.ax.tick_params(labelsize=9)
        
        mc = mpf.make_marketcolors(up='g',down='r')
        s  = mpf.make_mpf_style(marketcolors=mc)
        mpf.plot(df,ax=self.ax,type='candle',style=s)
        
        self.graph.draw()
    
    def update_price(self):
        if self.SELECTED:
            URL = f"https://api.coinbase.com/v2/prices/{self.coin}/spot"
            r = requests.get(URL)
            data = r.json()
            
            self.act_valor = float(data['data']['amount'])
            
            if self.act_valor >= self.ant_valor:
                self.lblCash.config(text=f"{float(data['data']['amount']):,.2f} USD", fg='green')
                try:
                    self.lblsmall.config(text=f"{(self.act_valor - self.ant_valor):.2f} {(self.act_valor - self.ant_valor)/self.ant_valor:.2f}%", fg='green')
                except:
                    pass
            else:
                self.lblCash.config(text=f"{float(data['data']['amount']):,.2f} USD", fg='red')
                try:
                    self.lblsmall.config(text=f"{(self.act_valor - self.ant_valor):.2f} {(self.act_valor - self.ant_valor)/self.ant_valor:.2f}%", fg='red')
                except:
                    pass
            self.ant_valor = self.act_valor
        
        self.after(5000, self.update_price)
        
            
        
app = App().mainloop()

