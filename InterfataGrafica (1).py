import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from baterie import Baterie
from rezervor import Rezervor

ctk.set_appearance_mode("dark")  # setez fereastra de dialog pe un fundal inchis pentru o mai buna lizibilitate din partea soferului in zilele cu soare puternic

app = ctk.CTk()
app.geometry("700x800") # fac o fereastra de dialog mare pentru o buna lizibilitate la volan
app.title("Eco Driving Dashboard")

# ---------------- DATE ----------------

baterie = Baterie(100, 100)
rezervor = Rezervor(40, 40)

distanta_totala = 0
drum_factor = 1

km_electrici = 0
km_termici = 0
eco_score = 100

lista_km = []
lista_combustibil = []

# ---------------- TITLU ----------------

titlu = ctk.CTkLabel(
    app,
    text="Eco Driving Dashboard",
    font=("Arial", 24, "bold")
)
titlu.pack(pady=10)

# ---------------- STATUS ----------------

baterie_label = ctk.CTkLabel(
    app,
    text="🔋 Baterie: 100%"
)
baterie_label.pack()

combustibil_label = ctk.CTkLabel(
    app,
    text="⛽ Combustibil: 40 L"
)
combustibil_label.pack()

mod_label = ctk.CTkLabel(
    app,
    text="🚗 Mod: Electric"
)
mod_label.pack()

distanta_label = ctk.CTkLabel(
    app,
    text="📍 Distanță: 0 km"
)
distanta_label.pack()

km_electrici_label = ctk.CTkLabel(
    app,
    text="⚡ Km electrici: 0"
)
km_electrici_label.pack()

km_termici_label = ctk.CTkLabel(
    app,
    text="🔥 Km termici: 0"
)
km_termici_label.pack()

eco_label = ctk.CTkLabel(
    app,
    text="🏆 Eco Score: 100"
)
eco_label.pack()

info_drum = ctk.CTkLabel(
    app,
    text="🚦 Selectează un drum"
)
info_drum.pack(pady=10)

# ---------------- DRUM ----------------

def actualizeaza_drum(alegere):     # Funcția actualizeaza_drum se execută automat de fiecare dată când utilizatorul alege o opțiune nouă din combobox-ul tip_drum
    global drum_factor

    if alegere == "Oraș":    # am definit oras in ideea ca este diferit de drum national, sunt semafoare; porniri; opriri la treceri de pietoni
        drum_factor = 1.2
        info_drum.configure(
            text="🚦 Trafic urban"
        )

    elif alegere == "Oraș aglomerat":    # oras aglomerat multe opriri multe accelerari de la 0 la poate 30kmh
        drum_factor = 1.5
        info_drum.configure(
            text="🚗🚗🚗 Trafic aglomerat"
        )

    elif alegere == "Drum național":   # drum national cu opriri foarte putine mers la o viteza relativ constanta 
        drum_factor = 1
        info_drum.configure(
            text="🛣️ Drum național"
        )

    elif alegere == "Autostradă":    # drum cu deplasare foarte rapida; 
        drum_factor = 0.8
        info_drum.configure(
            text="🏎️ Autostradă"
        )

tip_drum = ctk.CTkComboBox(        # am conceput ca butoane intr-o lista derulanta tipurile de drum (oras, oras aglomerat, drum national, autostrada)
    app,
    values=[
        "Oraș",
        "Oraș aglomerat",
        "Drum național",
        "Autostradă"
    ],
    command=actualizeaza_drum
)

tip_drum.pack(pady=5)
tip_drum.set("Oraș")

# ---------------- ECO UI ----------------  ### construiesc interfata "Eco" pentru acceleratie simbolul 🌿 - o frunza verde si linia acceleratiei colorata in verde
# sugereaza soferului sa accelereze domol nu brusc, pentru a reduce emisiile de dioxid de carbon si consumul de benzina.

simbol = ctk.CTkLabel(
    app,
    text="🌿",
    font=("Arial", 60)
)
simbol.pack()

progress = ctk.CTkProgressBar(
    app,
    width=350
)
progress.pack()

progress.set(0)

valoare = ctk.CTkLabel(
    app,
    text="Accelerație: 0%"
)
valoare.pack()

def actualizeaza_slider(v):   # 

    v = float(v)

    progress.set(v / 100)

    valoare.configure(
        text=f"Accelerație: {int(v)}%"
    )

    if v <= 20:
        simbol.configure(text="🌿")
        progress.configure(progress_color="green")
#  Daca acceleratia este mai viguroasa frunza o sa apara pleostita, aplecata in jos parca s-ar usca. Daca acceleratia este brutala peste 60% din potential
#  apare un semnul exclamarii atentionand soferul sa accelereze # mai domol si ca numai conduce eco-friendly
    elif v <= 60:
        simbol.configure(text="🍂")
        progress.configure(progress_color="yellow")

    else:
        simbol.configure(text="⚠️")
        progress.configure(progress_color="red")

slider = ctk.CTkSlider(
    app,
    from_=0,
    to=100,
    command=actualizeaza_slider
)

slider.pack(pady=15)

# ---------------- GRAFIC ----------------

fig, ax = plt.subplots(figsize=(5, 3))  # creează o figură matplotlib goală, de dimensiune 5x3 inch, plus un set de axe (ax) pe care ulterior va apare un grafic cu consumul si eficiența, în funcție de tipul de drum și accelerație
canvas = FigureCanvasTkAgg(
    fig,
    master=app
)
canvas.get_tk_widget().pack(pady=10) # transformă figura într-un widget normal de tkinter, pe care apoi îl afișezi cu .pack(pady=10), exact ca pe orice alt element din interfață.

