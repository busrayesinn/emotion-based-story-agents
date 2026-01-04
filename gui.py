import customtkinter as ctk
import webbrowser
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

# ================= GLOBAL UI REFERENCES =================
lbl_track = None
lbl_artist = None
btn_spotify = None
txt_activity = None
lbl_emotion = None
debug_box = None

input_event = None
input_mood = None
meal_var = None
city_var = None

# ================= AGENT IMPORT =================
try:
    from agents.coordinator_agent import CoordinatorAgent
    coordinator = CoordinatorAgent()
    COORDINATOR_AVAILABLE = True
except Exception as e:
    COORDINATOR_AVAILABLE = False
    print("Agent import hatası:", e)
    COORDINATOR_AVAILABLE = False
    coordinator = None

# ================= THEME SETTINGS =================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

COLORS = {
    "bg": "#0f172a",           # Koyu Lacivert Arka Plan
    "card_bg": "#1e293b",      # Kart Arka Planı
    "accent": "#3b82f6",       # Mavi Vurgu
    "text_main": "#f8fafc",    # Beyaz Metin
    "text_sub": "#94a3b8",     # Gri Metin
    "music_bg": "#064e3b",     # Koyu Yeşil (Spotify)
    "music_fg": "#34d399",     # Açık Yeşil
    "act_bg": "#312e81",       # Koyu Mor/İndigo
    "act_fg": "#a5b4fc",       # Açık Mor
    "chart_line": "#38bdf8",   # Grafik Çizgisi
}

# ================= GRAPH FUNCTION =================
def update_chart(values):
    """Matplotlib grafiğini günceller."""
    ax.clear()
    categories = ["Valence", "Arousal", "Comfort", "Calm", "Intensity"]

    # Çizgi ve Alan
    ax.plot(categories, values, color=COLORS["chart_line"], marker="o", linewidth=2, markersize=6)
    ax.fill_between(categories, values, color=COLORS["chart_line"], alpha=0.15)

    # Eksen Ayarları
    ax.set_ylim(-1.1, 1.1)
    ax.axhline(0, color=COLORS["text_sub"], linestyle="--", linewidth=0.8)
    ax.set_ylabel("Denge Sapması (50 = 0)", color=COLORS["text_sub"], fontsize=8)

    # Renkler ve Stil
    fig.patch.set_facecolor(COLORS["card_bg"])
    ax.set_facecolor(COLORS["card_bg"])
    
    # Kenarlıkları Kaldır/Ayarla
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_color(COLORS["text_sub"])
    ax.spines["left"].set_color(COLORS["text_sub"])
    
    ax.tick_params(axis="x", colors=COLORS["text_sub"], labelsize=9)
    ax.tick_params(axis="y", colors=COLORS["text_sub"], labelsize=8)

    canvas.draw()

# ================= PIPELINE (LOGIC) =================
def run_pipeline():
    global lbl_track, lbl_artist, btn_spotify, txt_activity, lbl_emotion, debug_box
    
    # 1. Girdileri Al
    user_text = input_mood.get("1.0", "end").strip()
    event_text = input_event.get("1.0", "end").strip()
    city = city_var.get() or "Bursa"
    micro_input = meal_var.get()

    if not user_text:
        return 

    # Debug kutusunu temizle ve aç
    debug_box.configure(state="normal")
    debug_box.delete("1.0", "end")

    if COORDINATOR_AVAILABLE:
        try:
            # --- AGENT İŞLEMİ ---
            res = coordinator.process(
                user_text=user_text,
                city=city,
                event_text=event_text if event_text else None,
                micro_input=micro_input,
            )

            # A. Duygu Durumu
            lbl_emotion.configure(text=res.final_emotion.upper())

            # B. Grafik Güncelleme
            s = res.affect_state
            chart_values = [
                (s.valence - 50) / 50,
                (s.arousal - 50) / 50,
                (s.physical_comfort - 50) / 50,
                (s.environmental_calm - 50) / 50,
                (s.emotional_intensity - 50) / 50,
            ]
            update_chart(chart_values)

            # C. Debug / Log Yazdırma
            debug_box.insert("end", "🧠 AFFECT STATE (Ham Veri)\n", "header")
            debug_box.insert("end", f"Val: {s.valence} | Aro: {s.arousal} | Comf: {s.physical_comfort}\n")
            debug_box.insert("end", f"Calm: {s.environmental_calm} | Int: {s.emotional_intensity}\n\n")

            debug_box.insert("end", "🎯 REGÜLASYON HEDEFİ\n", "header")
            for g in res.regulation.guidance:
                debug_box.insert("end", f"• {g}\n")

            debug_box.insert("end", "\n🪵 KARAR İZLERİ\n", "header")
            for d in res.debug:
                debug_box.insert("end", f"- {d}\n")

            # D. Müzik Önerisi
            music = res.music or {}
            lbl_track.configure(text=music.get("track", "Öneri Yok"))
            lbl_artist.configure(text=music.get("artist", "-"))
            
            spotify_link = music.get("spotify_url")
            if spotify_link:
                btn_spotify.configure(state="normal", command=lambda: webbrowser.open(spotify_link))
            else:
                btn_spotify.configure(state="disabled")

            # E. Aktivite Önerisi
            txt_activity.configure(state="normal")
            txt_activity.delete("1.0", "end")
            txt_activity.insert("end", res.micro_activity)
            txt_activity.configure(state="disabled")


        except Exception as e:
            debug_box.insert("end", f"\n❌ HATA: {e}\n", "header")
            print(e)
    else:
        # --- MOCK (TEST) MODU ---
        lbl_emotion.configure(text="TEST: MUTLU")
        update_chart([random.uniform(-0.8, 0.8) for _ in range(5)])
        
        lbl_track.configure(text="Test Şarkısı")
        lbl_artist.configure(text="Test Sanatçısı")
        
        txt_activity.configure(state="normal")
        txt_activity.delete("1.0", "end")
        txt_activity.insert("end", "Agent bağlı değil. Demo çıktısıdır.")
        txt_activity.configure(state="disabled")
        
        debug_box.insert("end", "⚠️ Agent bulunamadı, mock veriler.", "header")

    debug_box.configure(state="disabled")

