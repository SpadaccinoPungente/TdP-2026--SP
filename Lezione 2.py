# Scriviamo un codice python che modelli un semplice
# gestionale aziendale. Dovremo prevedere la possibilità di
# definire entità che modellano i prodotti, i clienti,
# offrire interfacce per calcolare i prezzi, eventualmente
# scontati, ...

class Prodotto:
    aliquota_iva = 0.22 # variabile di classe -- ovvero è la stessa per tutte le istanze che verranno create.

    def __init__(self, name: str, price: float, quantity: int, supplier = None):
        self.name = name
        self._price = None # qua mi riferisco alla variabile protetta, voglio fare controlli perciò metto None
        self.price = price # facendo così mi assicurerò che non price non possa essere negativa
        self.quantity = quantity
        self.supplier = supplier

    def valore_netto(self):
        return self._price*self.quantity

    def valore_lordo(self):
        netto = self.valore_netto()
        lordo = netto*(1+self.aliquota_iva)
        return lordo

    @classmethod
    def costruttore_con_quantita_uno(cls, name: str, price: float, supplier: str):
        return cls(name, price, 1, supplier) # aggiunto io la return perché sotto assegniamo a p3!

    @staticmethod
    def applica_sconto(prezzo, percentuale):
        return prezzo*(1-percentuale)

    @property
    def price(self): # eq. getter
        return self._price
    @price.setter # posso crearlo solo una volta definito property, si attiva quando scrivo self.price = val
    def price(self, valore):
        if valore < 0:
            raise ValueError("Attenzione, il prezzo non può essere negativo.")
        self._price = valore

    def __str__(self): # esattamente equivalente a toString() di Java
        return f"{self.name} - disponibili {self.quantity} a {self.price}$"
    # se è stato definito, facendo la print dell'oggetto vado direttamente a utilizzare questo metodo

    def __repr__(self): # simile a __str__ ma orientato al programmatore (come fosse la struttura del costruttore)
        return f"Prodotto(nome={self.name}, price={self.price}, disponibili={self.quantity}, supplier={self.supplier})"
    # questo viene utilizzato ad esempio in debug mode, per vedere cosa c'è all'interno delle variabili
    # se non è definito vedo l'opzione di default che stampa l'indirizzo della cella di memoria dove l'oggetto si trova

    def __eq__(self, other: object): # analogo al metodo equals() di Java, permette di confrontare le istanze (implementa ==)
        if not isinstance(other, Prodotto): # analogo instanceof di Java
            return NotImplemented
        return self.name == other.name and self.price == other.price and self.quantity==other.quantity and self.supplier == other.supplier

    def __lt__(self, other: "Prodotto") -> bool : # questo somiglia a compareTo() (lt = lower than) Python deduce gli altri metodi per confrontare
        return self.price < other.price # ritorna un valore booleano (true se self < other, false altrimenti)
        # other: "Prodotto" che cosa fa? Specifica che other debba essere di tipo Prodotto
        # --> Perché ""? compilatore sembra interpretarlo allo stesso modo sia con che senza
        # -> bool anticipa al compilatore che il valore di ritorno è booleano (non necessario)

    def prezzo_finale(self) -> float:
        return self.price*(1+self.aliquota_iva)

class ProdottoScontato(Prodotto): # ereditarietà -> ProdottoScontato è figlia di Prodotto
    # in Python anche possibile ereditare da più classi, non lo faremo

    def __init__(self, name: str, price: float, quantity: int, supplier: str, sconto_percento: float):
        # almeno gli stessi argomenti di Prodotto, parametri di default dopo quelli non-default (dà errore)
        # Prodotto.__init__(self, name, price, quantity, supplier) # perchè qua self e sotto no?
        super().__init__(name, price, quantity, supplier) # equivalente
        self.sconto_percento = sconto_percento # posso aggiungere attributi

    def prezzo_finale(self) -> float: # -> stesso nome, cose diverse: polimorfismo!!!
        return self.valore_lordo()*(1-self.sconto_percento/100) # sconto in percentuale

