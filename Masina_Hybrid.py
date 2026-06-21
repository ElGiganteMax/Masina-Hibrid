from baterie import Baterie
from rezervor import Rezervor


class MasinaHibrid:
    """
    Reprezintă o mașină hibridă, formată dintr-o baterie (kWh) și un
    rezervor de combustibil (L). Gestionează modul de rulare
    (Electric / Hibrid / Benzina) și simulează consumul pe distanțe parcurse.
    """

    MODURI_VALIDE = ["Hibrid", "Electric", "Benzina"]

    def __init__(self, capacitate_baterie, consum_benzina, rezervor=None):
        # bateria este acum un obiect Baterie, nu doar un numar
        self.baterie = Baterie(capacitate_baterie, capacitate_baterie)
        self.consum_benzina_l_100km = consum_benzina
        self.rezervor = rezervor if rezervor is not None else Rezervor(50, 50)

        self.mod_rulare = "Hibrid"
        self.drum_factor = 1  # multiplicator in functie de tipul de drum (oras/national/autostrada)

        self.km_totali = 0
        self.km_electric = 0
        self.km_termic = 0

        self.istoric_drumuri = []

    # ---------------- MOD DE RULARE ----------------

    def schimba_mod(self, mod):
        if mod in self.MODURI_VALIDE:
            self.mod_rulare = mod
            mesaj = f"Modul de rulare a fost schimbat în: {self.mod_rulare}"
        else:
            mesaj = f"Mod invalid! Moduri acceptate: {', '.join(self.MODURI_VALIDE)}"

        print(mesaj)
        return mesaj

    def seteaza_drum_factor(self, factor):
        """Folosit de interfata grafica pentru a regla consumul in functie de tipul de drum."""
        self.drum_factor = factor

    # ---------------- BATERIE ----------------

    def incarca_baterie(self, kwh):
        self.baterie.incarca(kwh)
        mesaj = f"Bateria a fost încărcată la {self.baterie.nivel_curent:.2f} kWh."
        print(mesaj)
        return mesaj

    # ---------------- SIMULARE DRUM ----------------

    def simuleaza_drum(self, distanta, viteza):
        """
        Simulează parcurgerea unei distanțe (km) la o anumită viteză (km/h).
        Consumă baterie și/sau combustibil in functie de mod_rulare si
        actualizeaza km_totali / km_electric / km_termic / rezervor.
        Returneaza un mesaj descriptiv (util pentru afisare in GUI sau consola).
        """

        self.km_totali += distanta
        penalizare_viteza = 1.2 if viteza > 100 else 1.0

        if self.mod_rulare == "Electric":
            mesaj = self._ruleaza_electric(distanta, penalizare_viteza)

        elif self.mod_rulare == "Benzina":
            mesaj = self._ruleaza_benzina(distanta, penalizare_viteza)

        else:  # Hibrid
            mesaj = self._ruleaza_hibrid(distanta, penalizare_viteza)

        self.istoric_drumuri.append({
            "distanta": distanta,
            "viteza": viteza,
            "mod": self.mod_rulare
        })

        print(mesaj)
        return mesaj

    def _ruleaza_electric(self, distanta, penalizare_viteza):
        self.km_electric += distanta

        energie_necesara = (distanta / 100) * 15 * self.drum_factor * penalizare_viteza
        self.baterie.consuma(energie_necesara)

        mesaj = (
            f"Ai parcurs {distanta} km în mod Electric. "
            f"Baterie rămasă: {self.baterie.nivel_curent:.2f} kWh."
        )

        if self.baterie.nivel_curent <= 0:
            self.mod_rulare = "Benzina"
            mesaj += " Bateria s-a descărcat! Trecere automată pe Benzină."

        return mesaj

    def _ruleaza_benzina(self, distanta, penalizare_viteza):
        self.km_termic += distanta

        consum_real = self.consum_benzina_l_100km * self.drum_factor * penalizare_viteza
        self.rezervor.consuma_functie_distanta(distanta, consum_real)
        benzina_consumata = (distanta / 100) * consum_real

        return (
            f"Ai parcurs {distanta} km în mod Benzină. "
            f"Ai consumat {benzina_consumata:.2f} litri "
            f"(rezervor: {self.rezervor.combustibil_curent:.1f} L)."
        )

    def _ruleaza_hibrid(self, distanta, penalizare_viteza):
        self.km_electric += distanta * 0.5
        self.km_termic += distanta * 0.5

        energie_necesara = (distanta / 100) * 7.5 * self.drum_factor * penalizare_viteza
        self.baterie.consuma(energie_necesara)

        consum_real = (self.consum_benzina_l_100km / 2) * self.drum_factor * penalizare_viteza
        self.rezervor.consuma_functie_distanta(distanta, consum_real)
        benzina_consumata = (distanta / 100) * consum_real

        return (
            f"Ai parcurs {distanta} km în mod Hibrid. "
            f"Consum estimat: {benzina_consumata:.2f} litri și "
            f"{energie_necesara:.2f} kWh "
            f"(rezervor: {self.rezervor.combustibil_curent:.1f} L)."
        )

    # ---------------- STATISTICI / RAPOARTE ----------------

    def afiseaza_status(self):
        mesaj = (
            f"Mod: {self.mod_rulare} | "
            f"Baterie: {self.baterie.nivel_curent:.1f}/{self.baterie.capacitate} kWh | "
            f"Combustibil: {self.rezervor.combustibil_curent:.1f}/{self.rezervor.capacitate} L"
        )
        print(mesaj)
        return mesaj

    def afiseaza_statistici(self):
        procent_baterie = (self.baterie.nivel_curent / self.baterie.capacitate) * 100

        linii = ["===== STATISTICI =====", f"Km totali: {self.km_totali}",
                 f"Km electrici: {self.km_electric:.1f}", f"Km termici: {self.km_termic:.1f}"]

        if self.km_totali > 0:
            procent_electric = (self.km_electric / self.km_totali) * 100
            linii.append(f"Rulare electrică: {procent_electric:.1f}%")

        linii.append(
            f"Baterie rămasă: {self.baterie.nivel_curent:.2f} kWh ({procent_baterie:.1f}%)"
        )
        linii.append("======================")

        mesaj = "\n".join(linii)
        print(mesaj)
        return mesaj

    def raport_eco(self):
        if self.km_totali == 0:
            mesaj = "Nu există date."
            print(mesaj)
            return mesaj

        procent = (self.km_electric / self.km_totali) * 100

        if procent >= 70:
            verdict = "🌿 Stil de condus foarte eficient!"
        elif procent >= 40:
            verdict = "🍂 Stil de condus moderat."
        else:
            verdict = "⚠️ Motorul termic este folosit frecvent."

        mesaj = f"===== RAPORT ECO =====\n{verdict}\n======================"
        print(mesaj)
        return mesaj

    def afiseaza_istoric(self):
        if not self.istoric_drumuri:
            mesaj = "Nu există drumuri înregistrate."
            print(mesaj)
            return mesaj

        linii = ["===== ISTORIC DRUMURI ====="]
        for nr, drum in enumerate(self.istoric_drumuri, start=1):
            linii.append(f"{nr}. {drum['distanta']} km | {drum['viteza']} km/h | {drum['mod']}")

        mesaj = "\n".join(linii)
        print(mesaj)
        return mesaj


if __name__ == "__main__":
    rezervor = Rezervor(50, 40)
    masina_mea = MasinaHibrid(
        capacitate_baterie=12.0,
        consum_benzina=5.5,
        rezervor=rezervor
    )

    masina_mea.schimba_mod("Electric")
    masina_mea.simuleaza_drum(40, 60)

    masina_mea.schimba_mod("Benzina")
    masina_mea.simuleaza_drum(30, 120)

    masina_mea.incarca_baterie(3)

    masina_mea.afiseaza_statistici()
    masina_mea.raport_eco()
    masina_mea.afiseaza_istoric()

    rezervor.afiseaza_nivel()
