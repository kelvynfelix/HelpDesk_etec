import tkinter as tk
from tkinter import messagebox
from DataBase_library import create_ticket

def _rounded_rect(canvas, x1, y1, x2, y2, r=20, **kwargs):
    points = [
        x1 + r, y1, x2 - r, y1, x2, y1,
        x2, y1 + r, x2, y2 - r, x2, y2,
        x2 - r, y2, x1 + r, y2, x1, y2,
        x1, y2 - r, x1, y1 + r, x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


class CanvasButton:
    def __init__(self, canvas, x, y, w, h, text, command,
                 bg="#4B7BEC", hover="#3A69E6", active="#2E53C9",
                 fg="white", radius=14, shadow=True, font=None):
        self.canvas = canvas
        self.command = command
        self.bg = bg
        self.hover = hover
        self.active = active
        self.fg = fg
        self.font = font or ("Segoe UI", 11, "bold")

        left, top, right, bottom = x - w/2, y - h/2, x + w/2, y + h/2

        self.shadow_id = None
        if shadow:
            self.shadow_id = _rounded_rect(canvas, left+3, top+4, right+3, bottom+4,
                                           r=radius, fill="#000000", stipple="gray25", outline="")

        self.rect_id = _rounded_rect(canvas, left, top, right, bottom, r=radius, fill=self.bg, outline="")
        self.text_id = canvas.create_text(x, y, text=text, fill=self.fg, font=self.font)

        for _id in (self.rect_id, self.text_id):
            canvas.tag_bind(_id, "<Enter>", self._on_enter)
            canvas.tag_bind(_id, "<Leave>", self._on_leave)
            canvas.tag_bind(_id, "<Button-1>", self._on_press)
            canvas.tag_bind(_id, "<ButtonRelease-1>", self._on_release)

    def _on_enter(self, _=None):
        self.canvas.itemconfigure(self.rect_id, fill=self.hover)

    def _on_leave(self, _=None):
        self.canvas.itemconfigure(self.rect_id, fill=self.bg)

    def _on_press(self, _=None):
        self.canvas.itemconfigure(self.rect_id, fill=self.active)

    def _on_release(self, _=None):
        self.canvas.itemconfigure(self.rect_id, fill=self.hover)
        if callable(self.command):
            self.command()


class TelaUsuario:
    CARD_W = 520
    CARD_H = 420

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tela Usuário")
        self.root.configure(bg="#0f1724")

        self._fullscreen_applied = False
        self._apply_fullscreen()

        self.canvas = tk.Canvas(self.root, highlightthickness=0, bg="#0f1724")
        self.canvas.pack(fill="both", expand=True)

        self._build_fields()
        self.root.bind("<Configure>", self._on_resize)
        self.root.bind("<F11>", self._toggle_fullscreen)
        self.root.bind("<Escape>", self._exit_fullscreen)
        self.root.bind("<Return>", lambda e: self._enviar())

        self.button = None
        self._resize_job = None
        self.root.after(60, self._draw)
        self.root.mainloop()

    def _apply_fullscreen(self):
        # Tenta maximizar no Windows / Linux
        try:
            self.root.state("zoomed")
            self._fullscreen_applied = True
        except Exception:
            pass
        # Força fullscreen se não funcionou
        if not self._fullscreen_applied:
            self.root.attributes("-fullscreen", True)
        self.root.update_idletasks()

    def _toggle_fullscreen(self, _=None):
        fs = bool(self.root.attributes("-fullscreen"))
        self.root.attributes("-fullscreen", not fs)

    def _exit_fullscreen(self, _=None):
        if self.root.attributes("-fullscreen"):
            self.root.attributes("-fullscreen", False)

    def _build_fields(self):
        entry_style = dict(bg="#152234", fg="#E6F0FF", insertbackground="#ffffff",
                           relief="flat", font=("Segoe UI", 11))
        self.sala_entry = tk.Entry(self.canvas, **entry_style)
        self.nome_entry = tk.Entry(self.canvas, **entry_style)
        self.desc_text = tk.Text(self.canvas, height=6, wrap="word", **entry_style)

    def _draw_gradient(self, w, h):
        self.canvas.delete("grad")
        top = (15, 23, 36)
        bottom = (28, 45, 74)
        steps = max(1, h // 4)
        # Efficient: single rectangles
        for i in range(steps):
            r = top[0] + (bottom[0] - top[0]) * i // steps
            g = top[1] + (bottom[1] - top[1]) * i // steps
            b = top[2] + (bottom[2] - top[2]) * i // steps
            color = f"#{r:02x}{g:02x}{b:02x}"
            y1 = i * h // steps
            y2 = (i + 1) * h // steps
            self.canvas.create_rectangle(0, y1, w, y2, outline="", fill=color, tags="grad")

    def _draw_card(self, w, h):
        self.canvas.delete("card")
        cx, cy = w / 2, h / 2
        x1 = cx - self.CARD_W / 2
        y1 = cy - self.CARD_H / 2
        x2 = cx + self.CARD_W / 2
        y2 = cy + self.CARD_H / 2
        _rounded_rect(self.canvas, x1, y1, x2, y2, r=26, fill="#0b1220", outline="", tags="card")

        self.canvas.create_text(cx, y1 + 42, text="Novo Chamado", fill="#E6F0FF",
                                font=("Segoe UI", 22, "bold"), tags="card")
        self.canvas.create_text(cx, y1 + 74, text="Preencha os campos e envie",
                                fill="#AFC7FF", font=("Segoe UI", 11), tags="card")

        form_left = x1 + 34
        form_width = self.CARD_W - 68
        entry_w_pixels = int(form_width)

        def place_entry(widget, wx, wy, h_inner=30):
            # Ajusta largura real
            if isinstance(widget, tk.Entry):
                widget.configure(width=max(10, entry_w_pixels // 8))
            elif isinstance(widget, tk.Text):
                widget.configure(width=max(10, entry_w_pixels // 8))
            self.canvas.create_window(wx, wy, anchor="nw", window=widget, height=h_inner, width=entry_w_pixels, tags="card")

        y = y1 + 110
        self._label("Sala:", form_left, y)
        place_entry(self.sala_entry, form_left, y + 18)

        y += 70
        self._label("Nome:", form_left, y)
        place_entry(self.nome_entry, form_left, y + 18)

        y += 70
        self._label("Descrição:", form_left, y)
        place_entry(self.desc_text, form_left, y + 20, h_inner=110)

        # Botão
        if self.button:
            for i in (self.button.rect_id, self.button.text_id, getattr(self.button, "shadow_id", None)):
                if i:
                    self.canvas.delete(i)

        self.button = CanvasButton(
            self.canvas, cx, y2 - 50, 230, 52, "Enviar",
            command=self._enviar,
            bg="#4B7BEC", hover="#3A69E6", active="#2E53C9",
            fg="white", radius=16, font=("Segoe UI", 13, "bold")
        )

        # Foco inicial
        if not self.sala_entry.focus_get():
            self.sala_entry.focus_set()

    def _label(self, text, x, y):
        self.canvas.create_text(x, y, text=text, fill="#AFC7FF",
                                font=("Segoe UI", 11), anchor="w", tags="card")

    def _on_resize(self, _):
        if self._resize_job:
            try:
                self.root.after_cancel(self._resize_job)
            except Exception:
                pass
        self._resize_job = self.root.after(50, self._draw)

    def _draw(self):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w <= 2 or h <= 2:
            self.root.after(40, self._draw)
            return
        self._draw_gradient(w, h)
        self._draw_card(w, h)

    def _enviar(self):
        sala = self.sala_entry.get().strip()
        nome = self.nome_entry.get().strip()
        descricao = self.desc_text.get("1.0", "end").strip()
        if not sala or not nome or not descricao:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return
        try:
            create_ticket(sala, nome, descricao)
            messagebox.showinfo("Sucesso", "Chamado enviado.")
            self.sala_entry.delete(0, "end")
            self.nome_entry.delete(0, "end")
            self.desc_text.delete("1.0", "end")
            self.sala_entry.focus_set()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao criar ticket:\n{e}")


def build_ui():
    TelaUsuario()


if __name__ == "__main__":
    build_ui()


