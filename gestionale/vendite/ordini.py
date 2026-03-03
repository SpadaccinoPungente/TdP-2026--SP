from dataclasses import dataclass

from gestionale.core.clienti import ClienteRecord
from gestionale.core.prodotti import ProdottoRecord


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