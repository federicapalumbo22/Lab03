import csv
from operator import attrgetter

class Strumento:
    def __init__(self, codice_univoco, tipo, marca, anno_acquisto, valore):
        self.codice_univoco = codice_univoco
        self.tipo = tipo
        self.marca = marca
        self.anno_acquisto = anno_acquisto
        self.valore = valore

    def __str__(self):
        return f"{self.codice_univoco}: {self.tipo} {self.marca} ({self.anno_acquisto}) - {self.valore} euro"

class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati"""
        self.nome = nome
        self.responsabile = responsabile
        self.strumenti = {}
        self.prestiti = {}
        self.ultimo_id_strumento = 0
        self.ultimo_id_prestito = 0


    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""
        #creare gli oggetti corrispondenti
        try:
            with open(file_path, 'r', encoding='utf-8') as filestrumenti:
                reader = csv.reader(filestrumenti)
                for riga in reader:
                    if not riga:
                        continue
                    codice_univoco = riga[0]
                    numero_id = int(codice_univoco[1:])
                    tipo = riga[1]
                    marca = riga[2]
                    anno_acquisto = int(riga[3])
                    valore = float(riga[4])
                    self.strumenti[codice_univoco] = Strumento(codice_univoco, tipo, marca, anno_acquisto, valore)
                    if numero_id > self.ultimo_id_strumento:
                        self.ultimo_id_strumento = numero_id
        except FileNotFoundError:
            raise FileNotFoundError("File non trovato")

    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""
        self.ultimo_id_strumento += 1
        nuovo_codice = "S"+str(self.ultimo_id_strumento)
        nuovo_strumento = Strumento(nuovo_codice, tipo, marca, anno_acquisto, valore)
        self.strumenti[nuovo_codice] = nuovo_strumento
        return nuovo_strumento

    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""
        return sorted(self.strumenti.values(), key=attrgetter('marca'))

    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""
        if id_strumento not in self.strumenti:
            raise Exception("Errore: questo strumento non esiste")
        for prestito in self.prestiti.values():
            if prestito["id_strumento"] == id_strumento:
                raise Exception("Errore: strumento già in prestito")
        self.ultimo_id_prestito += 1
        codice_prestito = "P"+str(self.ultimo_id_prestito)
        nuovo_prestito = {"codice_prestito": codice_prestito,
                          "data": data,
                          "id_strumento": id_strumento,
                          "cognome_allievo": cognome_allievo}
        self.prestiti[codice_prestito] = nuovo_prestito
        return nuovo_prestito

    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto"""
        if id_prestito not in self.prestiti:
            raise Exception("Errore: codice prestito non valido")
        del self.prestiti[id_prestito]