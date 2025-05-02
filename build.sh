#!/bin/bash

APP_NAME="PomodoroApp"
MAIN_FILE="app.py"
DMG_NAME="$APP_NAME.dmg"
APP_DIST_PATH="dist/$APP_NAME.app"
ALARMSOUND_PATH="alarma.mp3"  # Ruta al archivo de sonido

echo "🧹 Limpiando builds anteriores..."
rm -rf dist build __pycache__ *.spec "$DMG_NAME"

echo "⚙️ Compilando la app con PyInstaller..."
pyinstaller --noconfirm --windowed --name "$APP_NAME" "$MAIN_FILE"

# Asegurar que la app fue generada
if [ ! -d "$APP_DIST_PATH" ]; then
  echo "❌ No se encontró $APP_DIST_PATH. Algo falló con PyInstaller."
  exit 1
fi

echo "🗑️ Eliminando datos sensibles..."
rm -f "dist/sesiones.json"

echo "📁 Preparando carpeta temporal..."
mkdir -p dmg_temp
cp -R "$APP_DIST_PATH" dmg_temp/

# Crear un enlace simbólico a la carpeta Applications
ln -s /Applications dmg_temp/Applications

echo "💿 Creando el .dmg con solo la app..."
create-dmg \
  --volname "$APP_NAME" \
  --window-size 500 300 \
  --icon "$APP_NAME.app" 100 100 \
  --icon "Applications" 350 100 \
  "$DMG_NAME" dmg_temp/

echo "🧼 Limpiando carpeta temporal..."
rm -rf dmg_temp

echo "✅ ¡Listo! '$DMG_NAME' contiene solo la app compilada, sin datos del proyecto."