import datetime
import pandas as pd
from pathlib import Path
registros = []
def adicionar_registro(imagem_path, nome_planilha, localOcorrido):
    if not Path(nome_planilha).exists():
        df = pd.DataFrame(columns=[
            'data', 'hora', 'imagem', 'local'
        ])
        df.to_csv(nome_planilha, index=False)
        print(f" Planilha criada: {nome_planilha}")

    agora = datetime.datetime.now()
    registro = {
        'data': agora.strftime('%d/%m/%Y'),
        'hora': agora.strftime('%H:%M:%S'),
        'imagem': imagem_path,
        'local': localOcorrido
    }

    registros.append(registro)
    df = pd.DataFrame(registros)
    df.to_csv(nome_planilha, index=False, encoding='utf-8')
