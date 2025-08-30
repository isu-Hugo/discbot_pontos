# from datetime import datetime

# hora = datetime.now().strftime('%H:%M:%S')

# print(hora)

# SELECT (SUM(permanencia)/60) FROM calls WHERE id_usuario =

# class TimeFormatter():
#     def __init__(self):
#         self.att = "oi"
#         # pass

#     def getOi(self):
#         return self.att


# print(TimeFormatter().getOi())

# from datetime import timedelta, datetime

# duracao = 5459

# segundos = duracao % 60
# minutos = (duracao % 60) // 60
# horas = duracao // 3600

# horas = (duracao // 3600)
# minutos = (duracao % 3600) // 60
# segundos = (duracao % 60)

# print(f"H:{horas} M:{minutos} S:{segundos}")

medalhas = [":first_place:", ":second_place:", ":third_place:", ":medal:"]

for i, m in enumerate(medalhas):
    print(f"{i} - {m}")


# print("Minutos", minutos)
# print("Horas", horas)