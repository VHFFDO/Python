import RPi.GPIO as GPIO
import time
from datetime import datetime

# Configuração dos pinos
# - Pinos dos segmentos: a, b, c, d, e, f, g
segments = [2, 3, 4, 17, 27, 22, 10]

#Pinos dos 6 dígitos (catodos comuns)
# - Da esquerda para a direita: H1, H2, M1, M2, S1, S2
displays = [9, 11, 5, 6, 13, 19, 26, 10]

# Se você só quer usar 6 dígitos (HHMMSSS), usaremos displays[0..5].
USAR_DIGITOS = 6 # alterar para8 se quiser usar os 8 dígitos

# Configuração dos GPIOs
GPIO.setmode(GPIO.BCM)
for pin in segments + displays:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    
# Tabela dos números
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

# Funções
def set_segments_for_digit(value):
    """Define os pinos dos segmentos para o número value (0-9)."""
    pattern = numbers.get(value, numbers[0])
    for seg_pin, seg_val in zip(segments, pattern):
        GPIO.output(seg_pin, GPIO.HIGH if sg_val else GPIO.LOW)
    
def mostrar_digito(valor, display_index, on_time = 0.003):
    """Acende o dígito específico com o número desejado"""
    # Ajuste dos segmentos
    set_segments_for_digit(valor)
        
    # Liga o display atual
    GPIO.output(displays[display_index], GPIO.HIGH)
    time.sleep(on_time) # Tempo de exibição (multiplex)
    GPIO.output(displays[display_index], GPIO.LOW)
    
def mostrar_horario(hora_str):
    """Mostra todos os 6 dígitos rapidamente"""
    for i in range(USAR_DIGITOS):
        mostrar_digito(int(hora_str[i]), i)
        
#Loop principal
try:
   ON_TIME = 0.0035
   
   while True:
        agora = datetime.now()
        hora = agora.strftime("%H%M%S")
        if len(hora) < USAR_DIGITOS:
            hora = hora.rjust(USAR_DIGITOS, '0')
            
        for i in range(USAR_DIGITOS):
            set_segments_for_digit(int(hora[i]))
            GPIO.output(displays[i], GPIO.HIGH)
            time.sleep(ON_TIME)
            GPIO.output(display[i], GPIO.LOW)
            
except KeyboardInterrupt:
    GPIO.cleanup()
