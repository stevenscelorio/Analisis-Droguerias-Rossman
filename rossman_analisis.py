import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

file_path = '/home/jarvis/PROYECTOS/python_cienciaDatos/Proyecto1/rossmann_sales_real.csv'
data = pd.read_csv(file_path)

data['Date'] = pd.to_datetime(data['Date'])

data.info()

data['StateHoliday'] = data['StateHoliday'].astype(str)

sales_1 = data['Sales'] > 0 

open_1 = data['Open'] == 1

data_limpio = data[sales_1 & open_1]

#Cuantas tiendas hay

store_count = data['Store'].nunique()

#Rango de fechas

date_range = data_limpio['Date']

#Promedio general

mean_general = data_limpio['Sales'].mean()
print(mean_general)
print(data_limpio.describe())

#Promedio por tienda

average_per_store = data_limpio.groupby('Store')['Sales'].mean()
print(average_per_store.describe())

#Crear columnas de mes y año

data_limpio['Year'] = data_limpio['Date'].dt.year
data_limpio['Month'] = data_limpio['Date'].dt.month

sales_month = data_limpio.groupby(['Year','Month'])['Sales'].sum()
sales_month_year = sales_month.unstack(level=0)
df = pd.DataFrame(sales_month_year)

ax = df.plot(figsize=(12, 6), marker='o', linewidth=2)

# 1. FORMATEAR EJE Y: Números completos con separador de miles sin decimales
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))

# 2. FORMATEAR EJE X: Forzar a que muestre del 1 al 12 y cambiar por nombres de meses
# Lista con los nombres de los meses en orden
meses_nombres = [
    'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
]

# Le decimos a Matplotlib que ponga una marca en cada número del 1 al 12
ax.xaxis.set_major_locator(ticker.FixedLocator(range(1, 13)))
# Reemplazamos los números 1-12 por los nombres de la lista
ax.xaxis.set_major_formatter(ticker.FixedFormatter(meses_nombres))

# Personalización de etiquetas y títulos
plt.title('Ventas Mensuales por Año', fontsize=14, fontweight='bold')
plt.xlabel('Meses', fontsize=12)
plt.ylabel('Total Ventas', fontsize=12)
plt.xticks(rotation=45) # Inclina los nombres de los meses para que no se amontonen
plt.grid(True, linestyle='--', alpha=0.5) # Cuadrícula de fondo opcional
plt.legend(title='Año')

plt.tight_layout()
plt.show()

store_per_year = data_limpio.groupby(['Year','Month'])['Sales'].mean()
print(store_per_year.unstack(level=0))

data['Year'] = data['Date'].dt.year
data['Month'] = data['Date'].dt.month
store_per_year1 = data.groupby(['Year','Month'])['SchoolHoliday'].count()
print(store_per_year1.unstack(level=0))

data_limpio['SalesCustomers'] = data_limpio['Sales'] / data_limpio['Customers']

customers_per_month = data_limpio.groupby(['Year','Month'])['Customers'].mean()
print(customers_per_month.unstack(level=0))

sales_per_customers = data_limpio.groupby(['Year','Month'])['SalesCustomers'].mean()
print(sales_per_customers.unstack(level=0))

#Crecimiento
#ventas por año

#1. Filtramos y agrupamos los datos
data_filtrada = data_limpio[data_limpio['Month'] <= 6]
growth = data_filtrada.groupby('Year')['Sales'].sum()

#2. Calculamos el porcentaje de crecimiento respecto al año anterior
#(Calcula la diferencia porcentual año contra año)
porcentaje_crecimiento = growth.pct_change() * 100

plt.figure(figsize=(10,6))
# Creamos el gráfico de barras
barras = plt.bar(growth.index.astype(str),growth.values, color='blue', label='Ventas Anuales')
plt.title('Comparación de ventas de los primeros 6 meses entre 2013 al 2015')
plt.ylabel('Ventas')
plt.xlabel('Años')

# Formatear el eje Y con separador de miles (puntos)
formatter = ticker.FuncFormatter(lambda x, pos: f'{int(x):,}'.replace(',','.'))
plt.gca().yaxis.set_major_formatter(formatter)

# 3. Recorremos cada barra para agregar el texto encima (Monto y Porcentaje)
for i, barra in enumerate(barras):
    altura = barra.get_height()
    monto_str = f'${int(altura):,}'.replace(',','.')

    # Para el primer año no hay crecimiento previo, solo mostramos el monto
    if i == 0:
        texto = f'{monto_str}\n(Base)'
    else: 
        pct = porcentaje_crecimiento.iloc[i]
        signo = '+' if pct > 0 else ''
        texto = f'{monto_str}\n({signo}{pct:.1f}%)'

    # Colocamos el texto justo arriba de la barra
    plt.text(
        barra.get_x() + barra.get_width() / 2,
        altura + (altura * 0.01), # Un pequeño espacio por encima de la barra
        texto,
        ha='center',
        va='bottom',
        fontsize=10,
        fontweight='bold'
    )

# Ajustamos el límite del eje Y para que los textos de arriba no queden cortados
plt.ylim(0, growth.max() * 1.15)

plt.legend(loc='upper left')
plt.tight_layout()
plt.show()

sales_promo = data_limpio.groupby('Promo')['Sales'].mean()

plt.figure(figsize=(12,6))

barras4 = plt.bar(sales_promo.index.astype(str),sales_promo.values,color='skyblue',label='Relacion de ventas con las promociones')

plt.title('Las promociones aumentas las ventas?')
plt.ylabel('Promedio de ventas')
plt.xlabel('Promoción y no promoción')
#Cambiamos las etiquetas del eje x
plt.xticks(
    ticks=[0,1],
    labels=['Sin Promoción','Con Promoción'],
    fontsize=11
)
plt.legend()
plt.tight_layout()
plt.show()

sales_holiday = data_limpio.groupby('StateHoliday')['Sales'].mean()
print(sales_holiday)

barra3 = plt.bar(sales_holiday.index.astype(str),sales_holiday.values,color='red',label='Diferencia de ventas entre feriado y no feriado')
plt.title('Diferencia entre ventas de un dia feriado a un día normal')
plt.ylabel('Promedio ventas por dia')
plt.xlabel('Diasferiados y normales')
plt.xticks(
    ticks=[0,1,2,3],
    labels=['Normal','Feriado','Pascuas','Navidad'],
    fontsize=12
)
plt.legend()
plt.tight_layout()
plt.show()

correlacion = data_limpio[['Customers','Sales']].corr()

plt.scatter(data_limpio['Customers'],data_limpio['Sales'],color='blue',alpha=0.3,edgecolors='none')

plt.title('Correlación entre clientes y ventas')
plt.xlabel('Cantidad de clientes')
plt.ylabel('Ventas totales')

formatter = ticker.FuncFormatter(lambda x, pos: f'{int(x):,}'.replace(',','.'))
plt.gca().yaxis.set_major_formatter(formatter)

plt.tight_layout()
plt.show()