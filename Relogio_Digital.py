import RPi.GPIO as GPIO
import time
from datetime import datetime

# --- CONFIGURAÇÃO DOS PINOS ---

# Pinos dos segmentos: a, b, c, d, e, f, g
segments = [2, 3, 4, 17, 27, 22, 10]

# Pinos dos 6 dígitos (catodos comuns)
# Da esquerda para a direita: H1, H2, M1, M2, S1, S2
displays = [9, 11, 5, 6, 13, 19]

# Configuração dos GPIOs
GPIO.setmode(GPIO.BCM)

for pin in segments + displays:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

# --- TABELA DOS NÚMEROS ---
# 1 = acende o segmento, 0 = apaga
numbers = {
    0: [1, 1, 1, 1, 1, 1, 0],
    1: [0, 1, 1, 0, 0, 0, 0],
    2: [1, 1, 0, 1, 1, 0, 1],
    3: [1, 1, 1, 1, 0, 0, 1],
    4: [0, 1, 1, 0, 0, 1, 1],
    5: [1, 0, 1, 1, 0, 1, 1],
    6: [1, 0, 1, 1, 1, 1, 1],
    7: [1, 1, 1, 0, 0, 0, 0],
    8: [1, 1, 1, 1, 1, 1, 1],
    9: [1, 1, 1, 1, 0, 1, 1]
}

# --- FUNÇÕES ---

def mostrar_digito(valor, display_index):
    """Acende o dígito específico com o número desejado"""
    if valor not in numbers:
        valor = 0
    # Ativa o número
    for i, seg in enumerate(segments):
        GPIO.output(seg, numbers[valor][i])
    # Liga o display atual
    GPIO.output(displays[display_index], 1)
    time.sleep(0.003)  # tempo de exibição (multiplex)
    GPIO.output(displays[display_index], 0)

def mostrar_horario(hora_str):
    """Mostra todos os 6 dígitos rapidamente"""
    for i, ch in enumerate(hora_str):
        mostrar_digito(int(ch), i)

# --- LOOP PRINCIPAL ---
try:
    while True:
        agora = datetime.now()
        hora = agora.strftime("%H%M%S")  # Ex: "134529"
        mostrar_horario(hora)
except KeyboardInterrupt:
    GPIO.cleanup()
