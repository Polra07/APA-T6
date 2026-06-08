"""
Alumno: Pol Ramirez Sanchez
"""

import re
import doctest


class Alumno:
    """
    Clase usada para el tratamiento de las notas de los alumnos.
    """
    def __init__(self, nombre, numIden=-1, notas=[]):
        self.numIden = numIden
        self.nombre = nombre
        self.notas = [nota for nota in notas]

    def __add__(self, other):
        return Alumno(self.nombre, self.numIden, self.notas + [other])

    def media(self):
        return sum(self.notas) / len(self.notas) if self.notas else 0

    def __repr__(self):
        return f'Alumno("{self.nombre}", {self.numIden!r}, {self.notas!r})'

    def __str__(self):
        return f'{self.numIden}\t{self.nombre}\t{self.media():.1f}'


def leeAlumnos(ficAlumnos):
    """
    Lee el fichero de texto que se le pasa como único 
    argumento y devuelve un diccionario con los datos de los alumnos.
    
    >>> alumnos = leeAlumnos('alumnos.txt')
    >>> for alumno in alumnos:
    ...     print(alumnos[alumno])
    ...
    171     Blanca Agirrebarrenetse 9.5
    23      Carles Balcells de Lara 4.9
    68      David Garcia Fuster     7.0
    """
    alumn = {}
    expr_id = r'\s*(?P<id>\d+)\s+'
    # El operador +? asegura que tome el nombre completo sin comerse las notas
    expr_nom = r'(?P<nom>[\w\s]+?)\s+'
    expr_notes = r'(?P<notes>[\d.\s]+)\s*'
    expresion = re.compile(expr_id + expr_nom + expr_notes)
    
    with open(ficAlumnos, 'rt', encoding='utf-8') as fpAlumnos: 
        for linea in fpAlumnos:
            linea_limpia = linea.strip()
            if not linea_limpia:
                continue
            match = expresion.match(linea_limpia)
            if match is not None: 
                id_alum = int(match['id'])
                nom = match['nom'].strip()
                notes = [float(nota) for nota in match['notes'].split()]
                alumn[nom] = Alumno(nom, id_alum, notes)
    return alumn

if __name__ == "__main__":
    # Esto ejecuta los tests automáticos al lanzar el script
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE, verbose=True)
    

