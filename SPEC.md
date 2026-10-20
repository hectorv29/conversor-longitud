# SPEC.md - Especificación del Conversor de Longitud (mm, cm, m)

> **Leyenda de trazabilidad:**
> - `[Usuario]`: Requisito, restricción o directiva explícita indicada por el usuario.
> - `[Propuesta Aprobada]`: Decisión técnica acordada para resolver aspectos de implementación sin añadir funciones extra.

---

## 1. Objetivo
Desarrollar una aplicación funcional de escritorio en Python para convertir unidades de longitud entre milímetros (mm), centímetros (cm) y metros (m), con una interfaz visual moderna, pulida y profesional (no genérica), validación estricta de entrada en tiempo real y precisión matemática exacta sin imprecisiones de coma flotante `[Usuario]`.

---

## 2. Usuario
- **Perfil:** Cualquier usuario que requiera realizar conversiones de longitud entre mm, cm y m en entorno de escritorio `[Usuario]`.
- **Modo de interacción:** Teclado y ratón/puntero `[Usuario]`.

---

## 3. Interfaz
- **Composición:** Panel/tarjeta principal centrada, equilibrada, con jerarquía visual clara, bordes redondeados y sombras sutiles `[Usuario]`.
- **Encabezado:** Título «Conversor de longitud» y breve descripción explicativa `[Usuario]`.
- **Campo numérico:** Amplio, fácil de usar, con tipografía legible `[Usuario]`.
- **Selectores de unidades:**
  - Selector de unidad de origen: milímetros (mm), centímetros (cm), metros (m) `[Usuario]`.
  - Selector de unidad de destino: milímetros (mm), centímetros (cm), metros (m) `[Usuario]`.
  - Indicaciones visibles con sus símbolos oficiales (`mm`, `cm`, `m`) `[Usuario]`.
  - Valores predeterminados al inicio: Origen en `Metros (m)` y Destino en `Centímetros (cm)` `[Propuesta Aprobada]`.
- **Botones de acción:**
  - Botón principal «Convertir», visualmente destacado `[Usuario]`.
  - Botón secundario «Limpiar», fácilmente identificable `[Usuario]`.
- **Zona de resultado:**
  - Área visualmente diferenciada del resto de campos `[Usuario]`.
  - Muestra valor original, unidad de origen, resultado y unidad de destino (ejemplo: `2,5 m = 250 cm`) `[Usuario]`.
  - Formato decimal con coma (`,`) en la presentación final `[Usuario]`.
- **Mensajes de validación:** Discretos, legibles, integrados en la interfaz (sin alertas emergentes tipo popup ni modales) `[Usuario]`. Con reserva espacial fija para no desplazar bruscamente la interfaz `[Usuario]`.
- **Accesibilidad y usabilidad:** Contraste adecuado texto/fondo, estados hover/focus en botones, navegación y uso completo mediante teclado, diseño adaptable a diferentes tamaños de pantalla `[Usuario]`.

---

## 4. Requisitos del Sistema

### Funcionales
- **R1 - Selección de unidades:** El sistema debe permitir seleccionar la unidad de origen y destino entre mm, cm y m `[Usuario]`.
- **R2 - Ejecución manual de cálculo:** La conversión solo debe calcularse al pulsar el botón «Convertir». No debe calcularse automáticamente al escribir o cambiar unidades `[Usuario]`.
- **R3 - Persistencia de resultado hasta nueva acción:** Si tras convertir se modifican campos o unidades, el resultado anterior no se actualiza hasta volver a pulsar «Convertir» `[Usuario]`.
- **R4 - Operación de limpieza:** Al pulsar «Limpiar», el sistema debe:
  1. Borrar el valor numérico introducido `[Usuario]`.
  2. Eliminar el resultado visualizado `[Usuario]`.
  3. Eliminar cualquier mensaje de error o validación `[Usuario]`.
  4. Restaurar selectores a sus valores predeterminados (Origen: `Metros (m)`, Destino: `Centímetros (cm)`) `[Usuario]` `[Propuesta Aprobada]`.
  5. Devolver la interfaz a su estado inicial, funcionando incluso con campos vacíos o con error activo `[Usuario]`.
- **R5 - Precisión matemática:** Aplicar equivalencias exactas:
  - $1\text{ m} = 100\text{ cm} = 1000\text{ mm}$ `[Usuario]`.
  - $1\text{ cm} = 10\text{ mm}$ `[Usuario]`.
  - Origen y destino iguales deben devolver exactamente el mismo valor introducido `[Usuario]`.
  - Cero (`0`) y números negativos deben admitirse y convertirse correctamente `[Usuario]`.
  - Evitar imprecisiones binarias de coma flotante utilizando `decimal.Decimal` `[Usuario]` `[Propuesta Aprobada]`.

