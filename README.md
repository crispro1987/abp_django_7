# Django Wallet 
## Proyecto Módulo #7 | ABP

billetera digital (Alke Wallet) que permite a los usuarios gestionar y administrar sus activos financieros de forma segura y sencilla.

## Tecnologías utilizadas

- Python        3.14
- asgiref       3.11.1
- Django        6.0.2
- mysqlclient   2.2.8
- pip           26.0.1
- sqlparse      0.5.5
- tzdata        2025.3
- Github

## Configuración Base de datos

Base de datos SQLite para desarrollo y MySQL para producción

```
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE':'django.db.backends.mysql',
            'NAME': 'wallet_7',
            'USER': 'root',
            'PASSWORD': '*******',
            'HOST': '127.0.0.1',
            'PORT': '3306',
        }
    }
```

## Modelos

Creación de modelos Cliente, Cuenta y Transaccion 

```
class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cliente')
    phone = models.CharField("Teléfono",max_length=20, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

...

```

## Migraciones

Utilización de comandos para aplicar cambios en modelos.

```
python manage.py makemigrations

python manage.py migrate
```

## CRUD

Create - Read - Update - Delete

```
# Create
def cuenta_create(request):

# Read
def cuenta_list(request):

# Update
def cuenta_update(request, pk):

# Delete
def cuenta_delete(request,pk):
```

