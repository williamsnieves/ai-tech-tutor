# Generador de Datos Sintéticos con LLMs

Este proyecto implementa un generador de datos sintéticos utilizando diferentes modelos de lenguaje (LLMs) como GPT, Claude, Llama, Phi-3 y Gemma. Permite generar datos realistas en varios formatos (JSON, CSV, Parquet) para diferentes dominios como negocios, salud, e-commerce y NLP.

## Características

- 🎯 Generación de datos sintéticos realistas
- 🤖 Soporte para múltiples modelos de LLM:
  - OpenAI GPT
  - Anthropic Claude
  - Meta Llama
  - Microsoft Phi-3
  - Google Gemma
- 📊 Formatos de salida:
  - JSON
  - CSV
  - Parquet
- 🏗️ Tipos de datos soportados:
  - Datos de negocios
  - Datos de salud
  - Datos de e-commerce
  - Datos de NLP
- 🎨 Interfaz gráfica intuitiva con Gradio

## Estructura del Proyecto

```
synthetic_data/
├── api/                 # Clientes de API para diferentes LLMs
├── config/             # Configuración y constantes
├── core/               # Lógica principal del generador
├── ui/                 # Interfaz de usuario con Gradio
├── utils/              # Utilidades y funciones auxiliares
├── main.py            # Punto de entrada de la aplicación
├── requirements.txt   # Dependencias del proyecto
└── README.md          # Documentación
```

## Requisitos

- Python 3.8+
- Dependencias listadas en `requirements.txt`

## Instalación

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
cd synthetic_data
```

2. Crear y activar un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso

1. Iniciar la aplicación:
```bash
python main.py
```

2. Acceder a la interfaz web:
- La aplicación estará disponible en `http://localhost:7860`
- Seleccionar el tipo de datos a generar
- Elegir el modelo de LLM
- Configurar el número de muestras y tokens
- Seleccionar el formato de salida
- Hacer clic en "Generate Data"

## Configuración

El archivo `config/settings.py` contiene las configuraciones principales:
- Modelos disponibles
- Tipos de datos soportados
- Formatos de salida
- Valores por defecto

## Contribución

Las contribuciones son bienvenidas. Por favor, sigue estos pasos:
1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles. 