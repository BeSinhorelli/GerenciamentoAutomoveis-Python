
def ler_temperatura(mes):
    while True:
        try:
            temp = float(input("Digite a temperatura máxima de "+ mes+" (-60 a 50 °C): "))
            if -60 <= temp <= 50:
                return temp
            else:
                print("Erro: a temperatura deve estar entre -60 e 50 °C.")
        except ValueError:
            print("Erro: digite um número válido.")

meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
         "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

t1 = ler_temperatura(meses[0])
t2 = ler_temperatura(meses[1])
t3 = ler_temperatura(meses[2])
t4 = ler_temperatura(meses[3])
t5 = ler_temperatura(meses[4])
t6 = ler_temperatura(meses[5])
t7 = ler_temperatura(meses[6])
t8 = ler_temperatura(meses[7])
t9 = ler_temperatura(meses[8])
t10 = ler_temperatura(meses[9])
t11 = ler_temperatura(meses[10])
t12 = ler_temperatura(meses[11])

media = (t1 + t2 + t3 + t4 + t5 + t6 + t7 + t8 + t9 + t10 + t11 + t12) / 12

quentes = 0
if t1 > 33: quentes += 1
if t2 > 33: quentes += 1
if t3 > 33: quentes += 1
if t4 > 33: quentes += 1
if t5 > 33: quentes += 1
if t6 > 33: quentes += 1
if t7 > 33: quentes += 1
if t8 > 33: quentes += 1
if t9 > 33: quentes += 1
if t10 > 33: quentes += 1
if t11 > 33: quentes += 1
if t12 > 33: quentes += 1

mais_quente = t1
mes_mais_quente = meses[0]
menos_quente = t1
mes_menos_quente = meses[0]

if t2 > mais_quente: mais_quente, mes_mais_quente = t2, meses[1]
if t3 > mais_quente: mais_quente, mes_mais_quente = t3, meses[2]
if t4 > mais_quente: mais_quente, mes_mais_quente = t4, meses[3]
if t5 > mais_quente: mais_quente, mes_mais_quente = t5, meses[4]
if t6 > mais_quente: mais_quente, mes_mais_quente = t6, meses[5]
if t7 > mais_quente: mais_quente, mes_mais_quente = t7, meses[6]
if t8 > mais_quente: mais_quente, mes_mais_quente = t8, meses[7]
if t9 > mais_quente: mais_quente, mes_mais_quente = t9, meses[8]
if t10 > mais_quente: mais_quente, mes_mais_quente = t10, meses[9]
if t11 > mais_quente: mais_quente, mes_mais_quente = t11, meses[10]
if t12 > mais_quente: mais_quente, mes_mais_quente = t12, meses[11]

if t2 < menos_quente: menos_quente, mes_menos_quente = t2, meses[1]
if t3 < menos_quente: menos_quente, mes_menos_quente = t3, meses[2]
if t4 < menos_quente: menos_quente, mes_menos_quente = t4, meses[3]
if t5 < menos_quente: menos_quente, mes_menos_quente = t5, meses[4]
if t6 < menos_quente: menos_quente, mes_menos_quente = t6, meses[5]
if t7 < menos_quente: menos_quente, mes_menos_quente = t7, meses[6]
if t8 < menos_quente: menos_quente, mes_menos_quente = t8, meses[7]
if t9 < menos_quente: menos_quente, mes_menos_quente = t9, meses[8]
if t10 < menos_quente: menos_quente, mes_menos_quente = t10, meses[9]
if t11 < menos_quente: menos_quente, mes_menos_quente = t11, meses[10]
if t12 < menos_quente: menos_quente, mes_menos_quente = t12, meses[11]


print("\n--- Resultados ---")
print(f"Temperatura média máxima anual: {media:.2f} °C")
print(f"quantidade de meses escaldantes (> 33°C): {quentes}")
print(f"Mês mais escaldante: {mes_mais_quente} ({mais_quente} °C)")
print(f"Mês menos quente: {mes_menos_quente} ({menos_quente} °C)")
