# Scriviamo un codice Python che modelli un semplice gestionale aziendale. Dovremo prevedere la possbilità di definire entità che modellano prodotti
# i clienti, offrire interfacce per calcolare prezzi, eventuali sconti...

prodotto1_nome = "Laptop"
prodotto1_prezzo = 1200.0
prodotto1_quantità = 5

prodotto2_nome = "Mouse"
prodotto2_prezzo = 12.0
prodotto2_quantità = 15

valore_magazzino = prodotto1_prezzo * prodotto1_quantità + prodotto2_prezzo * prodotto2_quantità

print(f"Valore totale magazzino : {valore_magazzino}")


# Per creare lo stesso con meno righe, faccio una classe:

class Prodotto:
    aliquota_iva = 0.22  # variabile di classe --> rimane la stessa per tutte le istanze create

    def __init__(self, name: str, price: float, quantity: int,
                 supplier=None):  # ..., my_var = ...) --> valore di default
        self.name = name
        self.price = price
        self.quantity = quantity
        self.supplier = supplier

    def valore_netto(self):
        return self.quantity * self.price

    def valore_lordo(self):
        netto = self.valore_netto()  # self.price*self.quantity
        lordo = netto * (1 + self.aliquota_iva)
        return lordo

    @classmethod  # decoratore, messo così prima di un metodo lo rende metodo di classe e non d'istanza (lo creo una volta sola, singleton?)
    def costruttore_con_quantità_uno(cls, name: str, price: float, supplier: str):
        cls(name, price, 1, supplier)  # cls riferimento alla classe, sto richimando __init__()

    @staticmethod  # metodo statico
    def applica_sconto(price, percentage):
        return price * (1 - percentage)
    # essendo metodo statico non passo né self nè cls!


myproduct1 = Prodotto("Laptop", 1200, 12,
                      "ABC")  # myproduct1 = Prodotto(name: "Laptop", price: 1200, quantity: 12, supplier: "ABC")
# ordine rilevante, posso riferirmi direttamente alla variabile con ad es. supplier = "ABC"

print(f"Nome prodotto: {myproduct1.name} - prezzo: {myproduct1.price}")
print(f"Il totale lordo di myproduct1 è: {myproduct1.valore_lordo()}")  # uso metodo d'istanza

p3 = Prodotto.costruttore_con_quantità_uno(name:"Auricolari", price: 200.0, supplieri: "ABC")
print(f"Prezzo scontato prodotto 1: {myproduct1.applica_sconto(myproduct1.price, percentuale: 0.15)}")

myproduct2 = Prodotto("Mouse", 10, 25, "CDE")

print(f"Nome prodotto: {myproduct2.name} - prezzo: {myproduct2.price}")


# Scrivere una classe Cliente con campi nome, email, categoria (gold, silver, bronze)
# Vorremmo un metodo che chiamiamo "descrizione" che deve restituire una stringa formattata in un certo modo (ad es. Cliente Fulvio Bianchi (Gold) - fulvio@google.com)

class Cliente:
    def __init__(self, name: str, email: str, category: str):
        self.name = name
        self.email = email
        self.category = category

    def descrizione(self):
        return f"Cliente {self.name} ({self.category} - {self.mail})"  # "Cliente "+self.name+"("+self.category+")"+" - "+self.email


cliente1 = Cliente("Fulvio Bianchi", "fulvio@google.com", "Gold")
cliente2 = Cliente("Mario Bianchi", "mario.bianchi@polito.it", "Gold")

print(Cliente.descrizione(cliente1) + "\n")
print(Cliente.descrizione(cliente2))


