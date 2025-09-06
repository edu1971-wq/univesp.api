

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# ---
## Análise do Relatório Fiscal
st.header("Análise do Relatório Fiscal - Largo de Osasco")
st.write("Dados extraídos de um relatório fiscal para visualização em gráficos.")

# Os dados foram extraídos manualmente da imagem.
data = {
    'Linha': [329, 329, 329, 329, 329, 330, 329, 330, 329, 329, 329, 329, 329],
    'Carro': [329, 330, 329, 329, 330, 329, 330, 329, 329, 329, 329, 329, 330],
    'Partida': ['4:05', '5:15', '6:25', '7:50', '8:55', '10:25', '12:00', '13:30', '14:40', '15:50', '17:05', '18:20', '19:35'],
    'Entrada': ['4:05', '5:15', '6:15', '7:30', '8:55', '9:10', '10:45', '12:15', '13:25', '14:35', '15:45', '17:00', '18:15'],
    'Saida': ['4:49', '5:56', '7:22', '8:15', '9:04', '10:04', '11:33', '13:06', '14:10', '15:22', '16:32', '17:52', '19:01'],
    'Tempo': [44, 46, 67, 45, 54, 48, 51, 45, 47, 47, 52, 46, 52],
    'Catraca': ['4:05', '5:15', '6:25', '7:50', '8:55', '10:25', '12:00', '13:30', '14:40', '15:50', '17:05', '18:20', '19:35'],
    'Retorno': ['7:50', '8:55', '10:25', '12:00', '13:30', '14:40', '15:50', '17:05', '18:20', '19:35', '20:50', '22:25', '23:40'],
    'Motorista': ['Odenilton', 'Odenilton', 'Jessy', 'Jessy', 'Odenilton', 'Odenilton', 'Odenilton', 'Odenilton', 'L Daniel', 'Dantas', 'S DANIEL', 'Dantas', 'S DANIEL'],
    'Cobrador': ['Odenilton', 'Odenilton', 'Jessy', 'Jessy', 'Odenilton', 'Odenilton', 'Odenilton', 'Odenilton', 'L Daniel', 'Dantas', 'S DANIEL', 'Dantas', 'S DANIEL'],
    'Pass.': [24, 22, 44, 16, 17, 13, 15, 8, 15, 17, 17, 17, 19],
    'Observações': [None, None, None, None, None, None, None, None, 'REND', None, None, None, None]
}

df = pd.DataFrame(data)

# Processamento de dados
df['Catraca'] = pd.to_datetime(df['Catraca'], format='%H:%M', errors='coerce')
df['Retorno'] = pd.to_datetime(df['Retorno'], format='%H:%M', errors='coerce')
df.dropna(subset=['Catraca', 'Retorno'], inplace=True)

# Calcula a duração e ajusta para o horário que passa da meia-noite
df['Duração (minutos)'] = (df['Retorno'] - df['Catraca']).dt.total_seconds() / 60
df.loc[df['Duração (minutos)'] < 0, 'Duração (minutos)'] += 24 * 60
df['Duração (horas)'] = df['Duração (minutos)'] / 60

# Limpa e conta as observações
df['REND'] = df['Observações'].str.contains('REND', na=False)

# ---
## Gráficos Interativos
st.header("Gráficos por Motorista")
st.write("Use o seletor abaixo para filtrar os dados por motorista.")

# Dropdown para selecionar um motorista
all_drivers = ['Todos'] + sorted(df['Motorista'].dropna().unique())
selected_driver = st.selectbox("Selecione um Motorista:", all_drivers)

filtered_df = df if selected_driver == 'Todos' else df[df['Motorista'] == selected_driver]

# ---
### Número de Viagens por Motorista
st.subheader("Número de Viagens")

trip_counts = filtered_df.groupby('Motorista').size().reset_index(name='Viagens')
fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.bar(trip_counts['Motorista'], trip_counts['Viagens'], color='skyblue')
ax1.set_title('Número de Viagens por Motorista')
ax1.set_xlabel('Motorista')
ax1.set_ylabel('Nº de Viagens')
ax1.tick_params(axis='x', rotation=45)
st.pyplot(fig1)

