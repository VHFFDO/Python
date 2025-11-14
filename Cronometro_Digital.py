import RPi.GPIO as GPIO
import time
from datetime import datetime

GPIO.setmode(GPIO.BCM)

# ------------------------------------------
#  PINOS DO CD4511 – ADAPTE EXATAMENTE ASSIM
# ------------------------------------------

# CD4511 – dígito das unidades (0–9)
U_A = 5
U_B = 6
U_C = 13
U_D = 19

# CD4511 – dígito das dezenas (0–5)
D_A = 12
D_B = 16
D_C = 20
D_D = 21

# Configura como saída
for p in [U_A, U_B, U_C, U_D, D_A, D_B, D_C, D_D]:
    GPIO.setup(p, GPIO.OUT)
    GPIO.output(p, 0)

# ------------------------------------------
#  PINOS DOS BOTÕES
# ------------------------------------------
BT_UP = 23
BT_DOWN = 24

GPIO.setup(BT_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BT_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# ------------------------------------------
#  FUNÇÃO PARA MOSTRAR NÚMERO NO CD4511
# ------------------------------------------
def mostrar_digito(digito, pinos):
    A, B, C, D = pinos

    tabela = {
        0: (0,0,0,0),
        1: (0,0,0,1),
        2: (0,0,1,0),
        3: (0,0,1,1),
        4: (0,1,0,0),
        5: (0,1,0,1),
        6: (0,1,1,0),
        7: (0,1,1,1),
        8: (1,0,0,0),
        9: (1,0,0,1)
    }

    bcd = tabela[digito]

    GPIO.output(A, bcd[0])
    GPIO.output(B, bcd[1])
    GPIO.output(C, bcd[2])
    GPIO.output(D, bcd[3])


# ------------------------------------------
#  FUNÇÃO DE ATUALIZAR DISPLAYS
# ------------------------------------------
def mostrar_minutos(minutos):
    unidades = minutos % 10
    dezenas = minutos // 10

    mostrar_digito(unidades, (U_A, U_B, U_C, U_D))
    mostrar_digito(dezenas, (D_A, D_B, D_C, D_D))


# ------------------------------------------
#  CONTADOR PRINCIPAL
# ------------------------------------------
minutos = 0
ultimo_incremento = time.time()

print("Sistema iniciado!")

try:
    while True:

        # Atualiza a cada 60 segundos
        agora = time.time()
        if agora - ultimo_incremento >= 60:
            minutos += 1
            if minutos >= 60:
                minutos = 0
            ultimo_incremento = agora

        # Botão de aumentar
        if GPIO.input(BT_UP) == 0:
            minutos += 1
            if minutos >= 60:
                minutos = 0
            time.sleep(0.25)     # debounce

        # Botão de diminuir
        if GPIO.input(BT_DOWN) == 0:
            minutos -= 1
            if minutos < 0:
                minutos = 59
            time.sleep(0.25)     # debounce

        mostrar_minutos(minutos)
        time.sleep(0.05)

except KeyboardInterrupt:
    GPIO.cleanup()
