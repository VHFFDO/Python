import tm1638
from machine import Pin, Timer

tm = tm1638.TM1638(stb = Pin(20), clk = Pin(19), dio = Pin(18))
tm.brightness(0)
tm.clear()

# Varíaveis Globais
flag = segundos = minutos = horas = 0

# Interrupção por Timer
base_tempo = Timer()

def int_base_tempo(arg):
    global segundos, minutos, horas

    segundos += 1

    if segundos > 59:
        segundos = 0
        minutos += 1

    if minutos > 59:
        minutos = 0
        horas += 1

    if horas > 23:
        horas = minutos = segundos = 0

base_tempo.init(mode = Timer.PERIODIC, period = 1000, callback = int_base_tempo)
# Fim interrupção Timer

# Funções dos Botões
botoes = Timer()

def int_botoes(arg):
    global flag, segundos, minutos, horas

    if bt != 0:
        flag = bt

    elif bt == 0 and flag == 1:
        flag = 0
        horas += 1

    elif bt == 0 and flag == 2:
        flag = 0
        minutos += 1

    elif bt == 0 and flag == 4:
        flag = 0
        segundos = minutos = horas = 0

botoes.init(mode = Timer.PERIODIC, period = 60, callback = int_botoes)
# Fim funções dos Botoes

...
25 / 10 = 2.5          (float)
str(2.5) = "2.5"       (string)

0123
"2.5"

"2.5"[2:3] = 5         (unidade)
"2.5"[0:1] = 2         (dezena)
...

while True:
    # Leitura dos Botoes
    bt = tm.keys()
    # Unidade e Dezena dos Segundos
    tm.show(str(segundos / 10)[2:3], 7)
    tm.show(str(segundos / 10)[0:1], 6)
    # Unidade e Dezena dos Minutos
    tm.show(str(minutos / 10)[2:3], 3)
    tm.show(str(minutos / 10)[0:1], 2)
    # Unidade e Dezena dos Horas
    tm.show(str(horas / 10)[2:3] + '.', 1)
    tm.show(str(horas / 10)[0:1], 0)

