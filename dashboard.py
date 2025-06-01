import streamlit as st
import pandas as pd
import plotly.express as px

# Layout wide
st.set_page_config(page_title="Despesas Familiares", layout="wide")

# ======== TÍTULO ========
st.markdown("<h1 style='text-align: center; color: #3366cc;'>📊 Dashboard de Despesas Mensais</h1>", unsafe_allow_html=True)

# ======== LEITURA DO ARQUIVO EXCEL ========
caminho_arquivo = "despesas.xlsx"

try:
    df = pd.read_excel(caminho_arquivo)

    # Conversão de datas
    df["Início Mês"] = pd.to_datetime(df["Início Mês"])
    df["Final Mês"] = pd.to_datetime(df["Final Mês"])
    df["Mês"] = df["Início Mês"].dt.strftime('%B/%Y')

    # ======== FILTRO DE MESES (MULTISELECT ESTILIZADO) ========
    st.divider()
    st.markdown("<h2 style='color:#3366cc;'>📅 Filtrar por Mês</h2>", unsafe_allow_html=True)

    meses = sorted(df["Mês"].unique().tolist())

    meses_selecionados = st.multiselect(
        "Selecione um ou mais meses para análise:",
        options=meses,
        default=meses,
        help="Você pode selecionar múltiplos meses segurando CTRL ou clicando em vários"
    )

    if not meses_selecionados:
        st.warning("Selecione ao menos um mês para visualizar os dados.")
        st.stop()

    df_filtrado = df[df["Mês"].isin(meses_selecionados)]

    # ======== MÉTRICAS DAS DESPESAS ========
    st.divider()
    st.subheader("💸 Totais por Categoria")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total com Água", f"R$ {df_filtrado['Água'].sum():,.2f}")
    col2.metric("Total com Luz", f"R$ {df_filtrado['Luz'].sum():,.2f}")
    col3.metric("Total com Internet", f"R$ {df_filtrado['Internet'].sum():,.2f}")
    col4.metric("Total com Gás", f"R$ {df_filtrado['Gás'].sum():,.2f}")

    # ======== GRÁFICO ========
    st.divider()
    st.subheader("📈 Variação Mensal das Despesas Totais")
    fig = px.line(
        df_filtrado,
        x="Mês",
        y="Total Despesas",
        title="Total de Despesas por Mês",
        markers=True,
        line_shape="spline",
        labels={"Total Despesas": "Total (R$)", "Mês": "Mês"},
    )
    fig.update_layout(
        xaxis_title="Mês",
        yaxis_title="Total de Despesas (R$)",
        title_x=0.5,
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

    # ======== DIVISÃO POR PESSOA (COLORIDO) ========
    st.divider()
    st.subheader("👨‍👩‍👧‍👦 Divisão por Pessoa")

    valor_por_pessoa = df_filtrado["Por pessoa"].sum()

    cores = {
        "Mãe": "#007BFF",     # Azul
        "Pai": "#28A745",     # Verde
        "Eliel": "#FFC107",   # Amarelo
        "Isac": "#DC3545"     # Vermelho
    }

    col_a, col_b, col_c, col_d = st.columns(4)

    for col, pessoa in zip([col_a, col_b, col_c, col_d], cores.keys()):
        cor = cores[pessoa]
        col.markdown(
            f"""
            <div style='
                background-color: {cor};
                padding: 30px;
                border-radius: 12px;
                text-align: center;
                box-shadow: 0 4px 10px rgba(0,0,0,0.15);
                color: white;
            '>
                <h3 style='margin-bottom: 10px;'>{pessoa}</h3>
                <p style='font-size: 26px; font-weight: bold;'>R$ {valor_por_pessoa:,.2f}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()
    st.caption("💡 Os valores são calculados com base nas despesas registradas por mês. Cada pessoa representa 25% do total.")

except FileNotFoundError:
    st.error(f"⚠️ Arquivo '{caminho_arquivo}' não encontrado. Coloque-o na mesma pasta do script.")
