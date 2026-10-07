# AsyncLCELRefactor

Ejemplo mínimo de una cadena **LCEL** (LangChain Expression Language) encadenada y ejecutada de forma **asíncrona** con `ainvoke`, usando modelos de OpenAI.

## Qué hace

El script [`LCELRef.py`](LCELRef.py) arma dos cadenas y las conecta:

1. **`tech`**: le pide al modelo, actuando como experto en un `topic` (por defecto, `biotecnología`), que responda **solo con el nombre** de la tecnología que considera más innovadora.
2. **`advice`**: toma ese nombre como `subtopic` y le pide al modelo que explique sus beneficios en 3 puntos.

Ambas se componen con el operador `|`:

```
{"topic"} → tech (prompt | model | parser)
          → lambda nombre: {"subtopic": nombre}
          → advice (prompt) → model → parser
          → texto final
```

La `lambda` intermedia adapta la salida de texto de la primera cadena al diccionario de entrada que espera el segundo prompt. LangChain la convierte automáticamente en un `RunnableLambda`.

La ejecución se hace con `await tech_chain.ainvoke(...)` dentro de `asyncio.run(main())`, lo que permite integrar la cadena en aplicaciones asíncronas sin bloquear el event loop.

## Requisitos

- Python 3.9 o superior
- Una API key de OpenAI

## Instalación

```bash
git clone <url-del-repo>
cd AsyncLCELRefactor
python -m venv .venv
source .venv/bin/activate   # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Configuración

Copiá el archivo de ejemplo y completá tus valores:

```bash
cp .env.example .env
```

| Variable         | Obligatoria | Default  | Descripción                     |
|------------------|-------------|----------|---------------------------------|
| `OPENAI_API_KEY` | Sí          | —        | Tu API key de OpenAI            |
| `OPENAI_MODEL`   | No          | `gpt-4o` | Modelo de chat a utilizar       |

Las variables se cargan con `python-dotenv`; si ya están definidas en el entorno del sistema, tienen prioridad sobre el `.env`. El archivo `.env` **no** debe subirse al repositorio.

## Uso

```bash
python LCELRef.py
```

Se imprime en consola la explicación de los beneficios de la tecnología elegida por el modelo. Para cambiar el tema, modificá el valor de `topic` en la función `main()`:

```python
resultado = await tech_chain.ainvoke({"topic": "energías renovables"})
```

## Estructura

```
.
├── LCELRef.py        # Script principal con las cadenas LCEL
├── requirements.txt  # Dependencias
├── .env.example      # Plantilla de variables de entorno
└── README.md
```

## Notas

- Se usa `temperature=0` para obtener respuestas lo más deterministas posible.
- Si falta `OPENAI_API_KEY`, el script corta con un `RuntimeError` explicativo antes de llamar a la API.
