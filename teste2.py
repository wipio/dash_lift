import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import numpy as np

# Número dinâmico
numero1 = st.number_input("Digite o primeiro número", value=0)

# Carregar a imagem
image = Image.open("Plano de Fundo.png")

# Criar um objeto de desenho
draw = ImageDraw.Draw(image)

# Carregar a fonte externa para o título (caso não tenha, pode usar uma fonte padrão)
font = ImageFont.truetype("arial.ttf", 50)  # Ajuste o caminho para a sua fonte ou use uma fonte padrão

# Adicionar o texto h1 sobre a imagem
text = f'{numero1}'
text_position = (90, 75)  # Posição do texto (ajuste conforme necessário)
draw.text(text_position, text, font=font, fill="black")

# Adicionar outros textos na imagem
text2 = "100,60"
text_position2 = (380, 75)  # Posição do texto (ajuste conforme necessário)
draw.text(text_position2, text2, font=font, fill="black")

text3 = "150,90"
text_position3 = (680, 75)  # Posição do texto (ajuste conforme necessário)
draw.text(text_position3, text3, font=font, fill="black")

text4 = "4"
text_position4 = (1050, 75)  # Posição do texto (ajuste conforme necessário)
draw.text(text_position4, text4, font=font, fill="black")

# Criar o gráfico com Matplotlib
fig, ax = plt.subplots(figsize=(4.5, 3.8))  # Tamanho do gráfico (em polegadas)
ax.bar([1, 2, 3], [4, 5, 6])

fig.patch.set_facecolor('none')  # Define o fundo do gráfico como transparente
ax.set_facecolor('none')  # Define o fundo do eixo como transparente


# Remover os eixos para que o gráfico tenha um fundo transparente
ax.axis('off')

# Salvar o gráfico como imagem
plt.tight_layout()
fig.canvas.draw()
graph_image = np.array(fig.canvas.renderer.buffer_rgba())

# Converter para PIL Image e redimensionar se necessário
graph_image = Image.fromarray(graph_image)

# Definir a posição do gráfico sobre a imagem
position = (30, 190)  # Ajuste conforme necessário

# Colocar o gráfico sobre a imagem
image.paste(graph_image, position, graph_image)

# Exibir a imagem com o gráfico sobreposto
st.image(image, use_container_width=True)
