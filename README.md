# C&C Asociados Oriente S.A.S — Sitio web

Página web corporativa construida con **Python + Flask**, diseñada con un
lenguaje visual industrial-moderno apropiado para una empresa de transporte
de carga, logística de personal y obras civiles.

---

## Estructura

```
cyc_web/
├── app.py                    # Aplicación Flask + datos centralizados
├── requirements.txt
├── static/
│   ├── css/style.css         # Sistema de diseño completo
│   ├── js/main.js            # Animaciones, contadores, formulario
│   └── img/                  # Imágenes (camión, buldócer, etc.)
└── templates/
    ├── base.html             # Plantilla maestra
    └── index.html            # Página única (one-pager)
```

## Cómo correrlo

```bash
# 1. Crear entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate     # Linux/Mac
# venv\Scripts\activate      # Windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Lanzar
python app.py
```

Abrir <http://localhost:5000> en el navegador.

## Decisiones de diseño

- **Paleta**: asfalto (`#0D0D0F`) + naranja marca (`#F26419`) + hueso cálido
  (`#F4F1EA`). Sin la habitual paleta SaaS azul-violeta.
- **Tipografía**: *Archivo Black* (display industrial condensado) +
  *Inter* (cuerpo) + *JetBrains Mono* (datos/odómetro).
- **Elemento firma**: cinta de hazard (señalética amarillo/negro)
  animada bajo el hero, líneas de carretera moviéndose, contador
  estilo odómetro al entrar al viewport.
- **Estructura**: numeración `[ 01 ] / [ 02 ]` como pestañas de bitácora
  operativa, no como decoración.

## Endpoint disponible

| Método | Ruta             | Descripción                          |
| ------ | ---------------- | ------------------------------------ |
| GET    | `/`              | Página única                         |
| POST   | `/api/cotizar`   | Recibe formulario (JSON o form-data) |

El endpoint de cotización valida los campos `nombre`, `empresa`,
`contacto` y `servicio`, y devuelve un radicado. Para integrarlo a
correo o CRM, modifique la función `cotizar()` en `app.py`.

## Personalización rápida

Los textos del sitio están centralizados en `app.py` (constantes
`EMPRESA`, `SERVICIOS`, `VENTAJAS`, `POLITICAS`, `FLOTA`,
`CERTIFICACIONES`). Cambiar cualquiera de estos diccionarios actualiza
la página automáticamente.

Para sumar un servicio, agregue una entrada a la lista `SERVICIOS`:

```python
{
    "codigo": "07",
    "titulo": "Nuevo servicio",
    "descripcion": "…",
    "tags": ["…"],
},
```

## Próximos pasos sugeridos

- Conectar el endpoint `/api/cotizar` a un envío de correo
  (Flask-Mail) o a Google Sheets para registro de leads.
- Agregar Open Graph / Twitter Cards y favicon definitivo.
- Configurar `gunicorn` + `nginx` para despliegue en producción.
