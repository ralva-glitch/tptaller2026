# StreamAI: Recomendador de Contenido de Streaming
## Descripción del proyecto
StreamAI es una aplicación web desarrollada con el objetivo de analizar tendencias de contenido audiovisual en distintas plataformas de streaming y brindar recomendaciones personalizadas de películas y series mediante técnicas de análisis de datos y procesamiento de texto.
La plataforma integra información proveniente de Netflix, Disney+, Prime Video, HBO Max, Apple TV+. 
A partir de estos datos se desarrolló un dashboard interactivo y un motor de recomendación basado en similitud de contenido.
## Contenido
## Estructura del proyecto
```text
tp-con-sorpreas/
│
├── index.html                # Página principal
├── app.js                    # Lógica del dashboard y recomendaciones
├── dataset_embed.js          # Dataset embebido (800 títulos)
├── requirements.txt          # Dependencias de Python
├── README.md
├── LICENSE
│
├── docs/
│   ├── Stream IA - Pagina.pptx
│   └── Proyecto Stream IA (con n8n).pptx
│
├── n8n/
│   ├── chatbot-sorprendeme(n8n).json
│   └── comparador(n8n).json
│
└── preprocessing/
    ├── preprocessing_streamai.ipynb   # Notebook con el proceso real de unificación
    └── normalize_dataset.py           # Normaliza genero/pais (Drama/Dramas/drama, US/United States, etc.)
```
## Arquitectura del proyecto
Datasets Kaggle
        ↓
Limpieza y unificación (Python / Google Colab)
        ↓
Dataset final
        ↓
Dashboard Web (HTML + JS + Chart.js)
        ↓
Motor de recomendación (TF-IDF)
        ↓
Chatbot OpenAI + n8n
## Objetivos
### Objetivo general
Desarrollar una plataforma web que permita analizar el contenido disponible en múltiples servicios de streaming y recomendar títulos según las preferencias del usuario.
### Objetivos específicos
Integrar datasets de distintas plataformas.
Analizar géneros, popularidad y tendencias de consumo.
Construir indicadores y visualizaciones interactivas.
Implementar un sistema de recomendación basado en IA.
Integrar un chatbot mediante n8n y OpenAI.
## Demo del proyecto
🌐 Página Web:
https://seregrun-ops.github.io/tp-con-sorpreas/
Repositorio:
https://github.com/Seregrun-ops/tp-con-sorpreas
## Dataset
El archivo `dataset_embed.js` contiene una muestra de 800 títulos, obtenida
mediante un proceso real de unificación de los 5 datasets de Kaggle listados
abajo. El proceso completo está documentado en
`preprocessing/preprocessing_streamai.ipynb`, y consiste en:

1. Descarga de los 5 datasets desde Kaggle (API oficial).
2. Normalización de columnas: cada plataforma trae un esquema distinto
   (Netflix/Prime Video vs. Disney+/Apple TV+/HBO Max), por lo que se
   mapean todas a un esquema común.
3. Concatenación de las 5 plataformas en un único dataset de 23.529 títulos
   (`data/streaming_dataset_full.csv`).
4. Muestreo proporcional de 800 títulos (`data/streaming_dataset_sample.csv`),
   respetando el tamaño real de catálogo de cada plataforma.

Columnas: `show_id`, `titulo`, `tipo`, `plataforma`, `director`, `elenco`,
`pais`, `fecha_agregado`, `anio_lanzamiento`, `clasificacion`, `duracion`,
`genero`, `descripcion`, `puntaje`.

**Normalización aplicada (`preprocessing/normalize_dataset.py`):**
- `genero`: se unificaron 63 valores crudos (mezcla de mayúsculas/minúsculas,
  singular/plural y sinónimos entre plataformas, ej. `Drama`/`Dramas`/`drama`,
  `Horror`/`Horror Movies`) en 22 categorías canónicas.
- `pais`: se unificaron códigos ISO-2 (`US`, `GB`, `CA`, etc.) con su nombre
  completo correspondiente (`United States`, `United Kingdom`, `Canada`, etc.).

**Limitaciones conocidas del dataset real:**
- Netflix y Prime Video no incluyen puntaje de IMDb en su fuente original;
  esos títulos quedan con `puntaje` vacío (se muestra "N/D" en la web).
- Disney+, Apple TV+ y HBO Max no incluyen fecha de agregado al catálogo;
  se aproxima con el 1 de enero del año de estreno.
- Apple TV+ tiene un catálogo fuente mucho más chico (170 títulos) que el
  resto, por lo que está subrepresentado en la muestra proporcional (6 de 800).
Enlaces de Datasets:
https://www.kaggle.com/datasets/shivamb/netflix-show
https://www.kaggle.com/datasets/unanimad/disney-plus-shows
https://www.kaggle.com/datasets/shivamb/amazon-prime-movies-and-tv-shows
https://www.kaggle.com/datasets/dgoenrique/apple-tv-movies-and-tv-shows
https://www.kaggle.com/datasets/ruchi798/movies-on-netflix-prime-video-hulu-and-disney
