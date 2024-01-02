import pysmile
import pysmile_license

net = pysmile.Network()
net.read_file("NetworkAzienda.xdsl")
h = net.get_first_node()
print("\nElenco dei nodi nella rete:\n")
while (h >= 0):
    print(net.get_node_id(h))
    h = net.get_next_node(h)

print("\nE' possibile prendere 2 decisioni: Fare_ricerca o/e Migliora_qualita.")
decFare_ric = input("Si vuole effettuare una ricerca di mercato? Il costo è di 1000$ [Si/No]\n")
while decFare_ric != "Si" and decFare_ric != "No" and decFare_ric != "si" and decFare_ric != "no":
    decFare_ric = input("Si vuole effettuare una ricerca di mercato? [Si/No]\n")

if decFare_ric == "Si" or decFare_ric == "si":
    net.set_evidence("Fare_ricerca", "Si")
    net.update_beliefs()

    print("Ora inserire il risultato della ricerca di mercato sapendo che l'affidabilità è del 90%")
    ris_ricerca = input("Inserire 1 se la domanda di mercato è alta, 2 se bassa: ")
    while ris_ricerca != "1" and ris_ricerca != "2":
        ris_ricerca = input("Inserire 1 se la domanda di mercato è alta, 2 se bassa: ")

    if ris_ricerca == "1":
        net.set_evidence("Risultato_ricerca", "Alta")
    else: 
        net.set_evidence("Risultato_ricerca", "Bassa")
    net.update_beliefs()

else:
    net.set_evidence("Fare_ricerca", "No")
    net.update_beliefs()

decMigliora_qual = input("Si vuole migliorare la qualità del prodotto? Il costo è di 5000$ [Si/No]\n")
while decMigliora_qual != "Si" and decMigliora_qual != "No" and decMigliora_qual != "si" and decMigliora_qual != "no":
    decMigliora_qual = input("Si vuole migliorare la qualità del prodotto? Il costo è di 5000$ [Si/No]\n")
if decMigliora_qual == "Si" or decMigliora_qual == "si":
    net.set_evidence("Migliora_qualita", "Si")
else:
    net.set_evidence("Migliora_qualita", "No")
net.update_beliefs()

ut_profitto = net.get_node_value("Valore_profitto")
print("Il valore del profitto è " + str(ut_profitto))

ut = net.get_node_value("Utilità_finale")
print("\nSapendo che la decisione di fare una ricerca di mercato è " + decFare_ric
      + " e la decisione di migliorare il prodotto è " + decMigliora_qual 
      + ", l'utilità finale è " + str(ut) + "\n\n")