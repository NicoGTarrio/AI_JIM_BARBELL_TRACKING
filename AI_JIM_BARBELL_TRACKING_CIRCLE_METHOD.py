# -*- coding: utf-8 -*-
"""
Ai_Jim - Barbell tracking Circle method
20.02.24
"""

import cv2 as cv
import numpy as np


Captura = cv.VideoCapture(1) 
"El nº depende de la entrada de video"
circuloAnterior = None
distancia = lambda x1,y1,x2,y2: (x1-x2)**2+(y1-y2)**2

while True:
    ret, frame = Captura.read()
    if not ret: break
    
    Ventanagris = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) 
    "Cambio los colores de BGR a una escala de gris"
    Ventanaborrosa = cv.GaussianBlur(Ventanagris, (19,19), 0)
    " (contenido que quiero hacer borroso, tupla de nº impares cuanto mas"
    "grandes mas borroso, sigma )"
    cv.imshow("Ventanaborrosa", Ventanaborrosa)
    
    circulos = cv.HoughCircles(Ventanaborrosa, cv.HOUGH_GRADIENT, 1.4, 300,
                               param1=100, param2=30, minRadius=50, maxRadius=200)
    "La minima distancia la pongo a 300 por que solo quiero que haya un cirulo, el centro de la barra"
    "param1 sensibilidad para encontrar cirulos 100 funciona bien en mi caso"
    "param2 numero de bordes para encontrar circulos"
    "Pongo maxradius muy bajo por que no quiero que confunda las pesas con la barra pero depende tambien de dodne esta la camara"
    
    if circulos is not None:
        circulos = np.uint16(np.around(circulos)) 
        "Convierto en un array en np"
        circulomejor = None
        for i in circulos[0, :]:
            if circulomejor is None :
                circulomejor = i
            if circuloAnterior is not None:
                if distancia(circulomejor[0], circulomejor[1], circuloAnterior[0],
                             circuloAnterior[1]) <= distancia(i[0],i[1],circuloAnterior[0],circuloAnterior[1]):
                    circulomejor = i
                cv.cirle(frame, (circulomejor[0], circulomejor[1]), 1, (0,0,255), 5 )
                cv.cirle(frame, (circulomejor[0], circulomejor[1]), circulomejor[2], (0,255,0), 3 )
                circuloAnterior = circulomejor
                "Refina el circulo"
    
   
    cv.imshow("CIRCULOS", frame)
    if cv.waitKey(1) & 0xFF == ord('p'): break 
    "Esto hace que cuando le de a P el bucle pare" 
    
Captura.release()
"Para la grabación"
cv.destroyAllWindows() 
"Cierra las ventanas"