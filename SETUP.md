# 🚀 Configuración Automática del Proyecto

## 📋 **Configuración Inicial (Solo Primera Vez)**

### **Opción 1: Automática (Recomendada)**
```bash
# Ejecutar migraciones (crea categorías automáticamente)
python manage.py migrate

# El sistema estará listo para usar
python manage.py runserver
```

### **Opción 2: Manual (Si quieres personalizar)**
```bash
# Configurar categorías y usuario de ejemplo
python manage.py setup_categories

# Con opciones adicionales
python manage.py setup_categories --force
```

### **Opción 3: Solo Categorías (Sin usuario de ejemplo)**
```bash
# Las categorías se crean automáticamente en la primera migración
python manage.py migrate
```

## 🎯 **¿Qué Se Crea Automáticamente?**

### **📦 Categorías por Defecto (10)**
- **Electrónica** - Productos electrónicos y tecnológicos
- **Ropa** - Vestimenta y accesorios
- **Hogar** - Artículos para el hogar y decoración
- **Deportes** - Equipamiento y ropa deportiva
- **Libros** - Libros, revistas y material educativo
- **Juguetes** - Juguetes y entretenimiento
- **Automóviles** - Partes y accesorios para vehículos
- **Jardín** - Productos para jardín y exteriores
- **Salud y Belleza** - Productos de cuidado personal
- **Mascotas** - Productos para mascotas y animales

### **👤 Usuario de Ejemplo (Opcional)**
- **Username**: `usuario_ejemplo`
- **Password**: `password123`
- **Email**: `ejemplo@test.com`

## 🔧 **Comandos Disponibles**

### **`python manage.py setup_categories`**
- ✅ Crea categorías por defecto
- ✅ Crea usuario de ejemplo
- ✅ No sobrescribe datos existentes
- ✅ Muestra resumen detallado

### **`python manage.py setup_categories --force`**
- ✅ Crea categorías por defecto
- ✅ Actualiza descripciones existentes
- ✅ Crea usuario de ejemplo
- ✅ Sobrescribe datos existentes

### **`python manage.py migrate`**
- ✅ Ejecuta todas las migraciones
- ✅ Crea categorías automáticamente (primera vez)
- ✅ Configura la base de datos

## 🚫 **Ya NO Necesitas Ejecutar**

- ❌ `python create_initial_data.py` (obsoleto)
- ❌ Crear categorías manualmente
- ❌ Configurar la base de datos paso a paso

## 🎉 **Ventajas del Nuevo Sistema**

1. **🔄 Automático**: Las categorías se crean solas
2. **🛡️ Seguro**: No sobrescribe datos existentes
3. **⚡ Rápido**: Solo una migración necesaria
4. **🔧 Flexible**: Comandos opcionales disponibles
5. **📱 Fácil**: Instrucciones claras y simples

## 🚨 **Solución de Problemas**

### **Si las categorías no aparecen:**
```bash
# Verificar migraciones
python manage.py showmigrations

# Ejecutar migraciones pendientes
python manage.py migrate

# Forzar configuración
python manage.py setup_categories --force
```

### **Si hay errores:**
```bash
# Verificar estado del sistema
python manage.py check

# Recrear base de datos (¡CUIDADO! Borra todo)
python manage.py flush
python manage.py migrate
```

## 📚 **Más Información**

- **Documentación Django**: https://docs.djangoproject.com/
- **Signals Django**: https://docs.djangoproject.com/en/5.2/topics/signals/
- **Comandos Personalizados**: https://docs.djangoproject.com/en/5.2/howto/custom-management-commands/

---

**¡Tu proyecto ahora se configura automáticamente! 🎉**
