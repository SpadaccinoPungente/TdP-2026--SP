"""
# LEZIONE 1:
# Scriviamo un codice python che modelli un semplice
# gestionale aziendale. Dovremo prevedere la possibilità di
# definire entità che modellano i prodotti, i clienti,
# offrire interfacce per calcolare i prezzi, eventualmente
# scontati, ...

prodotto1_nome = "Laptop"
prodotto1_prezzo = 1200.0
prodotto1_quantita = 5

prodotto2_nome = "Mouse"
prodotto2_prezzo = 12.0
prodotto2_quantita = 15

valore_magazzino = prodotto1_prezzo * prodotto1_quantita + prodotto2_prezzo * prodotto2_quantita

print(f"Valore totale magazzino : {valore_magazzino}")

# per creare lo stesso con meno righe, faccio una classe:

class Prodotto:
    aliquota_iva = 0.22 # variabile di classe -- ovvero è la stessa per tutte le istanze che verranno create.

    def __init__(self, name: str, price: float, quantity: int, supplier = None): # ..., my_var = ...) --> valore di default
        self.name = name
        self.price = price
        self.quantity = quantity
        self.supplier = supplier

    def valore_netto(self):
        return self.price*self.quantity

    def valore_lordo(self):
        netto = self.valore_netto() # self.price*self.quantity
        lordo = netto*(1+self.aliquota_iva)
        return lordo

    @classmethod # decoratore, messo così prima di un metodo lo rende metodo di classe e non d'istanza (lo creo una volta sola, singleton?)
    def costruttore_con_quantita_uno(cls, name: str, price: float, supplier: str):
        cls(name, price, 1, supplier) # cls riferimento alla classe, sto richiamando __init__()

    @staticmethod # metodo statico
    def applica_sconto(prezzo, percentuale): # essendo metodo statico non passo né self nè cls!
        return prezzo*(1-percentuale)

myproduct1 = Prodotto(name = "Laptop", price = 1200.0, quantity=12, supplier="ABC")
# (??) myproduct1 = Prodotto(name: "Laptop", price: 1200, quantity: 12, supplier: "ABC")
# ordine rilevante, posso riferirmi direttamente alla variabile con ad es. supplier = "ABC"

print(f"Nome prodotto: {myproduct1.name} - prezzo: {myproduct1.price}")

print(f"Il totale lordo di myproduct1 è {myproduct1.valore_lordo()}") # uso un metodo di istanza
p3 = Prodotto.costruttore_con_quantita_uno("Auricolari", 200.0, "ABC") # modo per chiamare un metodo di classe
print(f"Prezzo scontato di myproduct1 {Prodotto.applica_sconto(myproduct1.price, 0.15)}") # modo per chiamare un metodo statico

myproduct2 = Prodotto("Mouse", 10, 25, "CDE")
print(f"Nome prodotto: {myproduct2.name} - prezzo: {myproduct2.price}")

# Scrivere una classe Cliente che abbia i campi "nome", "email", "categoria" ("Gold", "Silver", "Bronze").
# Vorremmo che questa classe avesse un metodo che chiamiamo "descrizione"
# che deve restituire una stringa formattata ad esempio
# "Cliente Fulvio Bianchi (Gold) - fulvio@google.com"

class Cliente:
    def __init__(self, nome, mail, categoria):
        self.nome = nome
        self.mail = mail
        self.categoria = categoria

    def descrizione(self): #to_string
        # "Cliente Fulvio Bianchi (Gold) - fulvio@google.com"
        return f"Cliente {self.nome} ({self.categoria}) - {self.mail}" # "Cliente "+self.name+"("+self.category+")"+" - "+self.email

c1 = Cliente("Mario Bianchi", "mario.bianchi@polito.it", "Gold")
print(c1.descrizione())
"""

# Scriviamo un codice python che modelli un semplice
# gestionale aziendale. Dovremo prevedere la possibilità di
# definire entità che modellano i prodotti, i clienti,
# offrire interfacce per calcolare i prezzi, eventualmente
# scontati, ...

from gestionale.vendite.ordini import Ordine, RigaOrdine, OrdineConSconto
from gestionale.core.prodotti import Prodotto, crea_prodotto_standard, ProdottoRecord
from gestionale.core.clienti import Cliente, ClienteRecord

print("===============================================================================================================")

p1 = Prodotto("Ebook Reader", 120.0, 1, "AAA")
p2 = crea_prodotto_standard("Tablet", 750)
print(p1)
print(p2)

"""
# modi per importare:
# 1)
from prodotti import ProdottoScontato
# 2)
from prodotti import ProdottoScontato as ps # rinomina la classe
p3 = ps("Auricolari", 230, 1, "ABC", 10)
# 3)
import prodotti # mi importa tutto ciò che c'è in prodotti
p4 = prodotti.ProdottoScontato("Auricolari", 230, 1, "ABC", 10)
# 4)
import prodotti as p # posso rinominarlo
p5 = p.ProdottoScontato("Auricolari", 230, 1, "ABC", 10)
"""

print("===============================================================================================================")

c1 = Cliente("Mario Rossi", "mail@gmail.com", "Gold")

print("---------------------------------------------------------------------------------------------------------------")

cliente1 = ClienteRecord("Mario Rossi", "mariorossi@example.com", "Gold")
p1 = ProdottoRecord("Laptop", 1200)
p2 = ProdottoRecord("Mouse", 20)

ordine = Ordine([RigaOrdine(p1, 2), RigaOrdine(p2, 10)], cliente1)
ordine_scontato = OrdineConSconto([RigaOrdine(p1, 2), RigaOrdine(p2, 10)], cliente1, 0.1) # parametri passati con ordine

print(ordine) # dataclass scrive automaticamente un __repr__ che è quello che viene mostrato
print("Numero di righe nell'ordine: ", ordine.numero_righe())
print("Totale netto: ", ordine.totale_netto())
print("Totale lordo (IVA 22%): ", ordine.totale_lordo(0.22))

print(ordine_scontato)
print("Totale netto scontato: ", ordine_scontato.totale_netto())
print("Totale lordo scontato: ", ordine_scontato.totale_lordo(0.22))
# totale_lordo() non esiste in OrdineConSconto, ma è definito in Ordine e richiama l'implementazione della super classe

print("---------------------------------------------------------------------------------------------------------------")

# Codice lungo ma che "fa poco" --> voglio suddividerlo in più file --> uso i moduli! Collezioni di classi, funzioni, variabili, ...
# Stesso modo in cui funzionano le librerie, o moduli tipo dataclass
# possono essere propri o pubblici scaricati

# da farsi poi mercoledì 4/3:
# nel package gestionale, scriviamo un modulo fatture.py che contenga:
# - una classe Fattura che contiene un Ordine, un numero fattura e una data
# - un metodo genera_fattura() che restituisce una stringa formattata con tutte le info della fattura