class Servizio(Prodotto): # eredita da prodotto ma non è qualcosa che vendo, la adatto a nuovi obiettivi
    def __init__(self, name: str, tariffa_oraria: float, ore: int):
        super().__init__(name=name, price=tariffa_oraria, quantity=1, supplier=None)
        self.ore = ore

    def prezzo_finale(self) -> float: # -> stesso nome, cose diverse: polimorfismo!!!
        return self.price*self.ore

myproduct1 = Prodotto(name = "Laptop", price = 1200.0, quantity=12, supplier="ABC")

print(f"Nome prodotto: {myproduct1.name} - prezzo: {myproduct1.price}")
print(f"Il totale lordo di myproduct1 è {myproduct1.valore_lordo()}") # uso un metodo di istanza

p3 = Prodotto.costruttore_con_quantita_uno("Auricolari", 200.0, "ABC") # modo per chiamare un metodo di classe

print(f"Prezzo scontato di myproduct1 {Prodotto.applica_sconto(myproduct1.price, 0.15)}")# modo per chiamare un metodo statico.

myproduct2 = Prodotto("Mouse", 10, 25, "CDE")
print(f"Nome prodotto: {myproduct2.name} - prezzo: {myproduct2.price}")

# se cambio il valore di una variabile di classe, vale per tutte le istanze:
print(f"Valore lordo di myproduct1: {myproduct1.valore_lordo()}")
Prodotto.aliquota_iva = 0.24
print(f"Valore lordo di myproduct1: {myproduct1.valore_lordo()}")

# print(p3) # print(myproduct1)

p_a = Prodotto("Laptop", price=1200, quantity=12, supplier="ABC")
p_b = Prodotto("Mouse", 10, 14, "CDE")

print("myproduct1 == p_a?", myproduct1 == p_a) # vado a chiamare __eq__, mi aspetto True
print("p_a == p_b?", p_a == p_b) # mi aspetto False

# andiamo a utilizzare __lt__:
mylist = [p_a,p_b, myproduct1]
mylist.sort() # mylist.sort(reverse=True) # mylist.reverse()
print("Lista di prodotti ordinata:")
for p in mylist:
    print(f"- {p}")
# la lista viene ordinata in ordine crescente di prezzo per come ho costruito __lt__

# Duck Typing:

my_product_scontato = ProdottoScontato(name="Auricolari", price=320, quantity=1, supplier="ABC", sconto_percento=10)
my_service = Servizio(name="Consulenza", tariffa_oraria=100.0, ore=3)

mylist.append(my_product_scontato)
mylist.append(my_service) # così facendo, gli elementi della lista non sono omogenei (ammesso)
# tuttavia, implementano i metodi necessari affinché questo non sia un problema

mylist.sort(reverse=True)

for elem in mylist:
    print(elem.name, " -> ", elem.prezzo_finale())

print("---------------------------------------------------------------------------------------------------------------")

# definire una classe Abbonamento che abbia come attributi: nome, prezzo_mensile, mesi
# Abbonamento dovrà avere un metodo per calcolare il prezzo finale ottenuto come prezzo_mensile*mesi

class Abbonamento:
    def __init__(self, nome: str, prezzo_mensile: float, mesi: int):
        self.name = nome
        self.prezzo_mensile = prezzo_mensile
        self.mesi = mesi
    def prezzo_finale(self) -> float:
        return self.prezzo_mensile*self.mesi

abb = Abbonamento("Software gestionale", prezzo_mensile=30, mesi=24)
mylist.append(abb) # in questo momento dà warning perché abb è di tipo diverso da Prodotto (no ereditarietà)
# secondo il principio del duck typing, il codice comunque funzionerà come inteso
for elem in mylist:
    print(elem.name, " -> ", elem.prezzo_finale())

def calcola_totale(elementi):
    tot = 0
    for e in elementi:
        tot += e.prezzo_finale()
    return tot

print(f"Il totale è: {calcola_totale(mylist)}")