# ================= APP UI LAYOUT =================
app = ctk.CTk()
app.title("Duygu Regülasyonu Asistanı")
app.geometry("1200x850")
app.configure(fg_color=COLORS["bg"])

# --- GRID AYARLARI (55x - 45x) ---
app.grid_columnconfigure(0, weight=55) # SOL TARAF DAHA GENİŞ
app.grid_columnconfigure(1, weight=45) # SAĞ TARAF
app.grid_rowconfigure(2, weight=1)

# ---------- 1. HEADER ----------
header = ctk.CTkFrame(app, fg_color="transparent")
header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(15, 5))

ctk.CTkLabel(header, text="🎧 Duygu Regülasyonu Asistanı", font=("Roboto", 26, "bold"), text_color=COLORS["text_main"]).pack(anchor="center")
ctk.CTkLabel(header, text="Beş boyutlu duygu analizi & yapay zeka destekli regülasyon", font=("Roboto", 14), text_color=COLORS["text_sub"]).pack(anchor="center")

# ---------- 2. SOL PANEL (GİRDİLER + ÖNERİLER) ----------
left_panel = ctk.CTkFrame(app, fg_color="transparent")
left_panel.grid(row=1, column=0, rowspan=2, sticky="nsew", padx=20, pady=10)

def create_card(parent):
    frame = ctk.CTkFrame(parent, fg_color=COLORS["card_bg"], corner_radius=16)
    frame.pack(fill="x", pady=8)
    return frame

# --- KART 1: Mood & Şehir ---
card1 = create_card(left_panel)
c1_header = ctk.CTkFrame(card1, fg_color="transparent")
c1_header.pack(fill="x", padx=15, pady=(12, 5))

ctk.CTkLabel(c1_header, text="🧠 Nasıl Hissediyorsun?", font=("Roboto", 15, "bold"), text_color=COLORS["text_main"]).pack(side="left")
city_var = ctk.StringVar(value="Bursa")
ctk.CTkOptionMenu(c1_header, variable=city_var, values=["Bursa", "İstanbul", "Ankara", "İzmir"], width=100, fg_color=COLORS["accent"], button_color=COLORS["accent"]).pack(side="right")
input_mood = ctk.CTkTextbox(card1, height=100, fg_color=COLORS["bg"], text_color="white", border_width=0)
input_mood.pack(fill="x", padx=15, pady=(0, 15))

# --- KART 2: Olay & Yemek ---
card2 = create_card(left_panel)
ctk.CTkLabel(card2, text="📩 Günlük Bağlam", font=("Roboto", 15, "bold"), text_color=COLORS["text_main"]).pack(anchor="w", padx=15, pady=(12, 5))
c2_grid = ctk.CTkFrame(card2, fg_color="transparent")
c2_grid.pack(fill="x", padx=15, pady=(0, 15))
c2_grid.grid_columnconfigure(0, weight=3)
c2_grid.grid_columnconfigure(1, weight=1)

input_event = ctk.CTkTextbox(c2_grid, height=80, fg_color=COLORS["bg"], text_color="white")
input_event.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
ctk.CTkLabel(c2_grid, text="Olay / Mesaj (Opsiyonel)", font=("Roboto", 10), text_color=COLORS["text_sub"]).grid(row=1, column=0, sticky="w")

