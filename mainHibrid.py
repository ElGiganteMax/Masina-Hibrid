from rezervor import Rezervor
from Masina_Hybrid import MasinaHibrid


def meniu():

    rezervor = Rezervor(50, 40)

    masina = MasinaHibrid(
        capacitate_baterie=20,
        consum_benzina=6,
        rezervor=rezervor
    )

    while True:

        print("\n===== MENIU =====")
        print("1. Afiseaza status")
        print("2. Mod electric")
        print("3. Mod termic (benzina)")
        print("4. Mod hibrid")
        print("5. Simuleaza drum")
        print("6. Statistici")
        print("7. Raport eco")
        print("8. Istoric drumuri")
        print("9. Incarca bateria")
        print("0. Iesire")

        optiune = input("Alege: ")

        if optiune == "1":
            masina.afiseaza_status()

        elif optiune == "2":
            masina.schimba_mod("Electric")

        elif optiune == "3":
            masina.schimba_mod("Benzina")

        elif optiune == "4":
            masina.schimba_mod("Hibrid")

        elif optiune == "5":
            distanta = float(
                input("Distanta (km): ")
            )
            viteza = float(
                input("Viteza (km/h): ")
            )
            masina.simuleaza_drum(distanta, viteza)

        elif optiune == "6":
            masina.afiseaza_statistici()

        elif optiune == "7":
            masina.raport_eco()

        elif optiune == "8":
            masina.afiseaza_istoric()

        elif optiune == "9":
            kwh = float(
                input("Cati kWh incarci? ")
            )
            masina.incarca_baterie(kwh)

        elif optiune == "0":
            print("La revedere!")
            break

        else:
            print("Optiune invalida!")


if __name__ == "__main__":
    meniu()