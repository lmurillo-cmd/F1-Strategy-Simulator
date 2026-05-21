import math

def calcular_tiempo_restante(vuelta_actual, vueltas_totales, neumatico, factor_deg, tiene_daño, es_lluvia): 
    """Función interna para que el código 'piense' en el futuro."""
    tiempo_futuro = 0
    # Multiplicadores de rendimiento y desgaste según neumático
    configs = {
        'BLANDO': {'base': 83.5, 'mult': 1.3},
        'MEDIO':  {'base': 85.0, 'mult': 1.0},
        'DURO':   {'base': 86.5, 'mult': 0.7},
        'INTER':  {'base': 88.5, 'mult': 1.0}
    }

    conf = configs[neumatico]
    v_neumatico = 1
    for v in range(vuelta_actual, vueltas_totales + 1):
        t = conf['base'] + (v_neumatico * factor_deg * conf['mult'])
        if tiene_daño: t += 3.5
        if es_lluvia and neumatico != 'INTER': t += 15.0 # Penalización masiva si no usa intermedios
        elif es_lluvia and neumatico == 'INTER': t += 5.0 # Lluvia normal

        tiempo_futuro += t
        v_neumatico += 1

    return tiempo_futuro

def simular_carrera(pista, piloto, clima_inicial, sc_inicial, posicion_salida):
    # 1. Configuración Inicial
    vueltas_totales = int(pista['Vueltas'])
    factor_deg = float(pista['Degradacion_Base']) * (float(pista['Longitud_km']) / 5.0)

    tiempos = []
    v_actual = 1
    v_neumatico = 1
    daño_ala = False
    lluvia = clima_inicial
    en_safety_car = sc_inicial
    neumatico_actual = "MEDIO"
    t_base = 85.0
    mult_deg = 1.0
    paradas_reales = []

    # --- CÁLCULO DE ESTRATEGIA INICIAL ---
    print(f"\n🧠 INGENIERO: 'Analizando pista... Calculando mejor estrategia para {pista['Circuito']} salienfo P{posicion_salida}...'")

    # --- CÁLCULO DE ESTRATEGIA INICIAL INTELIGENTE ---
    print(f"\n🧠 INGENIERO: 'Analizando condiciones iniciales en {pista['Circuito']}...'")

    if lluvia:
        neumatico_actual = "INTER"
        t_base = 88.5
        mult_deg = 1.0
        print("🌧️ ESTRATEGIA INICIAL: Pista mojada. Salida obligatoria con INTERMEDIOS.")
        print("💧 INGENIERO: 'Mantendremos los de lluvia hasta que la pista se seque'.")
    else:
      if posicion_salida > 10:
        print(f"🚦 INGENIERO: 'Salimos muy atrás (P{posicion_salida}). Iremos a la contra con DUROS para evitar tráfico en pits'.")
        neumatico_actual = "DURO"
        conf_inicial = {'DURO': 86.5}
        mults_inicial = {'DURO': 0.7}
        t_base = conf_inicial[neumatico_actual]
        mult_deg = mults_inicial[neumatico_actual]

      else:
        # Ponemos a competir 3 estrategias diferentes simulando hasta el final de la carrera:
        # 1. Agresiva: BLANDO a DURO (Parada temprana en el 25% de la carrera)
        v_blando = int(vueltas_totales * 0.25)
        t_estrategia_blanda = calcular_tiempo_restante(1, v_blando, 'BLANDO', factor_deg, False, False) + 23.0 + \
                              calcular_tiempo_restante(v_blando+1, vueltas_totales, 'DURO', factor_deg, False, False)

        # 2. Equilibrada: MEDIO a DURO (Parada en el 40% de la carrera)
        v_medio = int(vueltas_totales * 0.40)
        t_estrategia_media = calcular_tiempo_restante(1, v_medio, 'MEDIO', factor_deg, False, False) + 23.0 + \
                             calcular_tiempo_restante(v_medio+1, vueltas_totales, 'DURO', factor_deg, False, False)

        # 3. Larga: DURO a BLANDO (Parada tardía en el 65% de la carrera)
        v_duro = int(vueltas_totales * 0.65)
        t_estrategia_dura = calcular_tiempo_restante(1, v_duro, 'DURO', factor_deg, False, False) + 23.0 + \
                            calcular_tiempo_restante(v_duro+1, vueltas_totales, 'BLANDO', factor_deg, False, False)

        # Se elige la que tenga el MENOR tiempo total
        tiempos_estrategias = {'BLANDO': t_estrategia_blanda, 'MEDIO': t_estrategia_media, 'DURO': t_estrategia_dura}
        mejor_llanta = min(tiempos_estrategias, key=tiempos_estrategias.get)

        # Asignamos las variables iniciales según la estrategia elegida
        neumatico_actual = mejor_llanta
        conf_inicial = {'BLANDO': 83.5, 'MEDIO': 85.0, 'DURO': 86.5}
        mults_inicial = {'BLANDO': 1.3, 'MEDIO': 1.0, 'DURO': 0.7}
        t_base = conf_inicial[neumatico_actual]
        mult_deg = mults_inicial[neumatico_actual]

        # Imprimimos el reporte según la estrategia
        if neumatico_actual == 'BLANDO':
            print(f"☀️ ESTRATEGIA ÓPTIMA: Agresiva. Salida con BLANDOS, parada sugerida V{v_blando} por DUROS.")
        elif neumatico_actual == 'MEDIO':
            print(f"☀️ ESTRATEGIA ÓPTIMA: Equilibrada. Salida con MEDIOS, parada sugerida V{v_medio} por DUROS.")
        else:
            print(f"☀️ ESTRATEGIA ÓPTIMA: Overcut. Stint largo con DUROS, parada sugerida V{v_duro} por BLANDOS.")


    # --- CICLO DE CARRERA ---
    while v_actual <= vueltas_totales:
        # Calcular vuelta actual
        t_v = t_base + (v_neumatico * factor_deg * mult_deg)
        if daño_ala: t_v += 3.5
        if lluvia: t_v += 10.0

        if en_safety_car and v_actual <= 3:
            t_v += 25.0
            if v_actual == 3:
              print("\n🟢 INGENIERO: 'Safety Car en esta vuelta, preparamos relanzada'.")
              en_safety_car = False

        tiempos.append(t_v)

        # Interacción cada 10 vueltas
        if v_actual % 10 == 0 and v_actual < vueltas_totales:
            print(f"\n--- 📻 RADIO VUELTA {v_actual} ---")
            print(f"Estado: Neumático {neumatico_actual} ({v_neumatico} vueltas) | Ala: {'Dañada' if daño_ala else 'OK'} | Clima: {'Lluvia' if lluvia else 'seco'}")

            # El usuario solo informa los hechos, no decide la estrategia
            hay_choque = input("¿Hubo algún incidente/daño? (s/n): ").lower() == 's'
            hay_cambio_clima = input("¿Empezó/ Dejo de llover en el pitlane? (Escribe 's' si cambió): ").lower() == 's'

            if hay_choque: daño_ala = True
            if hay_cambio_clima:
              lluvia = not lluvia
              print(f"🌦️ INGENIERO: 'Copiado, actualizamos radares a pista {'mojada' if lluvia else 'seca'}.'")

            # --- RECALCULACIÓN INTELIGENTE ---
            print("🧐 INGENIERO: 'Recalculando... analizando opciones...'")

            # El código compara: ¿Es mejor seguir o entrar YA?
            tiempo_si_sigo = calcular_tiempo_restante(v_actual+1, vueltas_totales, neumatico_actual, factor_deg, daño_ala, lluvia)

            # Probar opciones de boxes
            opciones = ['DURO', 'MEDIO', 'BLANDO'] if not lluvia else ['INTER']
            mejor_opcion = neumatico_actual
            menor_tiempo = tiempo_si_sigo

            for opt in opciones:
                # Tiempo de la parada (23s) + tiempo con el nuevo neumático
                t_con_parada = 23.0 + calcular_tiempo_restante(v_actual+1, vueltas_totales, opt, factor_deg, False, lluvia)
                if t_con_parada < menor_tiempo:
                    menor_tiempo = t_con_parada
                    mejor_opcion = opt

            if mejor_opcion != neumatico_actual:
                print(f"🚨 ¡BOX BOX! Estrategia optimizada: Entramos ahora por neumáticos {mejor_opcion}.")
                if daño_ala: print("🔧 Aprovecharemos para cambiar el ala delantera.")

                # Ejecutar la parada
                tiempos[-1] += 23.0
                neumatico_actual = mejor_opcion
                daño_ala = False
                v_neumatico = 0 # Neumático nuevo
                paradas_reales.append(v_actual)

                # Actualizar bases de tiempo
                conf = {'BLANDO': 83.5, 'MEDIO': 85.0, 'DURO': 86.5, 'INTER': 88.5}
                mults = {'BLANDO': 1.3, 'MEDIO': 1.0, 'DURO': 0.7, 'INTER': 1.0}
                t_base = conf[mejor_opcion]
                mult_deg = mults[mejor_opcion]
            else:
                print("✅ INGENIERO: 'Mantente fuera, los números dicen que sigues siendo rápido'.")

        v_actual += 1
        v_neumatico += 1

    return tiempos, paradas_reales, f"Estrategia finalizada con {neumatico_actual}"

