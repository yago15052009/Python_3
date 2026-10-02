import streamlit as st
import pandas as pd

# Passo 4 - Olá, mundo
st.write("Olá, mundo")

# Passo 6 e 7 - Variáveis com nome e idade
nome = "Yago"
idade = 17
st.write(f"Nome: {nome}, Idade: {idade}")

# Passo 11 - Título
st.title("Meu primeiro dash")

# Passo 12 - Subtítulo
st.subheader("Yago")

# Passo 10 e 13 - DataFrame
df = pd.DataFrame({
    'first column': ['Português', 'Matemática', 'Python', 'Frame'],
    'second column': [5, 9, 7, 10]
})

st.write(df)
