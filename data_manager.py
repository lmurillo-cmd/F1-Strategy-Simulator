import pandas as pd
import os

def crear_entorno():
    # 1. Confirmación de la Carpeta de Salida
    if not os.path.exists('outputs'):
        os.makedirs('outputs') #Crea la carpeta
        print("📁 Carpeta 'outputs' creada correctamente (Aquí se guardarán tus gráficas).")
    else:
        print("📁 Carpeta 'outputs' detectada y lista.")

    # 2. Confirmación de los Datos (CSV)
    data = {
        'Circuito': ['Bahrain', 'Monaco', 'Silverstone', 'Spa', 'Monza', 'Interlagos','Jeddah','Melbourne','Suzuka',
              'Miami','Barcelona','Montreal','Hungaroring','Zandvoort', 'Baku', 'Austin', 'México', 'Las Vegas',
              'Abu Dhabi', 'Shanghai', 'Austria', 'Singapore', 'Qatar'],

        'Longitud_km': [5.412, 3.337, 5.891, 7.004, 5.793, 4.309, 6.174, 5.278, 5.807,
                    5.412, 4.657, 4.361, 4.381, 4.259, 6.003, 5.513, 4.304, 6.201,
                    5.281, 5.451, 4.318, 4.940, 5.419],

        'Vueltas': [57, 78, 52, 44, 53, 71, 50, 58, 53, 57, 66, 70, 70, 72, 51, 56, 71,
                50, 58, 56, 71, 62, 57],

        'Degradacion_Base': [0.15, 0.05, 0.18, 0.14, 0.10, 0.12, 0.09, 0.11, 0.17, 0.13, 0.19, 0.10,
                         0.16, 0.14, 0.08, 0.15, 0.09, 0.07, 0.11, 0.16, 0.10, 0.13, 0.18],

        'Pit_Loss_s': [23, 25, 23, 22, 24, 21, 20, 21, 22, 24, 22, 20, 21, 20, 24, 22, 22, 26, 23, 23, 20, 28, 24],

        'Prob_Lluvia': [0.05, 0.20, 0.40, 0.60, 0.15, 0.50, 0.02, 0.25, 0.45, 0.30, 0.15, 0.55, 0.20,
                    0.40, 0.05, 0.20, 0.25, 0.05, 0.02, 0.30, 0.35, 0.40, 0.01]
    }
    #Lo guardamos en el CSV
    pd.DataFrame(data).to_csv('pistas_f1.csv', index=False)

    print("✅ Archivo 'pistas_f1.csv' generado con exito.")
    print("🚀 Entorno configurado: ¡Todo listo para simular!")

def cargar_pistas():
   if not os.path.exists('pistas_f1.csv'):
    crear_entorno()
   else:
    print(" ✅ Base de datos cargada correctamente")

   return pd.read_csv('pistas_f1.csv')