### Validación de Entrada
- **R6 - Bloqueo de caracteres en tiempo real:** El campo numérico debe impedir físicamente la entrada de letras o símbolos no permitidos en el momento de la pulsación `[Usuario]`.
  - Permitido exclusivamente: dígitos `0-9`, un único signo negativo `-` al inicio, y un único separador decimal (coma `,` o punto `.`) `[Usuario]`.
  - Bloqueo de múltiples separadores (`3,4,5`, `2.3.4`) o signos negativos intermedios/duplicados (`5-2`, `--5`) `[Usuario]`.
  - Permitir edición normal (borrado con backspace/supr, selección total/parcial, inserción inicial de signo) `[Usuario]`.
- **R7 - Control estricto de portapapeles (Pegar):** Interceptar el pegado para impedir que se introduzcan caracteres no válidos `[Usuario]`.
- **R8 - Interpretación unificada de decimales:** El sistema debe interpretar tanto coma como punto, normalizando la coma a punto antes del cálculo `[Usuario]`.
- **R9 - Validación previa al cálculo:** Al pulsar «Convertir»:
  - Si el campo está vacío: mostrar mensaje integrado «Introduce un valor para realizar la conversión» `[Usuario]`.
  - Si el valor no es interpretable (ej. solo `-`, solo `.` o `,`): mostrar mensaje de error comprensible `[Usuario]`.

---

## 5. Criterios de Aceptación

- **A1:** Al teclear letras (`a`, `b`, etc.) o caracteres no numéricos, estos no aparecen en el campo de entrada.
- **A2:** Al pegar desde el portapapeles un texto con letras o estructura numérica errónea, la inserción es bloqueada.
- **A3:** Admite entradas válidas como `25`, `2,5`, `2.5`, `-10`, `-2,75`, `-0.5`, `0`.
- **A4:** Si el campo está vacío y se pulsa «Convertir», se muestra el mensaje integrado «Introduce un valor para realizar la conversión», sin diálogos modales.
- **A5:** Las siguientes conversiones de comprobación devuelven exactamente:
  - `1 m` → `100 cm`
  - `1 m` → `1000 mm`
  - `1 cm` → `10 mm`
  - `250 mm` → `25 cm`
  - `150 cm` → `1,5 m`
  - `-2,5 m` → `-250 cm`
- **A6:** Si origen y destino coinciden (ej. `2,5 m` a `m`), el resultado mostrado es exactamente `2,5 m`.
- **A7:** El resultado se muestra en la zona destacada con el formato: `[valor_orig] [u_orig] = [valor_dest] [u_dest]`, usando la coma decimal en la presentación.
- **A8:** Modificar el número o cambiar las unidades después de una conversión no altera el resultado previo hasta pulsar «Convertir» nuevamente.
- **A9:** Al pulsar «Limpiar», se borra la entrada, el resultado, los errores y las unidades vuelven a `Metros (m)` y `Centímetros (cm)`.
- **A10:** La aplicación se ejecuta en Python utilizando `customtkinter` y sin errores de consola.

---

## 6. Fuera de Alcance
- Otras magnitudes físicas (peso, volumen, temperatura, etc.) `[Usuario]`.
- Otras unidades de longitud ajenas a mm, cm y m `[Usuario]`.
- Conversión automática en tiempo real mientras se escribe `[Usuario]`.
- Cuadros de diálogo emergentes del sistema operativo `[Usuario]`.
- Conexión a bases de datos o servicios remotos `[Usuario]`.
- Funciones accesorias no solicitadas (historiales de conversión, conversión masiva, favoritos) `[Usuario]`.

---

## 7. Decisiones Técnicas Acordadas
- **Librería gráfica:** `customtkinter` en Python (garantiza la interfaz comercial moderna, tarjetas con bordes redondeados y soporte de temas) `[Propuesta Aprobada]`.
- **Motor de cálculo:** Módulo estándar `decimal.Decimal` de Python `[Propuesta Aprobada]`.
- **Valores predeterminados:** Origen = `Metros (m)`, Destino = `Centímetros (cm)` `[Propuesta Aprobada]`.
- **Atajos de teclado:** `Enter` para Convertir, `Escape` para Limpiar `[Propuesta Aprobada]`.

---

## 8. Dudas
*(No quedan dudas ni decisiones bloqueantes pendientes)*.