# ma come mi assicuro di comunicare a tutti quali sono i metodi che ci aspettiamo siano implementati? --> protocollo!

from typing import Protocol

class HaPrezzoFinale(Protocol):
    def prezzo_finale(self) -> float:
        ... # simile a pass (che metto quando devo poi implementare), sono un placeholder (non devo davvero scrivere qua)

def calcola_totale(elementi: list[HaPrezzoFinale]) -> float:
    # vuole ricordare la struttura array[int]
    # intende che il tipo degli elementi non è noto a priori ma solo che implementano prezzo_finale()
    return sum(e.prezzo_finale() for e in elementi) # comprehension

print(f"Il totale è: {calcola_totale(mylist)}")

print("---------------------------------------------------------------------------------------------------------------")

from dataclasses import dataclass

@dataclass # decoratore che dice che questa classe contiene solo dati
class ProdottoRecord:
    # non ho bisogno di fare il costruttore, scrivo più semplicemente e i dunder vengono generati automaticamente
    # classe automaticamente civile
    name: str
    prezzo_unitario: float

@dataclass
class ClienteRecord:
    name: str
    email: str
    categoria: str

# possiamo anche aggiungere dei metodi ad hoc:
@dataclass
class RigaOrdine:
    prodotto: ProdottoRecord
    quantita: int

    def totale_riga(self):
        return self.prodotto.prezzo_unitario * self.quantita # costo della riga dell'ordine

@dataclass
class Ordine:
    righe: list[RigaOrdine] # com'è la sintassi qui?
    cliente: ClienteRecord

    def totale_netto(self):
        return sum(r.totale_riga() for r in self.righe)

    def totale_lordo(self, aliquota_iva):
        return self.totale_netto()*(1+aliquota_iva)

    def numero_righe(self):
        return len(self.righe)

@dataclass # anche con dataclass è possibile utilizzare l'ereditarietà
class OrdineConSconto(Ordine):
    sconto_percentuale: float

    def totale_scontato(self):
        return self.totale_lordo()*(1-self.sconto_percentuale)

    def totale_netto(self): # il bersaglio indica gli override (freccia in alto se specifica, in basso se specificato)
        netto_base = super().totale_netto()
        return netto_base*(1-self.sconto_percentuale)

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

# scrivere una classe Cliente che abbia i campi "nome", "email", "categoria" ("Gold", "Silver", "Bronze")
# vorremmo che questa classe avesse un metodo che chiamiamo "descrizione"
# che deve restituire una stringa formattata ad esempio:
# "Cliente Fulvio Bianchi (Gold) - fulvio@google.com"

# si modifichi la classe cliente in maniera tale che la proprietà categoria sia "protetta"
# e accetti solo ("Gold", "Silver", "Bronze")

class Cliente:
    def __init__(self, nome, mail, categoria):
        self.nome = nome
        self.mail = mail
        self._categoria = None
        self.categoria = categoria

    @property
    def categoria(self):
        return self._categoria

    @categoria.setter
    def categoria(self, categoria):
        categorie_valide = {"Gold", "Silver", "Bronze"} # questo rappresenta un set (se fosse con ":" anche dizionario)
        if categoria not in categorie_valide:
            raise ValueError("Attenzione, categoria non valida. Scegliere fra Gold, Silver, Bronze")
        self._categoria = categoria

    def descrizione(self): #to_string
        # "Cliente Fulvio Bianchi (Gold) - fulvio@google.com"
        return f"Cliente {self.nome} ({self.categoria}) - {self.mail}"

c1 = Cliente("Mario Bianchi", "mario.bianchi@polito.it", "Gold")
# c2 = Cliente("Carlo Masone", "carlo.masone@polito.it", "Platinum") # la categoria "Platinum" non esiste
print(c1.descrizione())


# Codice lungo ma che "fa poco" --> voglio suddividerlo in più file --> uso i moduli! Collezioni di classi, funzioni, variabili, ...
# Stesso modo in cui funzionano le librerie, o moduli tipo dataclass
# possono essere propri o pubblici scaricati