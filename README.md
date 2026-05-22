# F1-Strategy-Simulator
Simulador avanzado de estrategias de carrera
El programa modela aspectos críticos como la degradación de compuestos (Blando, Medios y Duros), ventanas de parada en boxes, dinámicas de carrera con condiciones climáticas variables como lluvia e incidentes en pista (Safety car).

##Requisitos e intalación
Para ejecutar el programa en Visual Studio Code, es necesario tener instaladas las siguientes librerias en Phyton:
* Pandas
* os
* numpy
* matplotlib

##Estructura y archivos del proyecto
El software del proyecto se diseño mediante modulos .py
*main.py: Es el modulo principal, contrala el flujo del menú y conecta todos los componentes de la simulación.
*data_manager.py: Es el módulo encargado de verificar el entrono del sistema, generar por defecto y cargar el archivo con los datos de los circuitos udando *DataFrames* de Pandas.
*simulator.py: Es el módulo que contiene las formulas matemáticas (calculos de degradación), el control de la radio por vueltas, y toma las decisiones estratégicas.
*visualizer.py: Es el módulo que diseña y genera los gráficos con matplotlib basado en los datos procesados, y los guarda en la carpeta 'outputs'.

##Ejecución del software (VS Code)
1. Descargue y descomprima el archivo '.zip' que contine los 4 archivos:
   (main.py, data_manager.py, simulator.py y visualizer.py)
2. Abra la carpeta en VS code.
3. Ejecute el archivo main.py. Al iniciarlo, se creará automaticamente la carpeta 'outputs' y la base de datos 'pistas_f1.csv' si no es detectada en el disco.
4. El programa a continuación le solicitara el nombre del piloto, la escuderia, el circuito donde se hará la simulación y la posición de salida. Durante el desarrollo de la carrera, el menú cíclico simulara alertas o radios del ingeniero de carrera por, lluvia, daños en el ala y estrategias de entrada a boxes.
5. Al finalizar la simulación, el programa imprimirá en la consola un reporte final y guardara las gráficas de los resultados en la carpeta 'outputs'.
