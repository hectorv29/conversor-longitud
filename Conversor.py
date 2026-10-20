"""
Conversor de Unidades de Longitud (mm, cm, m)
Aplicación moderna desarrollada con Python y CustomTkinter.
Cumple con especificaciones de validación estricta de entrada,
precisión matemática mediante Decimal y diseño visual profesional.
"""

import sys
import os
import re
import tkinter as tk
from decimal import Decimal, InvalidOperation

try:
    import customtkinter as ctk
except ImportError:
    # Si customtkinter no estuviera instalado, avisar e intentar instalarlo
    import subprocess
    print("Instalando CustomTkinter para la interfaz moderna...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "customtkinter"])
    import customtkinter as ctk


# ----------------------------------------------------------------------
# CONSTANTES Y CONFIGURACIÓN DEL MODELO DE DATOS
# ----------------------------------------------------------------------

# Factores de conversión exactos con respecto al metro (m)
FACTORES_A_METROS = {
    "mm": Decimal("0.001"),
    "cm": Decimal("0.01"),
    "m":  Decimal("1")
}

ETIQUETAS_UNIDADES = {
    "Milímetros (mm)": "mm",
    "Centímetros (cm)": "cm",
    "Metros (m)": "m"
}

SIMBOLOS_A_ETIQUETAS = {v: k for k, v in ETIQUETAS_UNIDADES.items()}

NOMBRES_COMPLETOS = {
    "mm": "milímetros",
    "cm": "centímetros",
    "m":  "metros"
}

# Expresión regular para la validación estricta en tiempo de escritura:
# Permite únicamente:
# - Cadena vacía (al borrar)
# - Signo '-' solo al inicio
# - Dígitos 0-9
# - Máximo un separador decimal (coma ',' o punto '.')
REGEX_ENTRADA_VALIDA = re.compile(r'^-?[0-9]*[.,]?[0-9]*$')


def formatear_decimal_espanol(d: Decimal) -> str:
    """
    Convierte un objeto Decimal a cadena en formato español (coma decimal),
    evitando notación científica y eliminando ceros superfluos a la derecha.
    """
    # Formato decimal fijo (sin notación científica)
    cadena = format(d, "f")
    if "." in cadena:
        cadena = cadena.rstrip("0").rstrip(".")
    if cadena == "-0" or cadena == "":
        cadena = "0"
    return cadena.replace(".", ",")


def calcular_conversion(valor_str: str, unidad_origen_simbolo: str, unidad_destino_simbolo: str):
    """
    Realiza la conversión de longitud con precisión exacta Decimal.
    Devuelve: (valor_origen_formateado, valor_destino_formateado, factor_explicacion)
    """
    # Reemplazar coma por punto para la interpretación interna en Decimal
    valor_normalizado = valor_str.strip().replace(",", ".")
    val_decimal = Decimal(valor_normalizado)

    factor_origen = FACTORES_A_METROS[unidad_origen_simbolo]
    factor_destino = FACTORES_A_METROS[unidad_destino_simbolo]

    # Convertir primero a metros y después a la unidad destino
    en_metros = val_decimal * factor_origen
    resultado_decimal = en_metros / factor_destino

    # Explicación de equivalencia entre las unidades seleccionadas
    if unidad_origen_simbolo == unidad_destino_simbolo:
        explicacion = f"1 {unidad_origen_simbolo} = 1 {unidad_destino_simbolo} (Misma unidad)"
    else:
        relacion = factor_origen / factor_destino
        relacion_str = formatear_decimal_espanol(relacion)
        explicacion = f"1 {unidad_origen_simbolo} = {relacion_str} {unidad_destino_simbolo}"

    str_origen = formatear_decimal_espanol(val_decimal)
    str_resultado = formatear_decimal_espanol(resultado_decimal)

    return str_origen, str_resultado, explicacion


# ----------------------------------------------------------------------
# INTERFAZ GRÁFICA PRINCIPAL
# ----------------------------------------------------------------------

class ConversorLongitudApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de apariencia
        ctk.set_appearance_mode("Dark")  # Opciones: "System", "Dark", "Light"
        ctk.set_default_color_theme("blue")

        # Configuración de ventana
        self.title("Conversor de Longitud | mm · cm · m")
        self.geometry("540x700")
        self.minsize(480, 640)

        # Centrar ventana en pantalla si es posible
        self.center_window(540, 700)

        # Variables de estado
        self.unidad_origen_var = ctk.StringVar(value="Metros (m)")
        self.unidad_destino_var = ctk.StringVar(value="Centímetros (cm)")
        self.ultimo_resultado_texto = ""
        self.tema_actual = "Dark"

        # Construir interfaz
        self.crear_widgets()

        # Atajos de teclado globales
        self.bind("<Return>", lambda event: self.ejecutar_conversion())
        self.bind("<KP_Enter>", lambda event: self.ejecutar_conversion())
        self.bind("<Escape>", lambda event: self.limpiar_todo())
        self.bind("<Control-i>", lambda event: self.intercambiar_unidades())
        self.bind("<Control-I>", lambda event: self.intercambiar_unidades())

    def center_window(self, width: int, height: int):
        try:
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            x = (screen_width - width) // 2
            y = (screen_height - height) // 2
            self.geometry(f"{width}x{height}+{max(0, x)}+{max(0, y)}")
        except Exception:
            pass

    def crear_widgets(self):
        # Contenedor raíz con scroll para adaptarse a pantallas pequeñas
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.scroll_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_container.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        self.scroll_container.grid_columnconfigure(0, weight=1)

        # ---------------- 1. ENCABEZADO ----------------
        self.frame_header = ctk.CTkFrame(self.scroll_container, fg_color="transparent")
        self.frame_header.grid(row=0, column=0, sticky="ew", pady=(5, 15))
        self.frame_header.grid_columnconfigure(0, weight=1)

        # Contenedor de título e icono
        header_content = ctk.CTkFrame(self.frame_header, fg_color="transparent")
        header_content.grid(row=0, column=0, sticky="w")

        self.lbl_badge = ctk.CTkLabel(
            header_content,
            text="📏",
            font=("Segoe UI Emoji", 26),
            width=42,
            height=42,
            fg_color=("gray85", "#1e293b"),
            corner_radius=12
        )
        self.lbl_badge.pack(side="left", padx=(0, 12))

        header_text = ctk.CTkFrame(header_content, fg_color="transparent")
        header_text.pack(side="left")

        self.lbl_titulo = ctk.CTkLabel(
            header_text,
            text="Conversor de longitud",
            font=("Segoe UI", 22, "bold"),
            anchor="w"
        )
        self.lbl_titulo.pack(anchor="w")

        self.lbl_subtitulo = ctk.CTkLabel(
            header_text,
            text="Conversión exacta entre milímetros, centímetros y metros",
            font=("Segoe UI", 12),
            text_color=("gray40", "gray70"),
            anchor="w"
        )
        self.lbl_subtitulo.pack(anchor="w")

        # Botón de alternancia de tema Claro / Oscuro
        self.btn_tema = ctk.CTkButton(
            self.frame_header,
            text="☀️ Claro" if self.tema_actual == "Dark" else "🌙 Oscuro",
            font=("Segoe UI", 12, "bold"),
            width=85,
            height=32,
            corner_radius=8,
            fg_color=("gray80", "#334155"),
            hover_color=("gray70", "#475569"),
            text_color=("gray10", "white"),
            command=self.alternar_tema
        )
        self.btn_tema.grid(row=0, column=1, sticky="e")

        # ---------------- 2. TARJETA PRINCIPAL ----------------
        self.card = ctk.CTkFrame(
            self.scroll_container,
            corner_radius=18,
            fg_color=("white", "#1e293b"),
            border_width=1,
            border_color=("gray80", "#334155")
        )
        self.card.grid(row=1, column=0, sticky="ew", pady=(0, 15), padx=2)
        self.card.grid_columnconfigure(0, weight=1)

        # Padding interior del panel principal
        card_inner = ctk.CTkFrame(self.card, fg_color="transparent")
        card_inner.pack(fill="both", expand=True, padx=22, pady=22)
        card_inner.grid_columnconfigure(0, weight=1)

        # SECCIÓN A: Campo de entrada numérico
        sec_num_label_row = ctk.CTkFrame(card_inner, fg_color="transparent")
        sec_num_label_row.pack(fill="x", pady=(0, 6))

        ctk.CTkLabel(
            sec_num_label_row,
            text="VALOR NUMÉRICO",
            font=("Segoe UI", 11, "bold"),
            text_color=("gray40", "#94a3b8")
        ).pack(side="left")

        ctk.CTkLabel(
            sec_num_label_row,
            text="(admite dígitos, coma/punto y signo negativo)",
            font=("Segoe UI", 10),
            text_color=("gray50", "#64748b")
        ).pack(side="right")

        # Validación en tiempo real conectada a Tkinter
        vcmd = (self.register(self.validar_caracteres_entrada), "%P")

        self.entry_valor = ctk.CTkEntry(
            card_inner,
            placeholder_text="Introduce un número (ej. 2,5 o -10)",
            font=("Segoe UI", 18, "bold"),
            height=50,
            corner_radius=12,
            border_width=1.5,
            border_color=("gray70", "#475569"),
            fg_color=("gray95", "#0f172a"),
            text_color=("black", "white")
        )
        # Aplicar el comando de validación sobre el Entry subyacente
        self.entry_valor._entry.configure(validate="key", validatecommand=vcmd)
        self.entry_valor.pack(fill="x", pady=(0, 4))

        # Configurar interceptor estricto para pegar desde el portapapeles
        self.configurar_control_portapapeles()

        # Configurar menú contextual con clic derecho (Cortar, Copiar, Pegar)
        self.configurar_menu_contextual()

        # Mensaje de error/validación integrado (altura fija mínima para evitar saltos de interfaz)
        self.lbl_error = ctk.CTkLabel(
            card_inner,
            text="",
            font=("Segoe UI", 12, "bold"),
            text_color="#ef4444",
            anchor="w",
            height=20
        )
        self.lbl_error.pack(fill="x", pady=(0, 10))

        # SECCIÓN B: Selectores de Unidades con botón de intercambio
        sec_units_lbl = ctk.CTkLabel(
            card_inner,
            text="UNIDADES DE CONVERSIÓN",
            font=("Segoe UI", 11, "bold"),
            text_color=("gray40", "#94a3b8"),
            anchor="w"
        )
        sec_units_lbl.pack(fill="x", pady=(5, 6))

        unidades_opciones = ["Metros (m)", "Centímetros (cm)", "Milímetros (mm)"]

        frame_units_row = ctk.CTkFrame(card_inner, fg_color="transparent")
        frame_units_row.pack(fill="x", pady=(0, 18))
        frame_units_row.grid_columnconfigure((0, 2), weight=1)
        frame_units_row.grid_columnconfigure(1, weight=0)

        # Columna Origen
        col_origen = ctk.CTkFrame(frame_units_row, fg_color="transparent")
        col_origen.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        ctk.CTkLabel(
            col_origen,
            text="De (origen):",
            font=("Segoe UI", 12, "bold"),
            text_color=("gray30", "gray85"),
            anchor="w"
        ).pack(fill="x", pady=(0, 4))

        self.menu_origen = ctk.CTkOptionMenu(
            col_origen,
            values=unidades_opciones,
            variable=self.unidad_origen_var,
            font=("Segoe UI", 13, "bold"),
            dropdown_font=("Segoe UI", 12),
            height=42,
            corner_radius=10,
            fg_color=("gray85", "#334155"),
            button_color=("gray75", "#475569"),
            button_hover_color=("gray65", "#64748b"),
            text_color=("black", "white")
        )
        self.menu_origen.pack(fill="x")

        # Botón Intercambiar Unidades (⇄)
        self.btn_swap = ctk.CTkButton(
            frame_units_row,
            text="⇄",
            font=("Segoe UI", 18, "bold"),
            width=44,
            height=42,
            corner_radius=10,
            fg_color=("gray85", "#334155"),
            hover_color=("gray75", "#475569"),
            text_color=("gray20", "white"),
            command=self.intercambiar_unidades
        )
        self.btn_swap.grid(row=0, column=1, padx=6, sticky="s")

        # Columna Destino
        col_destino = ctk.CTkFrame(frame_units_row, fg_color="transparent")
        col_destino.grid(row=0, column=2, sticky="ew", padx=(6, 0))
        ctk.CTkLabel(
            col_destino,
            text="A (destino):",
            font=("Segoe UI", 12, "bold"),
            text_color=("gray30", "gray85"),
            anchor="w"
        ).pack(fill="x", pady=(0, 4))

        self.menu_destino = ctk.CTkOptionMenu(
            col_destino,
            values=unidades_opciones,
            variable=self.unidad_destino_var,
            font=("Segoe UI", 13, "bold"),
            dropdown_font=("Segoe UI", 12),
            height=42,
            corner_radius=10,
            fg_color=("gray85", "#334155"),
            button_color=("gray75", "#475569"),
            button_hover_color=("gray65", "#64748b"),
            text_color=("black", "white")
        )
        self.menu_destino.pack(fill="x")

        # SECCIÓN C: Botones Principales (Convertir y Limpiar)
        frame_botones = ctk.CTkFrame(card_inner, fg_color="transparent")
        frame_botones.pack(fill="x", pady=(5, 18))
        frame_botones.grid_columnconfigure(0, weight=3)
        frame_botones.grid_columnconfigure(1, weight=2)

        self.btn_convertir = ctk.CTkButton(
            frame_botones,
            text="Convertir ↵",
            font=("Segoe UI", 15, "bold"),
            height=46,
            corner_radius=12,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            text_color="white",
            command=self.ejecutar_conversion
        )
        self.btn_convertir.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        self.btn_limpiar = ctk.CTkButton(
            frame_botones,
            text="Limpiar ⟲",
            font=("Segoe UI", 14, "bold"),
            height=46,
            corner_radius=12,
            fg_color=("gray80", "#334155"),
            hover_color=("gray70", "#475569"),
            text_color=("gray10", "white"),
            command=self.limpiar_todo
        )
        self.btn_limpiar.grid(row=0, column=1, sticky="ew", padx=(8, 0))

        # SECCIÓN D: Zona destacada para la Presentación del Resultado
        self.frame_resultado = ctk.CTkFrame(
            card_inner,
            corner_radius=14,
            fg_color=("gray95", "#0f172a"),
            border_width=1.5,
            border_color=("gray80", "#334155")
        )
        self.frame_resultado.pack(fill="x", pady=(5, 5))

        self.inner_res_container = ctk.CTkFrame(self.frame_resultado, fg_color="transparent")
        self.inner_res_container.pack(fill="both", expand=True, padx=18, pady=16)

        # Mostrar estado inicial vacío del resultado
        self.mostrar_resultado_placeholder()

        # ---------------- 3. ACCESOS RÁPIDOS / EJEMPLOS DE PRUEBA ----------------
        self.frame_ejemplos = ctk.CTkFrame(
            self.scroll_container,
            corner_radius=14,
            fg_color=("gray95", "#1e293b"),
            border_width=1,
            border_color=("gray85", "#334155")
        )
        self.frame_ejemplos.grid(row=2, column=0, sticky="ew", pady=(0, 10), padx=2)

        ejemplos_inner = ctk.CTkFrame(self.frame_ejemplos, fg_color="transparent")
        ejemplos_inner.pack(fill="x", padx=16, pady=12)

        ctk.CTkLabel(
            ejemplos_inner,
            text="EJEMPLOS RÁPIDOS DE COMPROBACIÓN",
            font=("Segoe UI", 10, "bold"),
            text_color=("gray40", "#94a3b8"),
            anchor="w"
        ).pack(fill="x", pady=(0, 6))

        chips_frame = ctk.CTkFrame(ejemplos_inner, fg_color="transparent")
        chips_frame.pack(fill="x")

        # Lista de ejemplos solicitados en el enunciado
        ejemplos = [
            ("1 m → cm", "1", "Metros (m)", "Centímetros (cm)"),
            ("1 m → mm", "1", "Metros (m)", "Milímetros (mm)"),
            ("1 cm → mm", "1", "Centímetros (cm)", "Milímetros (mm)"),
            ("250 mm → cm", "250", "Milímetros (mm)", "Centímetros (cm)"),
            ("150 cm → m", "150", "Centímetros (cm)", "Metros (m)"),
            ("-2,5 m → cm", "-2,5", "Metros (m)", "Centímetros (cm)"),
        ]

        # Colocar botones en 2 filas
        for idx, (lbl, val, u_orig, u_dest) in enumerate(ejemplos):
            r = idx // 3
            c = idx % 3
            chips_frame.grid_columnconfigure(c, weight=1)
            btn_chip = ctk.CTkButton(
                chips_frame,
                text=lbl,
                font=("Segoe UI", 11),
                height=28,
                corner_radius=8,
                fg_color=("white", "#0f172a"),
                hover_color=("gray90", "#334155"),
                text_color=("gray20", "#cbd5e1"),
                border_width=1,
                border_color=("gray80", "#334155"),
                command=lambda v=val, o=u_orig, d=u_dest: self.cargar_ejemplo(v, o, d)
            )
            btn_chip.grid(row=r, column=c, padx=3, pady=3, sticky="ew")

        # ---------------- 4. PIE DE PÁGINA Y ATAJOS ----------------
        self.frame_footer = ctk.CTkFrame(self.scroll_container, fg_color="transparent")
        self.frame_footer.grid(row=3, column=0, sticky="ew", pady=(5, 5))

        lbl_atajos = ctk.CTkLabel(
            self.frame_footer,
            text="⌨ Atajos: Enter para convertir  •  Esc para limpiar  •  Ctrl+I para invertir unidades",
            font=("Segoe UI", 11),
            text_color=("gray50", "#64748b")
        )
        lbl_atajos.pack(anchor="center")

    # ------------------------------------------------------------------
    # VALIDACIÓN DEL CAMPO NUMÉRICO (EN TIEMPO REAL Y PORTAPAPELES)
    # ------------------------------------------------------------------

    def validar_caracteres_entrada(self, texto_propuesto: str) -> bool:
        """
        Callback de Tkinter para validate='key'.
        Impide físicamente que se introduzcan caracteres no válidos.
        Permite: dígitos 0-9, un único signo '-' al inicio, y máximo una coma o punto.
        """
        # La expresión regular acepta estados parciales mientras el usuario escribe:
        # "", "-", ".", ",", "-.", "-,", "25", "2,5", "-10", etc.
        es_valido = bool(REGEX_ENTRADA_VALIDA.fullmatch(texto_propuesto))

        if es_valido:
            # Si el usuario está corrigiendo y el texto es válido, retirar mensaje de error previo
            if self.lbl_error.cget("text") and texto_propuesto not in ("", "-", ".", ",", "-.", "-,"):
                self.ocultar_error()
        return es_valido

    def configurar_control_portapapeles(self):
        """
        Intercepta los eventos de pegar (Ctrl+V, Shift+Insert, <<Paste>>)
        para evitar que se introduzcan letras o caracteres inválidos copiados.
        """
        tk_entry = self.entry_valor._entry

        def interceptar_pegar(event=None):
            try:
                contenido_portapapeles = self.clipboard_get()
            except Exception:
                return "break"

            # Limpiar posibles espacios accidentales y normalizar signos tipográficos
            limpio = contenido_portapapeles.strip().replace("−", "-").replace("–", "-")

            texto_actual = tk_entry.get()

            # Verificar si hay una selección activa que sería reemplazada
            try:
                start = tk_entry.index("sel.first")
                end = tk_entry.index("sel.last")
                propuesto = texto_actual[:start] + limpio + texto_actual[end:]
                indice_insercion = start
                tiene_seleccion = True
            except tk.TclError:
                pos_cursor = tk_entry.index("insert")
                propuesto = texto_actual[:pos_cursor] + limpio + texto_actual[pos_cursor:]
                indice_insercion = pos_cursor
                tiene_seleccion = False

            # Validar si el resultado final cumpliría la regla
            if REGEX_ENTRADA_VALIDA.fullmatch(propuesto):
                if tiene_seleccion:
                    tk_entry.delete("sel.first", "sel.last")
                tk_entry.insert(indice_insercion, limpio)
                tk_entry.icursor(indice_insercion + len(limpio))
                self.ocultar_error()
            else:
                self.mostrar_error("El texto pegado contiene caracteres no permitidos.")

            return "break"

        tk_entry.bind("<<Paste>>", interceptar_pegar)
        tk_entry.bind("<Control-v>", interceptar_pegar)
        tk_entry.bind("<Control-V>", interceptar_pegar)
        tk_entry.bind("<Shift-Insert>", interceptar_pegar)

    def configurar_menu_contextual(self):
        """
        Añade menú emergente con clic derecho para Cortar, Copiar y Pegar con validación.
        """
        tk_entry = self.entry_valor._entry

        def mostrar_popup(event):
            menu = tk.Menu(self, tearoff=0)
            menu.add_command(
                label="Copiar",
                command=lambda: tk_entry.event_generate("<<Copy>>")
            )
            menu.add_command(
                label="Cortar",
                command=lambda: tk_entry.event_generate("<<Cut>>")
            )
            menu.add_command(
                label="Pegar",
                command=lambda: tk_entry.event_generate("<<Paste>>")
            )
            menu.add_separator()
            menu.add_command(
                label="Seleccionar todo",
                command=lambda: tk_entry.select_range(0, "end")
            )
            try:
                menu.tk_popup(event.x_root, event.y_root)
            finally:
                menu.grab_release()

        tk_entry.bind("<Button-3>", mostrar_popup)

    # ------------------------------------------------------------------
    # GESTIÓN DE ERRORES Y ESTADOS VISUALES
    # ------------------------------------------------------------------

    def mostrar_error(self, mensaje: str):
        """Muestra un mensaje de error integrado sin alterar el diseño ni emitir alertas modales."""
        self.lbl_error.configure(text=f"⚠ {mensaje}")
        self.entry_valor.configure(border_color="#ef4444")

    def ocultar_error(self):
        """Elimina el mensaje de error y restablece el estilo del campo de entrada."""
        self.lbl_error.configure(text="")
        color_borde = ("gray70", "#475569")
        self.entry_valor.configure(border_color=color_borde)

    # ------------------------------------------------------------------
    # CONVERSIÓN Y LÓGICA DE NEGOCIO
    # ------------------------------------------------------------------

    def ejecutar_conversion(self):
        """
        Valida los datos y ejecuta el cálculo únicamente al pulsar el botón 'Convertir'.
        """
        texto = self.entry_valor.get().strip()

        # 1. Comprobar campo vacío
        if not texto:
            self.mostrar_error("Introduce un valor para realizar la conversión.")
            return

        # 2. Comprobar valores incompletos como solo '-', '.', ',' o '-.'
        if texto in ("-", ".", ",", "-.", "-,"):
            self.mostrar_error("Introduce un número válido (ej. 25, 2,5 o -10).")
            return

        # 3. Intentar procesar como Decimal
        origen_etiqueta = self.unidad_origen_var.get()
        destino_etiqueta = self.unidad_destino_var.get()

        simb_origen = ETIQUETAS_UNIDADES[origen_etiqueta]
        simb_destino = ETIQUETAS_UNIDADES[destino_etiqueta]

        try:
            val_origen_fmt, val_destino_fmt, explicacion = calcular_conversion(
                texto, simb_origen, simb_destino
            )
        except (InvalidOperation, ValueError, Exception):
            self.mostrar_error("No se ha podido interpretar el valor como un número válido.")
            return

        # Si todo es correcto, limpiar errores y mostrar el resultado destacado
        self.ocultar_error()
        self.mostrar_resultado_destacado(
            val_origen_fmt, simb_origen, val_destino_fmt, simb_destino, explicacion
        )

    def mostrar_resultado_destacado(self, val_orig: str, simb_orig: str, val_dest: str, simb_dest: str, explicacion: str):
        """Presenta el resultado de manera clara, destacada y diferenciada."""
        # Limpiar widgets previos del contenedor de resultados
        for child in self.inner_res_container.winfo_children():
            child.destroy()

        self.frame_resultado.configure(
            border_color=("#3b82f6", "#2563eb"),
            fg_color=("gray95", "#0f172a")
        )

        # Fila superior: Etiqueta 'RESULTADO' + Botón 'Copiar'
        top_row = ctk.CTkFrame(self.inner_res_container, fg_color="transparent")
        top_row.pack(fill="x", pady=(0, 6))

        badge = ctk.CTkLabel(
            top_row,
            text="RESULTADO DE LA CONVERSIÓN",
            font=("Segoe UI", 11, "bold"),
            text_color=("#2563eb", "#60a5fa"),
            anchor="w"
        )
        badge.pack(side="left")

        # Texto que se copiará al portapapeles
        texto_copiar = f"{val_orig} {simb_orig} = {val_dest} {simb_dest}"
        self.ultimo_resultado_texto = texto_copiar

        btn_copiar = ctk.CTkButton(
            top_row,
            text="📋 Copiar",
            font=("Segoe UI", 11, "bold"),
            width=70,
            height=26,
            corner_radius=6,
            fg_color=("gray85", "#1e293b"),
            hover_color=("gray75", "#334155"),
            text_color=("gray20", "#cbd5e1"),
            command=lambda: self.copiar_resultado(btn_copiar, texto_copiar)
        )
        btn_copiar.pack(side="right")

        # Valor destacado (Hero number)
        lbl_hero = ctk.CTkLabel(
            self.inner_res_container,
            text=f"{val_dest} {simb_dest}",
            font=("Segoe UI", 32, "bold"),
            text_color=("black", "white"),
            anchor="w"
        )
        lbl_hero.pack(fill="x", pady=(2, 4))

        # Ecuación completa clara: 2,5 m = 250 cm
        lbl_ecuacion = ctk.CTkLabel(
            self.inner_res_container,
            text=f"{val_orig} {simb_orig}  =  {val_dest} {simb_dest}",
            font=("Segoe UI", 16, "bold"),
            text_color=("#1d4ed8", "#93c5fd"),
            anchor="w"
        )
        lbl_ecuacion.pack(fill="x", pady=(0, 6))

        # Fila inferior: factor o relación de equivalencia
        lbl_factor = ctk.CTkLabel(
            self.inner_res_container,
            text=f"Equivalencia: {explicacion}",
            font=("Segoe UI", 11),
            text_color=("gray50", "#94a3b8"),
            anchor="w"
        )
        lbl_factor.pack(fill="x")

    def mostrar_resultado_placeholder(self):
        """Muestra el estado inicial / vacío del área de resultados."""
        for child in self.inner_res_container.winfo_children():
            child.destroy()

        self.frame_resultado.configure(
            border_color=("gray85", "#334155"),
            fg_color=("gray95", "#0f172a")
        )

        holder = ctk.CTkFrame(self.inner_res_container, fg_color="transparent")
        holder.pack(fill="both", expand=True, pady=12)

        lbl_icon = ctk.CTkLabel(
            holder,
            text="📐",
            font=("Segoe UI Emoji", 24),
            text_color=("gray60", "gray50")
        )
        lbl_icon.pack(pady=(0, 4))

        lbl_placeholder = ctk.CTkLabel(
            holder,
            text="Introduce un valor y pulsa «Convertir» para ver el cálculo",
            font=("Segoe UI", 13, "bold"),
            text_color=("gray50", "#94a3b8")
        )
        lbl_placeholder.pack()

        lbl_hint = ctk.CTkLabel(
            holder,
            text="El resultado no se calculará automáticamente hasta que pulses el botón",
            font=("Segoe UI", 11),
            text_color=("gray60", "#64748b")
        )
        lbl_hint.pack(pady=(2, 0))

    def copiar_resultado(self, boton: ctk.CTkButton, texto: str):
        """Copia el resultado formateado al portapapeles y da feedback visual en el botón."""
        try:
            self.clipboard_clear()
            self.clipboard_append(texto)
            self.update()
            boton.configure(text="✓ Copiado!", fg_color="#10b981", text_color="white")
            self.after(2000, lambda: boton.configure(
                text="📋 Copiar",
                fg_color=("gray85", "#1e293b"),
                text_color=("gray20", "#cbd5e1")
            ))
        except Exception:
            pass

    # ------------------------------------------------------------------
    # ACCIONES: LIMPIAR, INTERCAMBIAR, EJEMPLOS Y TEMA
    # ------------------------------------------------------------------

    def limpiar_todo(self):
        """
        Restaura el programa exactamente a su estado inicial:
        1. Borra el número introducido.
        2. Elimina el resultado de la conversión.
        3. Elimina cualquier mensaje de error o validación.
        4. Restaura los selectores de unidades a sus valores predeterminados.
        5. Devuelve el foco al campo de texto.
        """
        # 1. Borrar entrada
        self.entry_valor.delete(0, "end")

        # 2. Eliminar resultado
        self.ultimo_resultado_texto = ""
        self.mostrar_resultado_placeholder()

        # 3. Eliminar errores
        self.ocultar_error()

        # 4. Restaurar unidades predeterminadas (Metros -> Centímetros)
        self.unidad_origen_var.set("Metros (m)")
        self.unidad_destino_var.set("Centímetros (cm)")

        # 5. Enfocar el campo para facilitar una nueva entrada
        self.entry_valor.focus()

    def intercambiar_unidades(self):
        """Intercambia rápidamente las unidades de origen y destino sin recalcular automáticamente."""
        origen_actual = self.unidad_origen_var.get()
        destino_actual = self.unidad_destino_var.get()

        self.unidad_origen_var.set(destino_actual)
        self.unidad_destino_var.set(origen_actual)

    def cargar_ejemplo(self, valor: str, u_orig: str, u_dest: str):
        """Carga uno de los ejemplos preconfigurados para facilitar la evaluación."""
        self.entry_valor.delete(0, "end")
        self.entry_valor.insert(0, valor)
        self.unidad_origen_var.set(u_orig)
        self.unidad_destino_var.set(u_dest)
        self.ocultar_error()
        self.entry_valor.focus()

    def alternar_tema(self):
        """Permite al usuario cambiar entre Modo Oscuro y Modo Claro."""
        if self.tema_actual == "Dark":
            ctk.set_appearance_mode("Light")
            self.tema_actual = "Light"
            self.btn_tema.configure(text="🌙 Oscuro")
        else:
            ctk.set_appearance_mode("Dark")
            self.tema_actual = "Dark"
            self.btn_tema.configure(text="☀️ Claro")


# ----------------------------------------------------------------------
# PUNTO DE ENTRADA PRINCIPAL
# ----------------------------------------------------------------------

def main():
    app = ConversorLongitudApp()
    app.mainloop()


if __name__ == "__main__":
    main()

