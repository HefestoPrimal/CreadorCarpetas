import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import csv
import json
from pathlib import Path


# ── Paleta de colores ──────────────────────────────────────────────────────────
BG        = "#0F0F13"
SURFACE   = "#1A1A24"
SURFACE2  = "#22222F"
BORDER    = "#2E2E42"
ACCENT    = "#7C6AF7"
ACCENT2   = "#A78BFA"
SUCCESS   = "#34D399"
ERROR     = "#F87171"
TEXT      = "#E8E8F0"
TEXT_DIM  = "#6B6B8A"
WHITE     = "#FFFFFF"

FONT_MONO = ("Consolas", 10)
FONT_UI   = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI Semibold", 10)
FONT_H1   = ("Segoe UI Semibold", 15)
FONT_H2   = ("Segoe UI Semibold", 11)
FONT_SM   = ("Segoe UI", 9)


class FolderCreatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Folder Creator")
        self.geometry("780x680")
        self.minsize(680, 580)
        self.configure(bg=BG)
        self.resizable(True, True)

        # Intentar icono sin que falle
        try:
            self.iconbitmap(default="")
        except Exception:
            pass

        # Estado
        self.dest_path = tk.StringVar(value=str(Path.home()))
        self.folder_entries: list[tk.StringVar] = []
        self.status_var = tk.StringVar(value="Listo.")

        self._build_ui()
        self._add_row()   # fila inicial vacía

    # ── Construcción de la interfaz ────────────────────────────────────────────

    def _build_ui(self):
        # Header
        header = tk.Frame(self, bg=ACCENT, height=4)
        header.pack(fill="x", side="top")

        title_frame = tk.Frame(self, bg=BG, pady=20, padx=30)
        title_frame.pack(fill="x")

        tk.Label(title_frame, text="📁", font=("Segoe UI", 22),
                 bg=BG, fg=ACCENT2).pack(side="left", padx=(0, 12))

        info = tk.Frame(title_frame, bg=BG)
        info.pack(side="left")
        tk.Label(info, text="Folder Creator", font=FONT_H1,
                 bg=BG, fg=WHITE).pack(anchor="w")
        tk.Label(info, text="Crea múltiples carpetas de forma rápida y automatizada",
                 font=FONT_SM, bg=BG, fg=TEXT_DIM).pack(anchor="w")

        # Separador
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=30)

        # Cuerpo principal
        body = tk.Frame(self, bg=BG, padx=30, pady=16)
        body.pack(fill="both", expand=True)

        # Columna izquierda (lista + acciones) y derecha (destino + opciones)
        body.columnconfigure(0, weight=3)
        body.columnconfigure(1, weight=2)
        body.rowconfigure(1, weight=1)

        # — Sección destino —
        self._section_label(body, "Directorio destino", 0, 0, colspan=2)
        self._dest_row(body, 1, 0)

        # — Separador —
        tk.Frame(body, bg=BORDER, height=1).grid(
            row=2, column=0, columnspan=2, sticky="ew", pady=12)

        # — Lista de carpetas —
        self._section_label(body, "Lista de carpetas", 3, 0)

        # Panel scrollable
        list_frame = tk.Frame(body, bg=SURFACE, bd=0,
                              highlightbackground=BORDER,
                              highlightthickness=1)
        list_frame.grid(row=4, column=0, sticky="nsew", rowspan=3)
        body.rowconfigure(4, weight=1)

        canvas = tk.Canvas(list_frame, bg=SURFACE, bd=0,
                           highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical",
                                  command=canvas.yview)
        self.scroll_frame = tk.Frame(canvas, bg=SURFACE)

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"))

        # Botones de lista
        btn_row = tk.Frame(body, bg=BG)
        btn_row.grid(row=7, column=0, sticky="ew", pady=(8, 0))

        self._btn(btn_row, "+ Agregar fila", self._add_row,
                  ACCENT, WHITE).pack(side="left", padx=(0, 6))
        self._btn(btn_row, "✕ Limpiar todo", self._clear_all,
                  SURFACE2, TEXT_DIM).pack(side="left")

        # — Panel derecho —
        right = tk.Frame(body, bg=BG)
        right.grid(row=3, column=1, rowspan=5, sticky="nsew", padx=(16, 0))

        self._section_label(right, "Importar CSV", 0, 0)
        self._csv_panel(right, 1)

        # Separador vertical simulado
        tk.Frame(body, bg=BORDER, width=1).grid(
            row=3, column=0, rowspan=5,
            sticky="ns", padx=(0, 0))  # no se muestra pero ayuda al layout

        # — Botón crear —
        create_btn = tk.Button(
            body, text="  Crear Carpetas  →",
            font=("Segoe UI Semibold", 11),
            bg=ACCENT, fg=WHITE, activebackground=ACCENT2,
            activeforeground=WHITE, relief="flat", cursor="hand2",
            pady=10, bd=0,
            command=self._create_folders
        )
        create_btn.grid(row=8, column=0, columnspan=2,
                        sticky="ew", pady=(16, 0))

        # — Status bar —
        status_bar = tk.Frame(self, bg=SURFACE2, pady=6, padx=30)
        status_bar.pack(fill="x", side="bottom")
        self.status_icon = tk.Label(status_bar, text="●",
                                    font=FONT_SM, bg=SURFACE2, fg=TEXT_DIM)
        self.status_icon.pack(side="left", padx=(0, 6))
        tk.Label(status_bar, textvariable=self.status_var,
                 font=FONT_SM, bg=SURFACE2, fg=TEXT_DIM).pack(side="left")

    def _section_label(self, parent, text, row, col, colspan=1):
        tk.Label(parent, text=text.upper(), font=("Segoe UI Semibold", 8),
                 bg=BG, fg=TEXT_DIM, pady=4).grid(
            row=row, column=col, columnspan=colspan,
            sticky="w", pady=(0, 4))

    def _dest_row(self, parent, row, col):
        frame = tk.Frame(parent, bg=BG)
        frame.grid(row=row, column=col, columnspan=2, sticky="ew", pady=(0, 4))
        frame.columnconfigure(0, weight=1)

        entry = tk.Entry(
            frame, textvariable=self.dest_path,
            font=FONT_MONO, bg=SURFACE, fg=TEXT,
            insertbackground=ACCENT, relief="flat",
            highlightbackground=BORDER, highlightthickness=1,
            bd=6
        )
        entry.grid(row=0, column=0, sticky="ew", ipady=6)

        self._btn(frame, "Examinar", self._browse_dest,
                  SURFACE2, TEXT).grid(row=0, column=1, padx=(6, 0), ipady=2)

    def _csv_panel(self, parent, row):
        frame = tk.Frame(parent, bg=SURFACE,
                         highlightbackground=BORDER, highlightthickness=1)
        frame.grid(row=row, column=0, sticky="ew", pady=(0, 12))

        inner = tk.Frame(frame, bg=SURFACE, padx=12, pady=12)
        inner.pack(fill="both")

        tk.Label(inner,
                 text="Sube un archivo CSV con los nombres\nde las carpetas separados por comas.",
                 font=FONT_SM, bg=SURFACE, fg=TEXT_DIM,
                 justify="left").pack(anchor="w")

        tk.Label(inner, text="Ejemplo:  ventas,marketing,rrhh",
                 font=("Consolas", 8), bg=SURFACE, fg=ACCENT2).pack(
            anchor="w", pady=(6, 10))

        self._btn(inner, "📂  Cargar CSV", self._load_csv,
                  ACCENT, WHITE).pack(fill="x")

        # Preview
        tk.Label(inner, text="PREVISUALIZACIÓN",
                 font=("Segoe UI Semibold", 8),
                 bg=SURFACE, fg=TEXT_DIM).pack(anchor="w", pady=(12, 4))

        self.csv_preview = tk.Text(
            inner, height=5, font=("Consolas", 8),
            bg=SURFACE2, fg=TEXT_DIM, relief="flat",
            bd=4, state="disabled",
            highlightbackground=BORDER, highlightthickness=1
        )
        self.csv_preview.pack(fill="x")

        # Botón importar
        self.import_btn = self._btn(
            inner, "↓  Importar a lista", self._import_csv_to_list,
            SUCCESS, "#0F0F13")
        self.import_btn.pack(fill="x", pady=(6, 0))
        self.import_btn.configure(state="disabled")
        self._csv_names: list[str] = []

    def _btn(self, parent, text, cmd, bg, fg):
        b = tk.Button(parent, text=text, command=cmd,
                      font=FONT_BOLD, bg=bg, fg=fg,
                      activebackground=ACCENT2, activeforeground=WHITE,
                      relief="flat", cursor="hand2", bd=0,
                      padx=12, pady=6)
        return b

    # ── Lógica de filas ────────────────────────────────────────────────────────

    def _add_row(self, name=""):
        var = tk.StringVar(value=name)
        self.folder_entries.append(var)

        idx = len(self.folder_entries) - 1
        row_frame = tk.Frame(self.scroll_frame, bg=SURFACE, pady=3, padx=8)
        row_frame.pack(fill="x", pady=1)
        row_frame.columnconfigure(1, weight=1)

        # Número
        tk.Label(row_frame,
                 text=f"{idx + 1:02d}",
                 font=("Consolas", 9), bg=SURFACE, fg=TEXT_DIM,
                 width=3).grid(row=0, column=0, padx=(0, 8))

        # Entry
        entry = tk.Entry(
            row_frame, textvariable=var,
            font=FONT_MONO, bg=SURFACE2, fg=TEXT,
            insertbackground=ACCENT, relief="flat",
            highlightbackground=BORDER, highlightthickness=1,
            bd=4
        )
        entry.grid(row=0, column=1, sticky="ew", ipady=4)
        entry.bind("<Return>", lambda e: self._add_row())

        # Botón eliminar
        del_btn = tk.Button(
            row_frame, text="✕",
            font=("Segoe UI", 8), bg=SURFACE, fg=TEXT_DIM,
            activebackground=ERROR, activeforeground=WHITE,
            relief="flat", cursor="hand2", bd=0,
            padx=6, pady=2,
            command=lambda rf=row_frame, v=var: self._remove_row(rf, v)
        )
        del_btn.grid(row=0, column=2, padx=(6, 0))

        entry.focus_set()

    def _remove_row(self, frame, var):
        if var in self.folder_entries:
            self.folder_entries.remove(var)
        frame.destroy()
        self._renumber()

    def _renumber(self):
        for i, child in enumerate(self.scroll_frame.winfo_children()):
            labels = [w for w in child.winfo_children()
                      if isinstance(w, tk.Label)]
            if labels:
                labels[0].configure(text=f"{i + 1:02d}")

    def _clear_all(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.folder_entries.clear()
        self._add_row()
        self._set_status("Lista limpiada.", TEXT_DIM)

    # ── CSV ────────────────────────────────────────────────────────────────────

    def _load_csv(self):
        path = filedialog.askopenfilename(
            title="Seleccionar CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not path:
            return

        names = []
        try:
            with open(path, newline="", encoding="utf-8-sig") as f:
                reader = csv.reader(f)
                for row in reader:
                    for cell in row:
                        clean = cell.strip()
                        if clean:
                            names.append(clean)
        except Exception as e:
            messagebox.showerror("Error al leer CSV", str(e))
            return

        self._csv_names = names
        preview = ", ".join(names[:30])
        if len(names) > 30:
            preview += f"  … +{len(names)-30} más"

        self.csv_preview.configure(state="normal")
        self.csv_preview.delete("1.0", "end")
        self.csv_preview.insert("end", preview)
        self.csv_preview.configure(state="disabled")

        self.import_btn.configure(state="normal")
        self._set_status(f"CSV cargado: {len(names)} nombre(s) encontrado(s).", SUCCESS)

    def _import_csv_to_list(self):
        if not self._csv_names:
            return
        self._clear_all()
        for name in self._csv_names:
            self._add_row(name)
        self._set_status(
            f"{len(self._csv_names)} carpeta(s) importada(s) desde CSV.", SUCCESS)

    # ── Destino ────────────────────────────────────────────────────────────────

    def _browse_dest(self):
        path = filedialog.askdirectory(
            title="Seleccionar directorio destino",
            initialdir=self.dest_path.get()
        )
        if path:
            self.dest_path.set(path)

    # ── Crear carpetas ─────────────────────────────────────────────────────────

    def _create_folders(self):
        dest = self.dest_path.get().strip()
        if not dest:
            messagebox.showwarning("Sin destino", "Por favor elige un directorio destino.")
            return

        dest_path = Path(dest)
        if not dest_path.exists():
            if messagebox.askyesno("Directorio no existe",
                                   f"El directorio no existe:\n{dest}\n\n¿Deseas crearlo?"):
                dest_path.mkdir(parents=True, exist_ok=True)
            else:
                return

        names = [v.get().strip() for v in self.folder_entries if v.get().strip()]
        if not names:
            messagebox.showwarning("Sin nombres",
                                   "Agrega al menos un nombre de carpeta.")
            return

        created, skipped, errors = [], [], []
        for name in names:
            folder = dest_path / name
            try:
                if folder.exists():
                    skipped.append(name)
                else:
                    folder.mkdir(parents=True)
                    created.append(name)
            except Exception as e:
                errors.append(f"{name}: {e}")

        # Reporte
        lines = []
        if created:
            lines.append(f"✅  {len(created)} carpeta(s) creada(s):")
            lines += [f"    • {n}" for n in created]
        if skipped:
            lines.append(f"\n⚠️  {len(skipped)} ya existía(n):")
            lines += [f"    • {n}" for n in skipped]
        if errors:
            lines.append(f"\n❌  {len(errors)} error(es):")
            lines += [f"    • {e}" for e in errors]

        msg = "\n".join(lines)
        icon = "info" if not errors else "warning"
        messagebox.showinfo("Resultado", msg) if icon == "info" \
            else messagebox.showwarning("Resultado", msg)

        color = SUCCESS if not errors else ERROR
        self._set_status(
            f"Proceso completado: {len(created)} creada(s), "
            f"{len(skipped)} omitida(s), {len(errors)} error(es).",
            color
        )

    # ── Utilidades ─────────────────────────────────────────────────────────────

    def _set_status(self, msg, color=TEXT_DIM):
        self.status_var.set(msg)
        self.status_icon.configure(fg=color)


if __name__ == "__main__":
    app = FolderCreatorApp()
    app.mainloop()
