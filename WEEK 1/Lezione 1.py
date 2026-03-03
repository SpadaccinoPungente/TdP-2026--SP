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