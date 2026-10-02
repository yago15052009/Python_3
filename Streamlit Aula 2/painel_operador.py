import streamlit as st
import random

st.title("🚌 Expresso Mobilidade — Painel do Operador")
st.markdown("Sistema de gestão operacional de linhas urbanas")

# --- Identificação do Operador ---
nome = st.text_input("Digite seu nome:")
if nome:
    st.write(f"👋 Bem-vindo(a), **{nome}**! Pronto para gerenciar as rotas de hoje?")

st.divider()

# --- Consulta de Rota Específica ---
st.header("🔍 Consulta de Linha Prioritária")

linhas_disponiveis = {
    "510 - Terminal Central → Bairro Novo": ["06:00", "07:30", "09:00", "12:00", "17:00", "19:30"],
    "520 - Estação Norte → Shopping Sul":   ["06:15", "08:00", "10:00", "13:00", "16:30", "20:00"],
    "550 - Aeroporto → Centro Histórico":   ["05:30", "07:00", "09:30", "14:00", "18:00", "21:00"],
    "620 - Zona Leste → Terminal Central":  ["06:45", "08:30", "11:00", "15:00", "17:30", "22:00"],
}

linha = st.selectbox("Escolha uma linha para consultar horários:", list(linhas_disponiveis.keys()))

if linha:
    horarios = linhas_disponiveis[linha]
    st.write(f"🕐 Horários da linha **{linha}**:")
    st.write(" | ".join(horarios))

st.divider()

# --- Seleção de Múltiplas Linhas ---
st.header("📋 Relatório Consolidado de Passageiros")

linhas_selecionadas = st.multiselect(
    "Selecione as linhas para o relatório:",
    list(linhas_disponiveis.keys())
)

if linhas_selecionadas:
    st.write(f"✅ {len(linhas_selecionadas)} linha(s) selecionada(s) para o relatório.")

st.divider()

# --- Disparo de Ação ---
st.header("⚙️ Cálculo de Demanda e Distribuição de Frota")

if st.button("🚀 Calcular Demanda e Distribuir Frota"):
    if not linhas_selecionadas:
        st.warning("Selecione ao menos uma linha antes de calcular.")
    else:
        st.success("Processando distribuição de frota...")
        for l in linhas_selecionadas:
            passageiros = random.randint(120, 850)
            onibus = max(1, passageiros // 60)
            st.write(f"🚌 **{l}** → {passageiros} passageiros estimados | {onibus} ônibus necessários")