def update_grafic():  # Funcția redesenează graficul de fiecare dată când e apelată (probabil după ce se adaugă un nou punct de date, pe măsură ce mașina "parcurge" kilometri în simulare).

    ax.clear() # șterge tot ce era desenat anterior pe axe, ca să nu se suprapună graficele vechi peste cele noi de fiecare dată când utilizatorul actualizeaza

    ax.plot(
        lista_km, # lista distante parcurse
        lista_combustibil, # cantitatea de combustibil ramasa dupa fiecare distanta 
        marker="o"
    )

    ax.set_title("Combustibil rămas")
    ax.set_xlabel("Km")
    ax.set_ylabel("Litri")

    ax.grid(True)

    canvas.draw()  
    canvas.draw() # forțează widget-ul tkinter să se redeseneze cu graficul actualizat 

# ---------------- CALCULE ----------------

def consum_la_suta(acceleratie):    # Funcția calculează consumul de combustibil la 100 km, combinând doi factori: intensitatea accelerației (parametrul acceleratie, de la slider, 0-100%) și tipul de drum (variabila globală drum_factor)
    """Returnează consumul în L/100km, în funcție de accelerație și tipul de drum."""

    baza = 8  # L / 100km la accelerație 0

    return baza * (1 + acceleratie / 100) * drum_factor

# ---------------- UI ----------------

def update_ui(acceleratie):   # Funcția actualizează toate elementele de UI cu informațiile curente ale simulării, de fiecare dată când se schimbă accelerația. Practic e funcția centrală care "redesenează" tot tabloul de bord.

    global eco_score

    baterie_label.configure(   # avem 3 blocuri care actualizeaza textul label-urilor citind valorile din obiectele baterie si rezervor
        text=f"🔋 Baterie: {baterie.nivel_curent:.0f}%"
    )

    combustibil_label.configure(
        text=f"⛽ Combustibil: {rezervor.combustibil_curent:.1f} L"
    )

    distanta_label.configure(
        text=f"📍 Distanță: {distanta_totala} km"
    )

    if baterie.nivel_curent <= 0:  # logica pentru modul de conducere bateria e goala forteaza pornirea motorului termic
        mod = "🚗 Mod: Termic"

    elif acceleratie < 30:   # daca viteza sub 30kmh auto circula in modul electric pentru a economisi combustibil
        mod = "🚗 Mod: Electric"

    elif acceleratie < 70: # daca viteza este peste 30kmh dar sub 70kmh sistemul alege deplasarea in ciclu mixt cu ambele motoare
        mod = "🚗 Mod: Hibrid"

    else:
        mod = "🚗 Mod: Termic" # pentru o deplasare peste 70kmh este suficient motorul pe benzona

    mod_label.configure(text=mod)

    eco_score = max(  # se calculează scăzând din 100 jumătate din valoarea accelerației (deci la 0% accelerație ai scor 100, la 100% accelerație ai scor 50 
        0,
        100 - int(acceleratie / 2)
    )

    eco_label.configure(
        text=f"🏆 Eco Score: {eco_score}"
    )

    km_electrici_label.configure(
        text=f"⚡ Km electrici: {km_electrici}"
    )

    km_termici_label.configure(
        text=f"🔥 Km termici: {km_termici}"
    )

# ---------------- SIMULARE ----------------

def simuleaza_drum():

    global distanta_totala
    global km_electrici
    global km_termici

    if rezervor.combustibil_curent <= 0:
        info_drum.configure(
            text="⛔ Rezervor gol!"
        )
        return

    acceleratie = slider.get()

    km = max(
        1,
        int((acceleratie / 10) * drum_factor)
    )

    distanta_totala += km

    consum_suta = consum_la_suta(acceleratie)
    rezervor.consuma_functie_distanta(km, consum_suta)

    if acceleratie < 30 and baterie.nivel_curent > 0:

        km_electrici += km
        baterie.consuma(km * 0.5)

    elif acceleratie < 70 and baterie.nivel_curent > 0:

        km_electrici += km // 2
        km_termici += km // 2
        baterie.consuma(km * 0.3)

    else:

        km_termici += km

    lista_km.append(
        distanta_totala
    )

    lista_combustibil.append(
        rezervor.combustibil_curent
    )

    update_ui(acceleratie)
    update_grafic()

# ---------------- START ----------------

def start_drum():

    global baterie
    global rezervor
    global distanta_totala
    global km_electrici
    global km_termici
    global eco_score
    global lista_km
    global lista_combustibil

    baterie = Baterie(100, 100)
    rezervor = Rezervor(40, 40)

    distanta_totala = 0

    km_electrici = 0
    km_termici = 0

    eco_score = 100

    lista_km = []
    lista_combustibil = []

    slider.set(0)
    actualizeaza_slider(0)

    update_ui(0)
    update_grafic()

    info_drum.configure(
        text="🔑 Motor pornit — la drum!"
    )

# ---------------- BUTOANE ----------------

start_btn = ctk.CTkButton(
    app,
    text="🔑 Pornește Mașina",
    command=start_drum
)

start_btn.pack(pady=5)

sim_btn = ctk.CTkButton(
    app,
    text="⏩ Continuă Drumul",
    command=simuleaza_drum
)

sim_btn.pack(pady=10)

app.mainloop()
