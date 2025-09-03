import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Constantes
m_dado = 3.5
sd_dado = np.sqrt(17.5 / 6)

# Función adaptada
def ilustrar_tcl(n, m, m_dado, sd_dado, clases=20):
    muestras = np.random.randint(1, 7, size=(m, n))
    
    # Mostrar la primera muestra
    st.write(f"{m} como estas: ", muestras[0])
    
    promedios = np.mean(muestras, axis=1)
    
    fig, ax = plt.subplots(figsize=(8,5))
    
    # Histograma
    bins = np.linspace(promedios.min(), promedios.max(), clases)
    ax.hist(promedios, bins=bins, density=True, alpha=0.6, color='skyblue', label='Promedios')
    
    # Normal teórica según TCL
    mu = m_dado
    sigma = sd_dado / np.sqrt(n)
    x = np.linspace(min(promedios), max(promedios), 200)
    ax.plot(x, norm.pdf(x, mu, sigma), 'r-', lw=2, label='Normal teórica')
    
    ax.set_xlabel('Promedio de la muestra')
    ax.set_ylabel('Densidad')
    ax.set_title(f'TCL: {m} muestras de {n} tiradas')
    ax.legend()
    
    return fig, muestras

# Interfaz de Streamlit
st.title("Visualización del TCL con tiradas de dado")

# Entradas del usuario
n = st.number_input("Número de tiradas por muestra (n)", min_value=1, value=10, step=1)
m = st.number_input("Número de muestras (m)", min_value=1, value=100, step=1)
clases = st.number_input("Cantidad de clases (opcional)", min_value=1, value=20, step=1)

# Inicializar estado para las muestras
if "muestras" not in st.session_state:
    st.session_state.muestras = None

col1, col2 = st.columns([1,1])

with col1:
    if st.button("Generar histograma"):
        fig, st.session_state.muestras = ilustrar_tcl(n, m, m_dado, sd_dado, clases)
        st.pyplot(fig)

with col2:
    if st.button("Resetear"):
        st.session_state.muestras = None
        st.experimental_rerun()  # recarga la app para limpiar

# Mostrar la primera muestra si hay tiradas
if st.session_state.muestras is not None:
    st.write("Primera muestra actual:", st.session_state.muestras[0])
