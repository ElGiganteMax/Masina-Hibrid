# 🌿 Eco Driving Dashboard

Simulator pentru o mașină hibrid (electric / hibrid / benzină), scris în Python, cu programare orientată pe obiecte. Proiectul are două moduri de utilizare: o interfață grafică de tip dashboard auto și un meniu de consolă, ambele bazate pe aceeași logică de simulare.

## Descriere

Aplicația modelează comportamentul unei mașini hibrid pe parcursul unui drum: consumul de curent din baterie (kWh) și de combustibil (litri) variază în funcție de modul de rulare ales (Electric, Hibrid, Benzină), de tipul de drum (oraș, oraș aglomerat, drum național, autostradă) și de viteza de deplasare. Mașina trece automat pe Benzină dacă bateria se descarcă, iar utilizatorul primește un scor eco și un raport asupra stilului de condus.

## Funcționalități

- simulare drum cu consum de baterie și/sau combustibil, în funcție de modul de rulare ales
- trecere automată pe modul Benzină atunci când bateria se descarcă complet
- penalizare de consum pentru viteze peste 100 km/h
- factor de consum diferit în funcție de tipul de drum (oraș / oraș aglomerat / drum național / autostradă)
- statistici (km totali, km electrici, km termici, procent rulare electrică)
- raport eco, calculat din procentul de kilometri parcurși electric
- istoric al drumurilor simulate
- interfață grafică (dashboard) cu grafic live al combustibilului rămas
- meniu interactiv de consolă, cu aceleași funcționalități

## Structura proiectului

| Fișier | Descriere |
|---|---|
| `baterie.py` | Clasa `Baterie` — gestionează nivelul curent și capacitatea bateriei |
| `rezervor.py` | Clasa `Rezervor` — gestionează nivelul curent și capacitatea rezervorului de combustibil |
| `Masina_Hybrid.py` | Clasa `MasinaHibrid` — compune o `Baterie` și un `Rezervor`, conține toată logica de simulare, schimbare mod rulare, statistici și rapoarte |
| `mainHibrid.py` | Versiunea de consolă — meniu interactiv pentru control direct din terminal |
| `InterfataGrafica.py` | Versiunea grafică — dashboard interactiv construit cu CustomTkinter și un grafic live "fabricat" cu ajutorul Matplotlib |

## Cerințe

- Python 3.10+
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) — trebuie instalat doar pentru versiunea grafică
- [Matplotlib](https://matplotlib.org/) — trebuie instalat doar pentru versiunea grafică

Instalare dependențe:

```bash
customtkinter>=5.2.0
matplotlib>=3.7.0

```

## Rulare

**Versiunea grafică:**

```bash
python InterfataGrafica.py
```

Se alege tipul de drum din meniul derulant, se reglează accelerația din slider, apoi se apasă „Pornește Mașina” și „Continuă Drumul” pentru a simula deplasarea. Daca soferul/ utilizatorul accelereaza "cu blandete" pana la 20% sa spunem frunza din Dashboard
este verde o parte din interfata este verde simbolizand o poluare redusa datorita emisiilor mai reduse de dioxid de carbon; daca apasarea "pedalei" creste (20-60%) frunza seapleaca in jos se "pleosteste" aratamd conducatorului ca exista emisii de dioxid
de carbon mai consistente; daca acceleratia depaseste 60% utilizatorul vede un semnul exclamarii avertizandu-l ca numai conduce ecologic

**Versiunea de consolă:**

```bash
python mainHibrid.py
```

Se navighează prin meniul numerotat afișat în terminal.

## Posibile extinderi pentru viitor

- salvarea istoricului de drumuri într-un fișier (CSV/JSON)
- alimentare cu combustibil / încărcare baterie direct din interfața grafică
- mod de condus autonom, cu accelerație generată automat pe baza tipului de drum
