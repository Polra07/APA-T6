"""
Alumno: Pol Ramirez Sanchez
"""

import re

def procesar_match(match):
    texto_original = match.group(0)
    
    # 1. Formato HH:MM o H:MM
    if match.group('h1') and match.group('m1'):
        h = int(match.group('h1'))
        m = int(match.group('m1'))
        if h < 24 and m < 60 and len(match.group('m1')) == 2:
            return f"{h:02}:{m:02}"
        return texto_original

    # 2. Formato XhYm o Xh
    if match.group('h2'):
        h = int(match.group('h2'))
        m = int(match.group('m2')) if match.group('m2') else 0
        if h < 24 and m < 60:
            return f"{h:02}:{m:02}"
        return texto_original

    # 3. Formatos verbales (en punto, y cuarto, y media, menos cuarto)
    if match.group('h_v'):
        h = int(match.group('h_v'))
        mod = match.group('mod')
        periodo = match.group('periodo')

        if h < 1 or h > 12:
            return texto_original  # El formato verbal usa reloj de 12 horas (1 a 12)

        # Determinar minutos según el modificador
        m = 0
        if mod == 'y cuarto': m = 15
        elif mod == 'y media': m = 30
        elif mod == 'menos cuarto': 
            m = 45
            h = h - 1 if h > 1 else 12

        # Ajuste por período (mañana, tarde, noche, etc.)
        if periodo:
            if 'mañana' in periodo and (h < 4 or h > 12): return texto_original
            if 'mediodía' in periodo and (h != 12 and h > 3): return texto_original
            if 'tarde' in periodo and (h < 3 or h > 8): return texto_original
            if 'noche' in periodo and (h < 8 and h > 4): return texto_original
            if 'madrugada' in periodo and (h < 1 or h > 6): return texto_original

            # Conversión a formato 24h
            if ('tarde' in periodo or 'noche' in periodo or 'mediodía' in periodo) and h < 12:
                h += 12
            elif 'madrugada' in periodo and h == 12:
                h = 0
            elif 'mañana' in periodo and h == 12:
                h = 12 # 12 de la mañana es mediodía
        else:
            # Si no hay periodo, el enunciado dice que se devuelve en el rango 00:00 a 11:59
            if h == 12: h = 0

        return f"{h:02}:{m:02}"

    # 4. Caso especial estricto: 12 de la noche
    if texto_original == "12 de la noche":
        return "00:00"

    return texto_original

def normalizaHoras(ficText, ficNorm):
    # Una regex maestra que captura limpiamente todas las variantes competitivas
    pattern = re.compile(
        r'\b(?P<h1>\d{1,2}):(?P<m1>\d{1,2})\b' # 18:30
        r'|\b(?P<h2>\d{1,2})h(?:(?P<m2>\d{1,2})m)?\b' # 8h27m o 8h
        r'|\b(?P<h_v>\d{1,2})\s+(?P<mod>en punto|y cuarto|y media|menos cuarto)(?:\s+de la\s+(?P<periodo>mañana|tarde|noche|madrugada)|\s+del\s+(?P<periodo_m>mediodía))?'
        r'|\b12 de la noche\b'
    )

    with open(ficText, 'r', encoding='utf-8') as infile, open(ficNorm, 'w', encoding='utf-8') as outfile:
        for linea in infile:
            # Reemplazamos usando la función inteligente paso a paso
            linea_cambiada = pattern.sub(procesar_match, linea)
            outfile.write(linea_cambiada)

# Ejecución local opcional
if __name__ == "__main__":
    try:
        normalizaHoras('horas.txt', 'horasNorm.txt')
        print("Horas normalizadas con éxito en 'horasNorm.txt'.")
    except FileNotFoundError:
        pass