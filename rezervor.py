class Rezervor:
    def __init__(self, capacitate, combustibil_curent):    # creeaza un rezervor de exemplu rezervor = Rezervor(50, 40)
        # adica 50 litri capacitate si 40 litri combustibil      
        self.capacitate = capacitate
        self.combustibil_curent = combustibil_curent

    def consuma_functie_distanta(self, kilometri, consum_suta):                       # consuma -- vehiculul se deplaseaza dar cantitatea de combustibil scade
            # aflu scaderea volumului combustibilului in functie de distanta parcursa
        consumat = kilometri *consum_suta / 100
        self.combustibil_curent -= consumat
        if self.combustibil_curent < 0:
            self.combustibil_curent = 0

    def alimenteaza(self, cantitate):
        self.combustibil_curent += cantitate  # metoda - alimentewaza () adica se adauga combustibil
            #rezervor.alimenteaza(10) adica de la pompa s-au 'incarcat' 10 litri 
            # rezervor.alimenteaza(10)  35 litri --> 45 litri  

        if self.combustibil_curent > self.capacitate:
            self.combustibil_curent = self.capacitate

    def afiseaza_nivel(self):
        print(f"Combustibil: {self.combustibil_curent:.1f} L / {self.capacitate} L")
        # Metoda : afiseaza nivel() adica afiseaza cantitatea d e combustibil din rezervor

if __name__ == "__main__":
    rezervor = Rezervor(50, 40)

    rezervor.afiseaza_nivel()

    rezervor.consuma_functie_distanta(100, 5.5)
    rezervor.afiseaza_nivel()

    print(rezervor.combustibil_curent)
    rezervor.alimenteaza(10)
    rezervor.afiseaza_nivel()        