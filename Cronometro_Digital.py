import RPi.GPIO as GPIO
import time

# --- CONFIGURAÇÃO DOS PINOS ---

# Entradas BCD (A0–A3)
pinosBCD = [17, 27, 22, 23]  # GPIO17=A0, GPIO27=A1, GPIO22=A2, GPIO23=A3

# Latch Enable dos dois CD4511
latch_unidade = 24
latch_dezena = 25

# Botões
botao_mais = 5
botao_menos = 6

# --- CONFIGURAÇÃO GERAL ---
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Saídas
for p in pinosBCD:
    GPIO.setup(p, GPIO.OUT)

GPIO.setup(latch_unidade, GPIO.OUT)
GPIO.setup(latch_dezena, GPIO.OUT)

# Entradas (botões com pull-up interno)
GPIO.setup(botao_mais, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(botao_menos, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# --- VARIÁVEIS ---
minutos = 0
ultimo_mais = True
ultimo_menos = True
ultimo_tempo = time.time()

# --- FUNÇÕES AUXILIARES ---
def mostrar_numero(numero, latch_pin):
    GPIO.output(latch_pin, GPIO.LOW)
    for i in range(4):
        bit = (numero >> i) & 1
        GPIO.output(pinosBCD[i], bit)
    GPIO.output(latch_pin, GPIO.HIGH)

def atualizar_display():
    dezena = minutos // 10
    unidade = minutos % 10
    mostrar_numero(dezena, latch_dezena)
    mostrar_numero(unidade, latch_unidade)

# --- LOOP PRINCIPAL ---
print("Iniciando cronômetro de minutos... pressione Ctrl+C para parar.")
atualizar_display()

try:
    while True:
        agora = time.time()

        # Contagem automática (1 minuto = 60 segundos)
        if agora - ultimo_tempo >= 60:
            minutos = (minutos + 1) % 60
            atualizar_display()
            ultimo_tempo = agora

        # Botão "+"
        estado_mais = GPIO.input(botao_mais)
        if not estado_mais and ultimo_mais:
            minutos = (minutos + 1) % 60
            atualizar_display()
            time.sleep(0.2)
        ultimo_mais = estado_mais

        # Botão "-"
        estado_menos = GPIO.input(botao_menos)
        if not estado_menos and ultimo_menos:
            minutos = (minutos - 1) % 60
            atualizar_display()
            time.sleep(0.2)
        ultimo_menos = estado_menos

        time.sleep(0.05)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("\nPrograma encerrado.")
