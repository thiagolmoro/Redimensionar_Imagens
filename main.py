# pip install pillow

import os
from PIL import Image, ImageEnhance

def redimensionar_imagens(pasta_origem, pasta_destino):
    """
    Redimensiona todas as imagens em uma pasta, alterando o tamanho baseado na largura e melhorando a qualidade.

    Args:
        pasta_origem (str): Caminho para a pasta contendo as imagens originais.
        pasta_destino (str): Caminho para a pasta onde as imagens redimensionadas serão salvas.
    """
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    # Iterar sobre os arquivos na pasta de origem
    for arquivo in os.listdir(pasta_origem):
        caminho_arquivo = os.path.join(pasta_origem, arquivo)

        # Verificar se é um arquivo de imagem
        if not os.path.isfile(caminho_arquivo):
            continue
        try:
            with Image.open(caminho_arquivo) as img:
                # Obter dimensões da imagem
                largura, altura = img.size

                # Determinar o fator de redimensionamento com base na largura
                if altura < 400:
                    fator = 2.1                
                elif altura > 400 and altura < 430:
                    fator = 1.9
                elif altura > 430 and altura < 460:
                    fator = 1.6
                else:
                    fator = 1.4

                # Calcular novas dimensões
                nova_largura, nova_altura = int(largura * fator), int(altura * fator)
                img_redimensionada = img.resize((nova_largura, nova_altura), Image.Resampling.LANCZOS)

                # Melhorar a qualidade da imagem
                enhancer = ImageEnhance.Sharpness(img_redimensionada)
                img_aprimorada = enhancer.enhance(2.0)  # Ajuste de nitidez

                # Salvar a nova imagem na pasta de destino
                nome_destino = os.path.join(pasta_destino, arquivo)
                img_aprimorada.save(nome_destino, quality=95)  # Salvar com qualidade alta
                print(f"Imagem redimensionada e salva: {nome_destino}")
        except Exception as e:
            print(f"Erro ao processar {arquivo}: {e}")

def process_images(image_folder, background_path, output_folder):
    """
    Processa imagens redimensionadas e as combina com um fundo branco.

    Args:
        image_folder (str): Caminho para a pasta contendo as imagens redimensionadas.
        background_path (str): Caminho para a imagem de fundo.
        output_folder (str): Caminho para a pasta onde as imagens combinadas serão salvas.
    """
    # Certifique-se de que as pastas existem
    if not os.path.exists(image_folder):
        raise FileNotFoundError(f"A pasta de imagens {image_folder} não foi encontrada.")

    if not os.path.exists(background_path):
        raise FileNotFoundError(f"A imagem de fundo {background_path} não foi encontrada.")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Carregar o fundo branco
    background = Image.open(background_path)
    bg_width, bg_height = background.size

    # Listar todas as imagens na pasta
    images = [f for f in os.listdir(image_folder) if f.lower().endswith(('png', 'jpg', 'jpeg'))]

    if not images:
        raise ValueError("Nenhuma imagem encontrada na pasta especificada.")

    # Processar cada imagem
    for index, image_name in enumerate(sorted(images), start=1):
        image_path = os.path.join(image_folder, image_name)
        img = Image.open(image_path)

        # Redimensionar ou manter as dimensões originais
        img_width, img_height = img.size

        # Centralizar a imagem no fundo branco
        offset_x = (bg_width - img_width) // 2
        offset_y = (bg_height - img_height) // 2

        # Criar uma cópia do fundo e colar a imagem no centro
        combined = background.copy()
        combined.paste(img, (offset_x, offset_y), mask=img if img.mode == 'RGBA' else None)

        # Salvar a nova imagem
        output_path = os.path.join(output_folder, f"{index:02d}.png")
        combined.save(output_path)

        print(f"Imagem processada e salva em: {output_path}")

# Definir os caminhos
caminho_padrao = "D:/Google Drive - Trader/0 - Resultado dos Clientes para os Storys"
caminho_data = "/Resultados Semana 2025.01.20 a 2025.01.24"
caminho_data_originais_e_redimensionada = "/05 - 20 a 24 de Janeiro de 2025"

pasta_origem = caminho_padrao + "/Imagens Originais" + caminho_data_originais_e_redimensionada
pasta_redimensionada = caminho_padrao + "/Imagens Redimensionadas" + caminho_data_originais_e_redimensionada
background_path = "D:/Google Drive - Trader/0 - Resultado dos Clientes para os Storys/Fundo - Branco.png"
pasta_saida = caminho_padrao + caminho_data

# Executar as funções
redimensionar_imagens(pasta_origem, pasta_redimensionada)
process_images(pasta_redimensionada, background_path, pasta_saida)
