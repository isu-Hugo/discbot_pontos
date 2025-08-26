from datetime import datetime

hora = datetime.now().strftime('%H:%M:%S')

print(hora)

# SELECT (SUM(permanencia)/60) FROM calls WHERE id_usuario =