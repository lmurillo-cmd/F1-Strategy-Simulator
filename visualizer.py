import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import os

def generar_grafica_rendimiento(tiempos, paradas, circuito, piloto, equipo, pos_salida):
    # 1. CONFIGURACIÓN DEL ESTILO (Dark Racing Theme)
    plt.style.use('dark_background')

    # Crear el lienzo con subplots (1 fila, 2 columnas)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8), facecolor='black')

    vueltas = list(range(1, len(tiempos) + 1))

    # -------------------------------------------------------------------------
    # --- ANÁLISIS DE RITMO DE CARRERA (Datos) ---
    # -------------------------------------------------------------------------
    ax1.set_facecolor('#080808')

    # Título del Panel
    ax1.set_title(f'LEFT PANEL: TYRE DEGRADATION vs. LAP TIME\n{piloto.upper()} - {equipo} ({circuito.upper()})',
                 fontsize=14, fontweight='bold', color='white', pad=15)

    # Etiquetas de Ejes (con unidades correctas)
    ax1.set_xlabel('LAPS COMPLETED', fontsize=11, fontweight='bold', color='#CCCCCC')
    ax1.set_ylabel('LAP TIME (seconds)', fontsize=11, fontweight='bold', color='#CCCCCC')

    # Graficar el ritmo real
    ax1.plot(vueltas, tiempos, color='#00D2BE', linewidth=2.5, marker='.', markersize=7, label='Actual Lap Times')

    # Marcar Paradas en Pits Reales
    for i, parada in enumerate(paradas):
        # Línea punteada azul claro
        ax1.axvline(x=parada, color='#00FFFF', linestyle='--', linewidth=1.5, alpha=0.9)
        # Etiqueta de la parada (con rotación de 90 grados)
        ax1.text(parada + 0.5, max(tiempos), f'PIT STOP {i+1}\n(Lap {parada})',
                 color='#00FFFF', rotation=90, verticalalignment='top', fontsize=9, fontweight='bold')

    #CÁLCULO DE ANOTACIONES ESTRATÉGICAS
    if len(paradas) >= 1:
        stint1_times = tiempos[0:paradas[0]]
        stint2_times = tiempos[paradas[0]:] if len(paradas) == 1 else tiempos[paradas[0]:paradas[1]]

        # Anotación promedio Stint 1
        avg_stint1 = np.mean(stint1_times)
        y_pos = avg_stint1 - 1.5 # Un poco por debajo del promedio
        ax1.text(paradas[0]/2, y_pos, f'STINT 1 Pace: {avg_stint1:.1f}s',
                 color='#00D2BE', fontweight='bold', ha='center', fontsize=10, bbox=dict(facecolor='black', alpha=0.6))

        # Anotación promedio Stint
        if len(stint2_times) > 0:
            avg_stint2 = np.mean(stint2_times)
            center_x = (paradas[0] + vueltas[-1])/2
            ax1.text(center_x, avg_stint2 - 1.5, f'STINT 2 Pace: {avg_stint2:.1f}s',
                     color='#00D2BE', fontweight='bold', ha='center', fontsize=10, bbox=dict(facecolor='black', alpha=0.6))

    # Formateo de Ejes
    ax1.tick_params(axis='both', which='major', labelsize=10, colors='#888888')
    ax1.grid(True, color='gray', linestyle=':', alpha=0.3)
    ax1.xaxis.set_major_locator(ticker.MultipleLocator(10)) # Muestra vueltas cada 10

    # --------------------------------------------------------------------------------------
    # --- PANEL DERECHO: COMPARACIÓN ESTRATÉGICA (Ilustrativa, matching Image 10) ---
    # --------------------------------------------------------------------------------------
    ax2.set_facecolor('#080808')

    # Títulos del Panel
    ax2.set_title('RIGHT PANEL: STRATEGY COMPARISON & OPTIMIZATION\nPERFORMANCE CURVES: SOFT vs MEDIUM',
                 fontsize=14, fontweight='bold', color='white', pad=10)

    # Etiquetas de Ejes
    ax2.set_xlabel('LAPS COMPLETED', fontsize=11, fontweight='bold', color='#CCCCCC')

    # Ocultar el eje Y de la derecha
    ax2.get_yaxis().set_visible(False)

    # -- RECREACIÓN DE CURVAS DE DEGRADACIÓN --
    # Creamos un eje X de 0 a 60 vueltas
    x_ilus = np.linspace(0, 60, 200)

    # Fórmulas para Degradación:
    # 1. Medium (Color Verde, Suave degradación, mejor a largo plazo)
    # y = base + deg_suave * x
    t_medium = 87.0 + (0.15 * x_ilus)

    # 2. Soft (Color Rojo, Degradación rápida, cae "The Cliff")
    # y = base_agresiva + deg_media * x + deg_exponencial * x^2
    t_soft = 83.5 + (0.3 * x_ilus) + (0.005 * x_ilus**2)

    # Grafica Curvas
    # Medium (Color Verde)
    ax2.plot(x_ilus, t_medium, color='#39FF14', linewidth=2.5, label='MEDIUM (Optimal)')
    # Soft (Color Rojo)
    ax2.plot(x_ilus, t_soft, color='#FF3131', linewidth=2.5, label='SOFT (Aggressive)')

    # -- ANOTACIONES MATCHING --

    # 1. CROSSOVER POINT (Línea punteada azul claro vertical)
    cross_lap = 25 # Punto aproximado de cruce
    ax2.axvline(x=cross_lap, color='#00FFFF', linestyle='--', linewidth=1.5, alpha=0.9)
    ax2.text(cross_lap + 1, 95, 'CROSSOVER\nPOINT',
             color='#00FFFF', verticalalignment='top', fontsize=10, fontweight='bold', horizontalalignment='left')

    # 2. PIT STOP WINDOW (Línea punteada azul horizontal)
    pit_loss = 23 # Tiempo estimado de parada
    t_window_low = min(tiempos) # Base de tiempo de la carrera real
    t_window_high = t_window_low + pit_loss

    ax2.axhline(y=t_window_low, color='#00FFFF', linestyle=':', linewidth=1.5, alpha=0.7)
    ax2.axhline(y=t_window_high, color='#00FFFF', linestyle=':', linewidth=1.5, alpha=0.7)

    ax2.text(1, t_window_high - 1, 'PIT STOP WINDOW\nCROSSOVER POINT',
             color='#00FFFF', verticalalignment='top', fontsize=9, fontweight='bold')

    # 3. TIME SAVED IN PIT LANE (Anotación con flechas)
    save_start_x = 42
    save_end_x = 55
    y_save = t_window_low - 3 # Un poco por debajo de la ventana

    ax2.text(save_start_x + 1, y_save + 1, 'TIME SAVED IN PIT\nLANE (e.g., VSC/SC)',
             color='#00FFFF', fontsize=9, fontweight='bold')
    # Flecha
    ax2.annotate('', xy=(save_end_x, y_save), xytext=(save_start_x, y_save),
                arrowprops=dict(facecolor='#00FFFF', edgecolor='#00FFFF', arrowstyle='<->', linewidth=1.5))

    # Formateo de Ejes
    ax2.tick_params(axis='x', which='major', labelsize=10, colors='#888888')
    ax2.grid(True, color='gray', linestyle=':', alpha=0.3)
    ax2.xaxis.set_major_locator(ticker.MultipleLocator(10))
    # Eje Y para que los textos queden bien colocados
    ax2.set_ylim(min(t_window_low - 5, 80), max(t_soft[-1] + 5, 110))

    ax2.legend(loc='upper right', frameon=True, facecolor='black', edgecolor='white')

    # -- GUARDAR LA IMAGEN FINAL --
    # Guardar la imagen final con alta resolución (dpi=300) y bordes ajustados (bbox_inches='tight')
    plt.tight_layout()

    if not os.path.exists('outputs'):
        os.makedirs('outputs')

    ruta_img = f"outputs/analisis_estrategico_{piloto}_{circuito}.png"
    plt.savefig(ruta_img, dpi=300, bbox_inches='tight')
    plt.close()

    return ruta_img
