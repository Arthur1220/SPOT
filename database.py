import sqlite3
import datetime

def initialize_database():
    """Inicializa o banco de dados e cria a tabela se não existir."""
    conn = sqlite3.connect('informacoes.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            peso REAL,
            area REAL,
            distancia REAL,
            data_hora TEXT,
            imagem_color BLOB,
            imagem_depth BLOB
        )
    ''')
    conn.commit()
    conn.close()

def salvar_informacoes(peso, distancia, area, imagem_color, imagem_depth):
    """
    Salva as informações no banco de dados.
    :param peso: Peso inserido pelo usuário.
    :param distancia: Distância medida pela câmera.
    :param area: Área calculada do objeto.
    :param imagem_color: Imagem colorida capturada.
    :param imagem_depth: Imagem de profundidade processada.
    """
    # Obtém a data e hora atual
    data_hora = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    
    conn = sqlite3.connect('informacoes.db')
    cursor = conn.cursor()
    
    # Armazena as imagens como BLOBs
    cursor.execute('''
        INSERT INTO registros (peso, area, distancia, data_hora, imagem_color, imagem_depth)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (peso, area, distancia, data_hora, imagem_color, imagem_depth))
    
    conn.commit()
    conn.close()
    
def fetch_all_records():
    """Recupera todos os registros do banco de dados."""
    conn = sqlite3.connect('informacoes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, peso, area, distancia, data_hora, imagem_color, imagem_depth FROM registros')
    records = cursor.fetchall()
    conn.close()
    return records