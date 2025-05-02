import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def generar_grafico(sesiones_diarias):
    # Crear lista de últimos 7 días
    hoy = datetime.now().date()
    dias = [hoy - timedelta(days=i) for i in range(6, -1, -1)]
    etiquetas = [dia.strftime('%d-%m') for dia in dias]
    valores = [sesiones_diarias.get(dia.strftime('%Y-%m-%d'), 0) for dia in dias]

    # Crear gráfico
    plt.figure(figsize=(10, 5))
    barras = plt.bar(etiquetas, valores, color='steelblue')

    # Etiquetas arriba de cada barra
    for barra, valor in zip(barras, valores):
        plt.text(barra.get_x() + barra.get_width() / 2, barra.get_height() + 0.1, str(valor),
                 ha='center', va='bottom', fontsize=10)

    # Configuraciones estéticas
    plt.title('Pomodoros realizados en los últimos 7 días')
    plt.xlabel('Fecha')
    plt.ylabel('Cantidad de Pomodoros')
    plt.tight_layout()

    # Guardar gráfico
    plt.savefig('grafico_semanal.png')
    plt.close()