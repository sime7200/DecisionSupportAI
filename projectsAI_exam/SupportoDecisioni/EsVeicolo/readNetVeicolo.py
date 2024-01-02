import pysmile
import pysmile_license

net = pysmile.Network()
net.read_file("veicoloAutonomoUnrolled.xdsl")
ris = ""
while ris != "Si" and ris != "No" and ris != "si" and ris != "no":
    ris = input("Visualizzare tutti i nodi presenti nella rete? [Si/No]\n")
    if(ris=="Si" or ris=="si"):
        h = net.get_first_node()
        print("\nElenco dei nodi nella rete:")
        while (h >= 0):
            print(net.get_node_id(h))
            h = net.get_next_node(h)
print("\nStep 0")
print("Caricamento rete...")
net.update_beliefs()
posizione = net.get_node_value("Posizione_rilevata")
print("Il sensore di posizione ha rilevato che il veicolo si trova: ")
print("-> A sinistra con una probabilità di " + str(posizione[0]) + 
      "\n-> Al centro con una probabilità di " + str(posizione[1]) +
      "\n-> A destra con una probabilità di " + str(posizione[2]) + "\n")
ev = ""
while ev != "1" and ev != "2" and ev != "3":
    ev = input("Inserire evidenza: 1=sinistra, 2=centro, 3=destra. [1/2/3]\n")
    if ev == "1":
        net.set_evidence("Posizione_rilevata", "Left")
    elif ev == "2":
        net.set_evidence("Posizione_rilevata", "Center")
    elif ev == "3":
        net.set_evidence("Posizione_rilevata", "Right")
print("Caricamento...")
net.update_beliefs()

dir = ""
while dir != "1" and dir != "2" and dir != "3":
    dir = input("Selezionare decisione: inserire 1 se si vuole che il veicolo vada a sinistra, 2 per rimanere dove si è, 3 a destra.\n")
    if dir == "1":
        net.set_evidence("Decisione_azione", "Left")
    elif dir == "2":
        net.set_evidence("Decisione_azione", "Stay")
    elif dir == "3":
        net.set_evidence("Decisione_azione", "Right")
print("\nCaricamento...")
net.update_beliefs()


for i in range(4):
    print("\nStep " + str(i+1))
    nome = "Posizione_rilevata" + "_" + str(i+1)
    posizione = net.get_node_value(nome)
    print("Il sensore di posizione ha rilevato che il veicolo si trova: ")
    print("-> A sinistra con una probabilità di " + str(posizione[0]) + 
      "\n-> Al centro con una probabilità di " + str(posizione[1]) +
      "\n-> A destra con una probabilità di " + str(posizione[2]) + "\n")
    ev = ""
    while ev != "1" and ev != "2" and ev != "3":
        ev = input("Inserire evidenza: 1=sinistra, 2=centro, 3=destra. [1/2/3]\n")
        if ev == "1":
            net.set_evidence(nome, "Left")
        elif ev == "2":
            net.set_evidence(nome, "Center")
        elif ev == "3":
            net.set_evidence(nome, "Right")
    print("Caricamento...")
    net.update_beliefs()

    nodo_dec = "Decisione_azione" + "_" + str(i+1)
    dir = ""
    while dir != "1" and dir != "2" and dir != "3":
        dir = input("Selezionare decisione: inserire 1 se si vuole che il veicolo vada a sinistra, 2 per rimanere dove si è, 3 a destra.\n")
        if dir == "1":
            net.set_evidence(nodo_dec, "Left")
        elif dir == "2":
            net.set_evidence(nodo_dec, "Stay")
        elif dir == "3":
            net.set_evidence(nodo_dec, "Right")
    print("\nCaricamento...")
    net.update_beliefs()

pos_fin = net.get_node_value("Posizione_finale")
print("Probabilità della posizione finale: " + str(pos_fin))
print("Sinistra -> " + str(pos_fin[0]) + "\n" +
      "Centro -> " + str(pos_fin[1]) + "\n" +
      "Destra -> " + str(pos_fin[2]) + "\n")
ut = net.get_node_value("Ut_finale")
print("L'utilità finale è: " + str(ut[0]) + "\n\n")

#posizione1 = net.get_node_value("Posizione_rilevata_1")
#print(posizione1)