meal_frame = ctk.CTkFrame(c2_grid, fg_color="transparent")
meal_frame.grid(row=0, column=1, sticky="ns")
ctk.CTkLabel(meal_frame, text="Yemek?", font=("Roboto", 12, "bold"), text_color=COLORS["text_sub"]).pack(anchor="w")
meal_var = ctk.IntVar(value=0)
ctk.CTkRadioButton(meal_frame, text="Açım/Kötü", variable=meal_var, value=-1, font=("Roboto", 11)).pack(anchor="w", pady=5)
ctk.CTkRadioButton(meal_frame, text="Tokum/İyi", variable=meal_var, value=1, font=("Roboto", 11)).pack(anchor="w")

# --- AKSİYON BUTONU ---
ctk.CTkButton(left_panel, text="✨ Analiz Et ve Regüle Et", height=50, font=("Roboto", 16, "bold"), fg_color=COLORS["accent"], hover_color="#2563eb", corner_radius=12, command=run_pipeline).pack(fill="x", pady=10)

# --- YENİ YER: MÜZİK VE AKTİVİTE (SOL PANELDE BUTONUN ALTI) ---
output_grid = ctk.CTkFrame(left_panel, fg_color="transparent")
output_grid.pack(fill="x", pady=(10, 0))
output_grid.grid_columnconfigure(0, weight=1)
output_grid.grid_columnconfigure(1, weight=1)

# Müzik Kutusu
music_box = ctk.CTkFrame(output_grid, fg_color=COLORS["music_bg"], corner_radius=16)
music_box.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

ctk.CTkLabel(music_box, text="🎧 Müzik Önerisi", font=("Roboto", 14, "bold"), text_color=COLORS["music_fg"]).pack(anchor="w", padx=15, pady=(15, 5))
lbl_track = ctk.CTkLabel(music_box, text="-", font=("Roboto", 16, "bold"), text_color="white", wraplength=200)
lbl_track.pack(anchor="w", padx=15)
lbl_artist = ctk.CTkLabel(music_box, text="-", font=("Roboto", 12), text_color="#a7f3d0")
lbl_artist.pack(anchor="w", padx=15)
btn_spotify = ctk.CTkButton(music_box, text="Spotify'da Aç", fg_color="#1db954", hover_color="#15803d", text_color="white", height=32, state="disabled")
btn_spotify.pack(anchor="w", padx=15, pady=(10, 15))

# Aktivite Kutusu
act_box = ctk.CTkFrame(output_grid, fg_color=COLORS["act_bg"], corner_radius=16)
act_box.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

ctk.CTkLabel(act_box, text="🧩 Mikro Aktivite", font=("Roboto", 14, "bold"), text_color=COLORS["act_fg"]).pack(anchor="w", padx=15, pady=(15, 5))
txt_activity = ctk.CTkTextbox(act_box, height=80, fg_color="transparent", text_color="white", wrap="word", font=("Roboto", 13))
txt_activity.pack(fill="both", expand=True, padx=10, pady=(0, 10))
txt_activity.insert("end", "Öneri bekleniyor...")
txt_activity.configure(state="disabled")


# ---------- 3. SAĞ PANEL (GRAFİK + LOG) ----------
right_panel = ctk.CTkFrame(app, fg_color="transparent")
right_panel.grid(row=1, column=1, rowspan=2, sticky="nsew", padx=(0, 20), pady=10)

# --- ÜST: Özet ve Grafik ---
summary_card = ctk.CTkFrame(right_panel, fg_color=COLORS["card_bg"], corner_radius=16)
summary_card.pack(fill="x", pady=(0, 10))

lbl_emotion = ctk.CTkLabel(summary_card, text="ANALİZ BEKLENİYOR", font=("Roboto", 24, "bold"), text_color=COLORS["accent"])
lbl_emotion.pack(pady=(15, 5))

fig, ax = plt.subplots(figsize=(6, 3), dpi=100) # Grafiği biraz daha uzun yapabiliriz artık
canvas = FigureCanvasTkAgg(fig, master=summary_card)
canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
update_chart([0, 0, 0, 0, 0])

# --- ALT: Debug Konsolu ---
debug_frame = ctk.CTkFrame(right_panel, fg_color="#020617", corner_radius=12)
debug_frame.pack(fill="both", expand=True)

ctk.CTkLabel(debug_frame, text="🛠️ Karar İzleri & Sistem Logları", font=("Consolas", 12, "bold"), text_color="#64748b").pack(anchor="w", padx=10, pady=(8, 5))

debug_box = ctk.CTkTextbox(debug_frame, font=("Consolas", 12), fg_color="transparent", text_color="#cbd5e1", wrap="word")
debug_box.pack(fill="both", expand=True, padx=5, pady=(0, 5))
debug_box._textbox.tag_config("header", foreground=COLORS["accent"], font=("Consolas", 12, "bold")) # FIX UYGULANDI
debug_box.insert("end", "Sistem hazır. Veri girişi bekleniyor...\n")
debug_box.configure(state="disabled")

if __name__ == "__main__":
    app.mainloop()