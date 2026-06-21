class Baterie:
    def __init__(self, capacitate, nivel_curent):
        self.capacitate = capacitate
        self.nivel_curent = nivel_curent

    def consuma(self, procent):
        self.nivel_curent -= procent

        if self.nivel_curent < 0:
            self.nivel_curent = 0

    def incarca(self, procent):
        self.nivel_curent += procent

        if self.nivel_curent > self.capacitate:
            self.nivel_curent = self.capacitate

    def afiseaza_nivel(self):
        print(f"Baterie: {self.nivel_curent}% / {self.capacitate}%")

if __name__ == "__main__":
    baterie = Baterie(100, 80)

    baterie.afiseaza_nivel()

    baterie.consuma(10)
    baterie.afiseaza_nivel()

    baterie.incarca(15)
    baterie.afiseaza_nivel()