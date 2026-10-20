# Conversor de Unidades de Longitud (mm, cm, m)

Aplicación de escritorio moderna, robusta y con acabado profesional para la conversión de unidades de longitud entre **milímetros (mm)**, **centímetros (cm)** y **metros (m)**.

---

## 🚀 Cómo ejecutar la aplicación

### Opción 1: Doble clic en Windows
Haz doble clic sobre el archivo `ejecutar.bat` en esta carpeta.

### Opción 2: Desde la terminal o consola de comandos
1. Abre PowerShell o el Símbolo del Sistema en esta carpeta.
2. Asegúrate de tener instalada la dependencia (solo requiere `customtkinter`):
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecuta el programa con Python:
   ```bash
   python Conversor.py
   ```

---

## ✨ Características y Requisitos Implementados

### 1. Validación Estricta en Tiempo Real (Bloqueo en el teclado)
- El campo de entrada numérico **impide físicamente escribir cualquier carácter no permitido**: letras (`abc`, `12a`), signos repetidos (`--5`), múltiples separadores (`3,4,5` o `2.3.4`) o símbolos fuera de lugar (`5-2`).
- Permite exclusivamente:
  - Dígitos del `0` al `9`.
  - El signo negativo (`-`), **únicamente en la primera posición**.
  - Un único separador decimal, aceptando indistintamente **coma (`,`)** o **punto (`.`)**.
- **Control de portapapeles**: Se intercepta la acción de pegar (`Ctrl+V`, `Shift+Insert`, clic derecho -> Pegar) para impedir que se pegue texto con letras o caracteres no válidos. Si el portapapeles contiene texto con espacios en los extremos, se limpian automáticamente; si contiene letras, la operación se cancela y se muestra un aviso integrado.

### 2. Precisión Numérica Absoluta (Módulo `decimal.Decimal`)
- Se evita por completo el error de redondeo de coma flotante binaria (`float`).
- Relaciones exactas:
  - $1\text{ m} = 100\text{ cm} = 1000\text{ mm}$
  - $1\text{ cm} = 10\text{ mm}$
- Formateo de presentación adaptado al estándar español (coma decimal) sin ceros innecesarios a la derecha:
  - Ejemplo: `2,5 m = 250 cm`
  - Ejemplo: `150 cm = 1,5 m`
  - Ejemplo: `-2,5 m = -250 cm`

### 3. Interfaz Moderna y Comercial (CustomTkinter)
- **Tarjeta principal** con esquinas redondeadas, bordes sutiles y elevación visual.
- **Selectores de unidades claros** (`Metros (m)`, `Centímetros (cm)`, `Milímetros (mm)`).
- **Botón de intercambio rápido (`⇄`)**: Invierte las unidades de origen y destino con un solo clic.
- **Botón «Convertir ↵»** con color de acento destacado.
- **Botón «Limpiar ⟲»** que restablece todo el estado (campo de entrada, resultado, mensajes de error y selectores por defecto a *Metros* y *Centímetros*).
- **Área de resultado diferenciada**: Muestra el valor en grande, la ecuación completa (`2,5 m = 250 cm`), la equivalencia y un botón **📋 Copiar** al portapapeles.
- **Alternador de Tema (Modo Oscuro / Modo Claro)**: Permite alternar la estética con el botón `☀️ Claro / 🌙 Oscuro`.
- **Chips de pruebas rápidas**: 6 accesos directos con los casos del enunciado para comprobar el funcionamiento al instante.
- **Atajos de teclado**:
  - `Enter` o `Intro`: Ejecuta la conversión.
  - `Escape`: Limpia la interfaz y restaura el estado inicial.
  - `Ctrl + I`: Invierte las unidades.

