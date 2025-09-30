# Setup Instructions - E-Commerce Platform with AI-Generative Features

## Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

## Step 1: Clone and Setup Environment
```bash
git clone <Repository-url>
cd E-Commerce-con-IA-Generativa

# Create virtual environment
python -m venv env

# Activate virtual environment
# Windows:
env\Scripts\activate
# macOS/Linux:
source env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Database Setup
```bash
# Apply migrations (creates database tables and default categories automatically)
python manage.py migrate
```

**Note:** No need to run `makemigrations` - migrations are already created.
The `migrate` command will automatically create:
- All database tables
- Default product categories (Electrónica, Ropa, Hogar, etc.)
- Review system tables

## Step 3: Create Test Users (Required for Testing)
You need 2 users to test all features:

### User 1 (Seller):
- Go to: [http://localhost:8000/register/](http://localhost:8000/register/)
- Create account: `seller_user` / `password123`
- This user will create products

### User 2 (Buyer/Reviewer):
- Go to: [http://localhost:8000/register/](http://localhost:8000/register/)
- Create account: `buyer_user` / `password123`
- This user will review products

## Step 4: Run Development Server
```bash
python manage.py runserver
```

## Step 5: Access the Platform
- Main Site: [http://localhost:8000](http://localhost:8000)
- Admin Panel: [http://localhost:8000/admin](http://localhost:8000/admin)

## Step 6: Test the Features
1. Login as seller_user → Create a product (status: "Published")
2. Logout → Login as buyer_user → Go to product detail → Leave a review
3. Check AI features at `/api/ai/` (health check and product analysis)

## Configuration Files
- No configuration files need to be modified
- Database: SQLite (default, no setup required)
- AI Provider: Gemma (default, configurable via `settings.AI_PROVIDER`)

## Troubleshooting
```bash
# If categories don't appear:
python manage.py migrate

# If you need to reset everything:
python manage.py flush
python manage.py migrate
```
# Desplegar servidor de la API
Para el uso de la funcionalidad de IA en este proyecto es necesario desplegar el modelo Gemma para análisis de imágenes(solo en caso de que quieras usar la IA integrada en el proyecto).

1) Primero sería obtener los acces tokens del modelo de Gemma en este link y obtener acceso al modelo: [Gemma-3-4b-it](https://huggingface.co/google/gemma-3-4b-it)

![accesHuggingFace](/readmeAssets/acceshug.png)

1) Por medio de este link puedes clonar el despliegue del modelo para que sea más facil: [TutorialLink](https://lightning.ai/sitammeur/studios/deploy-gemma-3-multimodal-multilingual-model?view=public&section=featured&query=multimoda)
- Buscas el botón `clone` 
  
![clone](/readmeAssets/clone.png)
- Te va a llevar a una página como esta 

![studio](/readmeAssets/studio.png)

- Reemplaza el código de client.py por este código [client.py](/readmeAssets/client.py) 
- Reemplaza el código de server.py por este código [server.py](/readmeAssets/server.py)
- Crea un `.env` con el acces tokend de hugginFace para hacer uso de Gemma model
- Luego crea el `API builder`
![searchBuilder](/readmeAssets/Build.png)
 Presionas 'Serving' donde debes seleccionar `API builder` e install 
![serving](/readmeAssets/serving.png)
Te va a aparecer un apartado con el api builder
![API_BUilder](/readmeAssets/api.png)
Luego vas y presionas `New API` y pones el puerto `8001` y `auto start` con el comando `python server.py` para poder iniciar el servidor
![conf1](/readmeAssets/conf1.png)

## Configurar el proyecto para usar tu propio servidor Lightning AI

Cuando usted haya desplegado el servidor de Lightning AI, necesitas actualizar la configuración del proyecto Django para que use tu endpoint:

### Paso 1: Obtener tu URL del servidor Lightning AI

Después de crear tu API Builder, obtendrás una URL única como:
- `https://8001-01k6bxyd24206n6bm11najcms8.cloudspaces.litng.ai` (ejemplo)

### Paso 2: Actualizar la configuración en Django

Edita el archivo `productplatform/settings.py` y busca la sección de configuración de IA:

```python
# Configuración de Lightning AI
LIGHTNING_AI_ENDPOINT = 'https://8001-01k6bxyd24206n6bm11najcms8.cloudspaces.litng.ai'  # Cambia la URL
LIGHTNING_AI_API_KEY = 'gemma3-litserve'  # Deja este valor
```

**Reemplaza la URL** `https://8001-01k6bxyd24206n6bm11najcms8.cloudspaces.litng.ai` por la URL que obtuviste del propio API Builder.


### Paso 3: Configuración manual (Alternativa)

Manualmente, actualiza el archivo `client.py`:

```python
client = OpenAI(
    base_url="https://8001-01k6bxyd24206n6bm11najcms8.cloudspaces.litng.ai/v1/",  # Cambia por tu URL
    api_key="gemma3-litserve",  # Mantén este valor
)
```

### Paso 4: Verificar la configuración

Para verificar que todo funciona correctamente:

1. **Asegúrate de que el servidor Lightning AI esté corriendo:**
   ```bash
   ⚡ ~ python server.py
   INFO:     Uvicorn running on http://0.0.0.0:8001
   ```

2. **Ejecuta el servidor Django:**
   ```bash
   python manage.py runserver
   ```

3. **Prueba la funcionalidad de IA** subiendo una imagen en `/product/create/`

### Nota importante sobre conectividad

Si experimenta errores de conexión (`ConnectionResetError`), el sistema automáticamente usará un servicio mock como fallback, asegurando que la aplicación siempre funcione. Esto es normal y esperado si ocurre algo.

## Features to Test
- User registration/login
- Product CRUD (Create, Read, Update, Delete)
- Product search and filtering
- Wishlist functionality
- Review system (ratings and comments)
- AI integration (product analysis)
- Admin panel access

## Architecture Patterns Implemented
- Dependency Inversion (AI providers)
- Strategy + Factory (AI client selection)
- Class-Based Views (CRUD operations)
- Custom QuerySet/Manager (product filtering)
- Observer (Django Signals for review averages)
- Strategy (review moderation)