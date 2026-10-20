"""
Interfaz gráfica del Conversor de Unidades de Longitud.
Desarrollada con CustomTkinter según la especificación SPEC.md.
"""

import tkinter as tk
import customtkinter as ctk

from logica import (
    ETIQUETAS_UNIDADES,
    es_entrada_valida,
    validar_para_conversion,
    convertir_longitud,
    intercambiar_unidades
)


class ConversorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de apariencia moderna
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # Configuración de la ventana
        self.title("Conversor de longitud")
        self.geometry("500x620")
        self.minsize(440, 560)

        # Centrar ventana en pantalla si está disponible
        self.centrar_ventana(500, 620)

        # Variables de estado para los selectores de unidades
        self.var_origen = ctk.StringVar(value="Metros (m)")
        self.var_destino = ctk.StringVar(value="Centímetros (cm)")

        # Construcción de componentes gráficos
        self.construir_interfaz()

        # Atajos de teclado para accesibilidad
        self.bind("<Return>", lambda event: self.accion_convertir())
        self.bind("<KP_Enter>", lambda event: self.accion_convertir())
        self.bind("<Escape>", lambda event: self.accion_limpiar())
        self.bind("<Control-i>", lambda event: self.accion_intercambiar())
        self.bind("<Control-I>", lambda event: self.accion_intercambiar())

    def centrar_ventana(self, ancho: int, alto: int):
        try:
            pantalla_ancho = self.winfo_screenwidth()
            pantalla_alto = self.winfo_screenheight()
            x = (pantalla_ancho - ancho) // 2
            y = (pantalla_alto - alto) // 2
            self.geometry(f"{ancho}x{alto}+{max(0, x)}+{max(0, y)}")
        except Exception:
            pass

    def construir_interfaz(self):
        # Contenedor principal con margen
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        contenedor = ctk.CTkFrame(self, fg_color="transparent")
        contenedor.grid(row=0, column=0, sticky="nsew", padx=24, pady=24)
        contenedor.grid_columnconfigure(0, weight=1)

        # ---------------- 1. ENCABEZADO ----------------
        frame_cabecera = ctk.CTkFrame(contenedor, fg_color="transparent")
        frame_cabecera.pack(fill="x", pady=(0, 16))

        lbl_titulo = ctk.CTkLabel(
            frame_cabecera,
            text="Conversor de longitud",
            font=("Segoe UI", 22, "bold"),
            anchor="w"
        )
        lbl_titulo.pack(anchor="w")

        lbl_subtitulo = ctk.CTkLabel(
            frame_cabecera,
            text="Convierte unidades entre milímetros (mm), centímetros (cm) y metros (m)",
            font=("Segoe UI", 12),
            text_color=("gray40", "gray70"),
            anchor="w"
        )
        lbl_subtitulo.pack(anchor="w")

        # ---------------- 2. TARJETA PRINCIPAL ----------------
        tarjeta = ctk.CTkFrame(
            contenedor,
            corner_radius=16,
            fg_color=("white", "#1e293b"),
            border_width=1,
            border_color=("gray80", "#334155")
        )
        tarjeta.pack(fill="both", expand=True)

        tarjeta_interna = ctk.CTkFrame(tarjeta, fg_color="transparent")
        tarjeta_interna.pack(fill="both", expand=True, padx=20, pady=20)
        tarjeta_interna.grid_columnconfigure(0, weight=1)

        # SECCIÓN: Campo de entrada numérico
        lbl_entrada = ctk.CTkLabel(
            tarjeta_interna,
            text="Valor numérico:",
            font=("Segoe UI", 12, "bold"),
            anchor="w"
        )
        lbl_entrada.pack(fill="x", pady=(0, 6))

        # Validación en tiempo real (validate='key')
        vcmd = (self.register(self.validar_tecleo), "%P")

        self.entry_valor = ctk.CTkEntry(
            tarjeta_interna,
            placeholder_text="Ej: 2,5 o -10",
            font=("Segoe UI", 18, "bold"),
            height=48,
            corner_radius=10,
            border_width=1.5,
            border_color=("gray70", "#475569"),
            fg_color=("gray95", "#0f172a")
        )
        # Configurar validación sobre el widget Entry interno
        self.entry_valor._entry.configure(validate="key", validatecommand=vcmd)
        self.entry_valor.pack(fill="x", pady=(0, 2))

        # Control estricto del portapapeles para evitar pegar letras o símbolos
        self.configurar_control_pegado()

        # Mensaje de error/validación integrado con altura fija para no mover la interfaz
        self.lbl_error = ctk.CTkLabel(
            tarjeta_interna,
            text="",
            font=("Segoe UI", 12, "bold"),
            text_color="#ef4444",
            anchor="w",
            height=20
        )
        self.lbl_error.pack(fill="x", pady=(0, 10))

        # SECCIÓN: Selectores de unidades de origen y destino
        frame_selectores = ctk.CTkFrame(tarjeta_interna, fg_color="transparent")
        frame_selectores.pack(fill="x", pady=(0, 18))
        frame_selectores.grid_columnconfigure((0, 1), weight=1)

        opciones_unidades = list(ETIQUETAS_UNIDADES.keys())

        # Columna Origen
        col_orig = ctk.CTkFrame(frame_selectores, fg_color="transparent")
        col_orig.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        lbl_de = ctk.CTkLabel(
            col_orig,
            text="Unidad de origen:",
            font=("Segoe UI", 12, "bold"),
            anchor="w"
        )
        lbl_de.pack(fill="x", pady=(0, 4))

        self.menu_origen = ctk.CTkOptionMenu(
            col_orig,
            values=opciones_unidades,
            variable=self.var_origen,
            font=("Segoe UI", 13),
            dropdown_font=("Segoe UI", 12),
            height=40,
            corner_radius=8
        )
        self.menu_origen.pack(fill="x")

        # Columna Destino
        col_dest = ctk.CTkFrame(frame_selectores, fg_color="transparent")
        col_dest.grid(row=0, column=1, sticky="ew", padx=(8, 0))

        lbl_a = ctk.CTkLabel(
            col_dest,
            text="Unidad de destino:",
            font=("Segoe UI", 12, "bold"),
            anchor="w"
        )
        lbl_a.pack(fill="x", pady=(0, 4))

        self.menu_destino = ctk.CTkOptionMenu(
            col_dest,
            values=opciones_unidades,
            variable=self.var_destino,
            font=("Segoe UI", 13),
            dropdown_font=("Segoe UI", 12),
            height=40,
            corner_radius=8
        )
        self.menu_destino.pack(fill="x")

        # Botón Intercambiar unidades
        self.btn_intercambiar = ctk.CTkButton(
            frame_selectores,
            text="⇄ Intercambiar unidades",
            font=("Segoe UI", 12, "bold"),
            height=34,
            corner_radius=8,
            fg_color=("gray85", "#334155"),
            hover_color=("gray75", "#475569"),
            text_color=("gray10", "white"),
            command=self.accion_intercambiar
        )
        self.btn_intercambiar.grid(row=1, column=0, columnspan=2, pady=(10, 0), sticky="ew")

        # SECCIÓN: Botones Convertir y Limpiar
        frame_botones = ctk.CTkFrame(tarjeta_interna, fg_color="transparent")
        frame_botones.pack(fill="x", pady=(0, 18))
        frame_botones.grid_columnconfigure(0, weight=3)
        frame_botones.grid_columnconfigure(1, weight=2)

        self.btn_convertir = ctk.CTkButton(
            frame_botones,
            text="Convertir",
            font=("Segoe UI", 14, "bold"),
            height=44,
            corner_radius=10,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            command=self.accion_convertir
        )
        self.btn_convertir.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        self.btn_limpiar = ctk.CTkButton(
            frame_botones,
            text="Limpiar",
            font=("Segoe UI", 14),
            height=44,
            corner_radius=10,
            fg_color=("gray80", "#334155"),
            hover_color=("gray70", "#475569"),
            text_color=("gray10", "white"),
            command=self.accion_limpiar
        )
        self.btn_limpiar.grid(row=0, column=1, sticky="ew", padx=(8, 0))

        # SECCIÓN: Zona específica para presentar el resultado
        self.frame_resultado = ctk.CTkFrame(
            tarjeta_interna,
            corner_radius=12,
            fg_color=("gray95", "#0f172a"),
            border_width=1.5,
            border_color=("gray85", "#334155")
        )
        self.frame_resultado.pack(fill="both", expand=True)

        self.contenedor_resultado = ctk.CTkFrame(self.frame_resultado, fg_color="transparent")
        self.contenedor_resultado.pack(fill="both", expand=True, padx=16, pady=16)

        # Mostrar estado inicial del resultado
        self.mostrar_placeholder_resultado()

    # ---------------- VALIDACIÓN DE ENTRADA Y PORTAPAPELES ----------------

    def validar_tecleo(self, texto_propuesto: str) -> bool:
        """Impide físicamente introducir caracteres no permitidos al escribir."""
        es_valido = es_entrada_valida(texto_propuesto)
        if es_valido and self.lbl_error.cget("text"):
            # Si el usuario corrige la entrada, se oculta el error previo
            self.ocultar_error()
        return es_valido

    def configurar_control_pegado(self):
        """Intercepta los eventos de pegado para filtrar contenido del portapapeles."""
        tk_entry = self.entry_valor._entry

        def interceptar_pegado(event=None):
            try:
                clip = self.clipboard_get()
            except Exception:
                return "break"

            texto_limpio = clip.strip().replace("−", "-").replace("–", "-")
            actual = tk_entry.get()

            # Determinar si existe texto seleccionado a reemplazar
            try:
                start = tk_entry.index("sel.first")
                end = tk_entry.index("sel.last")
                propuesto = actual[:start] + texto_limpio + actual[end:]
                pos_insert = start
                con_seleccion = True
            except tk.TclError:
                pos = tk_entry.index("insert")
                propuesto = actual[:pos] + texto_limpio + actual[pos:]
                pos_insert = pos
                con_seleccion = False

            if es_entrada_valida(propuesto):
                if con_seleccion:
                    tk_entry.delete("sel.first", "sel.last")
                tk_entry.insert(pos_insert, texto_limpio)
                tk_entry.icursor(pos_insert + len(texto_limpio))
                self.ocultar_error()
            else:
                self.mostrar_error("El texto pegado contiene caracteres no permitidos.")

            return "break"

        tk_entry.bind("<<Paste>>", interceptar_pegado)
        tk_entry.bind("<Control-v>", interceptar_pegado)
        tk_entry.bind("<Control-V>", interceptar_pegado)
        tk_entry.bind("<Shift-Insert>", interceptar_pegado)

    # ---------------- GESTIÓN DE ERRORES ----------------

    def mostrar_error(self, mensaje: str):
        self.lbl_error.configure(text=f"• {mensaje}")
        self.entry_valor.configure(border_color="#ef4444")

    def ocultar_error(self):
        self.lbl_error.configure(text="")
        self.entry_valor.configure(border_color=("gray70", "#475569"))

    # ---------------- ACCIÓN CONVERTIR ----------------

    def accion_convertir(self):
        texto = self.entry_valor.get()
        valido, mensaje_error, val_decimal = validar_para_conversion(texto)

        if not valido:
            self.mostrar_error(mensaje_error)
            return

        self.ocultar_error()

        simb_orig = ETIQUETAS_UNIDADES[self.var_origen.get()]
        simb_dest = ETIQUETAS_UNIDADES[self.var_destino.get()]

        str_orig, str_dest, ecuacion = convertir_longitud(val_decimal, simb_orig, simb_dest)
        self.mostrar_resultado_destacado(str_orig, simb_orig, str_dest, simb_dest, ecuacion)

    def mostrar_resultado_destacado(self, str_orig: str, simb_orig: str, str_dest: str, simb_dest: str, ecuacion: str):
        self.resultado_mostrado = ecuacion

        # Limpiar contenedor de resultado
        for hijo in self.contenedor_resultado.winfo_children():
            hijo.destroy()

        self.frame_resultado.configure(border_color=("#3b82f6", "#2563eb"))

        lbl_tag = ctk.CTkLabel(
            self.contenedor_resultado,
            text="RESULTADO",
            font=("Segoe UI", 11, "bold"),
            text_color=("#2563eb", "#60a5fa"),
            anchor="w"
        )
        lbl_tag.pack(fill="x", pady=(0, 4))

        lbl_destacado = ctk.CTkLabel(
            self.contenedor_resultado,
            text=f"{str_dest} {simb_dest}",
            font=("Segoe UI", 28, "bold"),
            text_color=("black", "white"),
            anchor="w"
        )
        lbl_destacado.pack(fill="x", pady=(0, 4))

        lbl_ecuacion = ctk.CTkLabel(
            self.contenedor_resultado,
            text=ecuacion,
            font=("Segoe UI", 15, "bold"),
            text_color=("#1d4ed8", "#93c5fd"),
            anchor="w"
        )
        lbl_ecuacion.pack(fill="x")

    def mostrar_placeholder_resultado(self):
        self.resultado_mostrado = "—"

        for hijo in self.contenedor_resultado.winfo_children():
            hijo.destroy()

        self.frame_resultado.configure(border_color=("gray85", "#334155"))

        lbl_vacio = ctk.CTkLabel(
            self.contenedor_resultado,
            text="—",
            font=("Segoe UI", 28, "bold"),
            text_color=("gray50", "#94a3b8")
        )
        lbl_vacio.pack(expand=True)

    # ---------------- ACCIÓN INTERCAMBIAR ----------------

    def accion_intercambiar(self):
        """
        Intercambia las unidades de origen y destino:
        - Conserva exactamente el texto escrito en Valor.
        - Borra el resultado anterior (vuelve a '—').
        - No convierte automáticamente.
        """
        origen_actual = self.var_origen.get()
        destino_actual = self.var_destino.get()
        nuevo_origen, nuevo_destino = intercambiar_unidades(origen_actual, destino_actual)

        self.var_origen.set(nuevo_origen)
        self.var_destino.set(nuevo_destino)

        # Borra el resultado anterior y vuelve a '—'
        self.mostrar_placeholder_resultado()
        self.ocultar_error()

    # ---------------- ACCIÓN LIMPIAR ----------------

    def accion_limpiar(self):
        """
        Restaura la aplicación a su estado inicial:
        1. Borra el número introducido.
        2. Elimina el resultado de la conversión.
        3. Elimina mensajes de validación y error.
        4. Restaura selectores a valores por defecto (Metros -> Centímetros).
        5. Devuelve el foco a la entrada.
        """
        self.entry_valor.delete(0, "end")
        self.ocultar_error()
        self.mostrar_placeholder_resultado()
        self.var_origen.set("Metros (m)")
        self.var_destino.set("Centímetros (cm)")
        self.entry_valor.focus()


def main():
    app = ConversorApp()
    app.mainloop()


if __name__ == "__main__":
    main()

