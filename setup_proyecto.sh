#!/bin/bash

echo "📁 Creando estructura de carpetas para el proyecto de métodos numéricos..."

# Nombre raíz del proyecto
PROYECTO="metodos_numericos"
mkdir -p $PROYECTO/{gui,core,data,benchmark,doc}

# Crear archivos base para cada unidad
touch $PROYECTO/gui/{main_interface.py,unidad1_gui.py,unidad2_gui.py,unidad3_gui.py}
touch $PROYECTO/core/{newton_raphson.py,minimos_cuadrados.py,rk4_motor.py,utils.py}
touch $PROYECTO/benchmark/{benchmark_unidad1.py,benchmark_unidad2.py,benchmark_unidad3.py}
touch $PROYECTO/doc/{README.md,bitacora.md}
touch $PROYECTO/data/.gitkeep
touch $PROYECTO/cli/{cli_newton.py,cli_minimos_cuadrados.py,cli_rk4_motor.py}

# Crear archivo de dependencias
cat > $PROYECTO/requirements.txt <<EOL
numpy
scipy
matplotlib
pandas
PySimpleGUI
scikit-learn
opencv-python
EOL

# Crear entorno virtual
cd $PROYECTO
pip install -r requirements.txt

echo "✅ Proyecto '$PROYECTO' creado con éxito y entorno virtual activado."
echo "🚀 Ya puedes comenzar con la codificación desde gui/main_interface.py"