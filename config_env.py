import tkinter as tk
from tkinter import messagebox
import json
import os

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x, y, _, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + cy + self.widget.winfo_rooty() + 25
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify="left",
                         background="#ffffe0", relief="solid", borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

class EnvGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de .env")

        # Campos principais
        tk.Label(root, text="API_KEY:").grid(row=0, column=0, sticky="w")
        self.api_key_entry = tk.Entry(root, width=40)
        self.api_key_entry.grid(row=0, column=1)

        tk.Label(root, text="DISCORD_TOKEN:").grid(row=1, column=0, sticky="w")
        self.discord_token_entry = tk.Entry(root, width=40)
        self.discord_token_entry.grid(row=1, column=1)

        tk.Label(root, text="DISCORD_CHANNEL_ID:").grid(row=2, column=0, sticky="w")
        self.discord_channel_entry = tk.Entry(root, width=40)
        self.discord_channel_entry.grid(row=2, column=1)

        tk.Label(root, text="GAMES_FILE (.json):").grid(row=3, column=0, sticky="w")
        self.games_file_entry = tk.Entry(root, width=40)
        self.games_file_entry.insert(0, "jogos_anteriores.json")
        self.games_file_entry.grid(row=3, column=1)

        lang_label = tk.Label(root, text="LANGUAGE:")
        lang_label.grid(row=4, column=0, sticky="w")
        self.language_entry = tk.Entry(root, width=40)
        self.language_entry.insert(0, "brazilian")
        self.language_entry.grid(row=4, column=1)
        ToolTip(lang_label, "Veja a lista completa de linguagens aqui:\nhttps://partner.steamgames.com/doc/store/localization/languages")

        # Membros da família
        family_label = tk.Label(root, text="Pessoas da família (nome e ID):")
        family_label.grid(row=5, column=0, columnspan=2, pady=(10, 0))
        ToolTip(family_label, "O ID deve ser numérico e pode ser obtido em:\nhttps://steamid.io/")

        self.members_frame = tk.Frame(root)
        self.members_frame.grid(row=6, column=0, columnspan=2)

        # Títulos para colunas
        tk.Label(self.members_frame, text="Membro", font=("Arial", 9, "bold")).grid(row=0, column=0, padx=5, pady=(0,5))
        tk.Label(self.members_frame, text="ID Steam", font=("Arial", 9, "bold")).grid(row=0, column=1, padx=5, pady=(0,5))

        self.members_entries = []
        for i in range(6):
            name_entry = tk.Entry(self.members_frame, width=20)
            name_entry.grid(row=i+1, column=0, padx=5, pady=2)
            id_entry = tk.Entry(self.members_frame, width=25)
            id_entry.grid(row=i+1, column=1, padx=5, pady=2)
            self.members_entries.append((name_entry, id_entry))

        # Botão de gerar
        tk.Button(root, text="Gerar .env", command=self.generate_env).grid(row=7, column=0, columnspan=2, pady=10)

    def generate_env(self):
        api_key = self.api_key_entry.get().strip()
        discord_token = self.discord_token_entry.get().strip()
        channel_id = self.discord_channel_entry.get().strip()
        games_file = self.games_file_entry.get().strip()
        language = self.language_entry.get().strip()

        if not games_file.endswith(".json"):
            messagebox.showerror("Erro", "O campo GAMES_FILE precisa terminar em .json")
            return

        steam_ids = {}
        for name_entry, id_entry in self.members_entries:
            name = name_entry.get().strip()
            steam_id = id_entry.get().strip()
            if name and steam_id:
                steam_ids[name] = steam_id

        env_content = (
            f"API_KEY=\"{api_key}\"\n"
            f"DISCORD_TOKEN=\"{discord_token}\"\n"
            f"DISCORD_CHANNEL_ID={channel_id}\n"
            f"STEAM_IDS='{json.dumps(steam_ids, ensure_ascii=False)}'\n"
            f"GAMES_FILE=\"{games_file}\"\n"
            f"LANGUAGE=\"{language}\"\n"
        )

        file_path = os.path.join(os.getcwd(), ".env")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(env_content)

        messagebox.showinfo("Sucesso", f"Arquivo .env gerado automaticamente na pasta do projeto:\n{file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EnvGeneratorApp(root)
    root.mainloop()
