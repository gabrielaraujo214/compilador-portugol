from analisador_lexico import executar_lexico
from analisador_semantico import AnalisadorSemantico

def main():
    try:
        tokens = executar_lexico('TESTE_COM_ERRO.POR', 'saida.TEM')
        analisador = AnalisadorSemantico(tokens)
        analisador.programa()
        print("Compilação concluída com sucesso.")
    except Exception as e:
        print(f"Erro durante a compilação: {e}")

if __name__ == '__main__':
    main()