# ---
### Duração Total de Viagens por Motorista
st.subheader("Duração Total de Viagens (em horas)")

total_duration = filtered_df.groupby('Motorista')['Duração (horas)'].sum().reset_index()
fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.bar(total_duration['Motorista'], total_duration['Duração (horas)'], color='lightgreen')
ax2.set_title('Duração Total de Viagens por Motorista')
ax2.set_xlabel('Motorista')
ax2.set_ylabel('Duração Total (horas)')
ax2.tick_params(axis='x', rotation=45)
st.pyplot(fig2)

# ---
### Contagem de Observações
if 'REND' in filtered_df.columns:
    st.subheader("Contagem de Observações ('REND')")
    rend_count = filtered_df.groupby('Motorista')['REND'].sum().reset_index(name='Contagem de REND')
    if not rend_count.empty and rend_count['Contagem de REND'].sum() > 0:
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        ax3.bar(rend_count['Motorista'], rend_count['Contagem de REND'], color='salmon')
        ax3.set_title('Contagem de Observações "REND"')
        ax3.set_xlabel('Motorista')
        ax3.set_ylabel('Contagem')
        st.pyplot(fig3)
    else:
        st.write("Nenhuma ocorrência de 'REND' encontrada nos dados filtrados.")

# ---
## Tabela de Dados Originais
st.header("Tabela de Dados")
st.write(filtered_df)







import streamlit as st
import pandas as pd

# Exemplo de dados (substitua pelos seus dados do PDF)
data_domingos = {
    'Unidade': ['Intermunicipal G1', 'Municipal Osasco G4', 'Seletivo G4', 'Total Osasco G1+G4', 'Intermunicipal G5', 'Total Santana G5'],
    'Frota Média': [42.0, 45.0, 2.0, 89.0, 23.5, 44.5],
    'Total Viagens': [598, 715, 20, 1333, 259, 528]
}
df_domingos = pd.DataFrame(data_domingos).set_index('Unidade')

st.header('Resumo da Frota - Domingos e Feriados')
st.bar_chart(df_domingos[['Frota Média']])
st.bar_chart(df_domingos[['Total Viagens']])

# Você pode usar abas para organizar por dia da semana
tab1, tab2, tab3 = st.tabs(["Sábados", "Domingos", "Segunda a Quinta"])

with tab1:
    st.header("Dados de Sábados")
    # Insira o código com os dados de Sábados aqui...
    st.write("Exemplo de gráfico de barras para Sábados.")

    import streamlit as st
import pandas as pd

# Exemplo de dados (substitua pelos seus dados de fevereiro)
data_cumprimento = {
    'Dia': [1, 2, 3, 4, 5],
    'NÚCLEO 1': [99.66, 100.00, 99.50, 99.56, 99.89],
    'NÚCLEO 4': [99.41, 99.59, 99.60, 99.78, 99.83],
    'NÚCLEO 5': [94.48, 98.30, 99.12, 99.59, 99.73],
    'SOMA DOS NÚCLEOS': [98.24, 99.35, 99.42, 99.65, 99.82]
}
df_cumprimento = pd.DataFrame(data_cumprimento).set_index('Dia')

st.header('Fator de Cumprimento de Viagens - Janeiro a Agosto/2025')
st.line_chart(df_cumprimento[['NÚCLEO 1', 'NÚCLEO 4', 'NÚCLEO 5', 'SOMA DOS NÚCLEOS']])

import streamlit as st
import pandas as pd

# Exemplo de dados de atrasos mensais
data_atrasos_mensais = {
    'Mês': ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO'],
    'Total Atrasos': [203, 142, 113, 172, 129, 157, 128, 105]
}


import streamlit as st
import pandas as pd

# Exemplo de dados da linha 378TRO em um dia (dados parciais)
data_passageiros = {
    'Hora': ['04:40', '05:00', '05:30', '05:45', '06:00'],
    'Passageiros': [34, 30, 31, 45, 26]
}
df_passageiros = pd.DataFrame(data_passageiros).set_index('Hora')

st.header('Fluxo de Passageiros - Linha 378TRO')
st.line_chart(df_passageiros)