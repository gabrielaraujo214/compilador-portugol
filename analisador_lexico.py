import re

# Palavras reservadas com e sem acento
tokens_especificos = {
    'ate': 'ATE', 'até': 'ATE',
    'entao': 'ENTAO', 'então': 'ENTAO',
    'escreva': 'ESCREVA',
    'fim_para': 'FIMPARA',
    'fim_se': 'FIMSE',
    'leia': 'LEIA',
    'nao': 'NAO', 'não': 'NAO',
    'ou': 'OU',
    'para': 'PARA',
    'passo': 'PASSO',
    'se': 'SE',
    'senao': 'SENAO', 'senão': 'SENAO',
    'inteiro': 'TIPO',
    'e': 'E'
}

operadores = {
    '<-': 'ATR', '<=': 'LOGMENORIGUAL', '>=': 'LOGMAIORIGUAL', '<>': 'LOGDIFF',
    '=': 'LOGIGUAL', '>': 'LOGMAIOR', '<': 'LOGMENOR', '+': 'OPMAIS',
    '-': 'OPMENOS', '*': 'OPMULTI', '/': 'OPDIVI', '(': 'PARAB',
    ')': 'PARFE', ':': 'DOIS_PONTOS'
}

operadores_ordenados = sorted(operadores.items(), key=lambda x: -len(x[0]))

# Regex para possíveis palavras (incluindo com acento) — deferimos a verificação para depois
token_specs = [
    ('POT_ID', r'[a-zA-ZáéíóúâêîôûãõçÁÉÍÓÚÂÊÎÔÛÃÕÇ_][a-zA-Z0-9áéíóúâêîôûãõçÁÉÍÓÚÂÊÎÔÛÃÕÇ_]*'),
    ('NUMINT', r'[0-9]+'),
    ('STRING', r'"[^"\n]*"'),
] + [(v, re.escape(k)) for k, v in operadores_ordenados] + [
    ('NEWLINE', r'\n'),
    ('SKIP', r'[ \t]+'),
    ('MISMATCH', r'.')
]

regex_compilada = '|'.join(f'(?P<{nome}>{regex})' for nome, regex in token_specs)

tabela_simbolos = {}

def verificar_palavra_reservada(lexema):
    return tokens_especificos.get(lexema.lower(), -1)

def executar_lexico(arquivo_entrada, arquivo_saida):
    tokens = []
    simbolo_index = 0

    with open(arquivo_entrada, 'r', encoding='utf-8') as f:
        codigo = f.read()

    for linha in codigo.splitlines():
        for match in re.finditer(regex_compilada, linha):
            tipo = match.lastgroup
            lexema = match.group()

            if tipo in ['NEWLINE', 'SKIP']:
                continue
            elif tipo == 'POT_ID':
                token = verificar_palavra_reservada(lexema)
                if token != -1:
                    tokens.append((token, lexema, '-'))
                else:
                    # Não é palavra reservada → então é identificador → rejeitar acento
                    if re.search(r'[^\x00-\x7F]', lexema):
                        raise RuntimeError(f"Identificador inválido (acentos não são permitidos): {lexema}")
                    token = 'ID'
                    if lexema not in tabela_simbolos:
                        tabela_simbolos[lexema] = simbolo_index
                        simbolo_index += 1
                    posicao = tabela_simbolos[lexema]
                    tokens.append((token, lexema, posicao))
            elif tipo in ['NUMINT', 'STRING']:
                tokens.append((tipo, lexema, '-'))
            elif tipo == 'MISMATCH':
                raise RuntimeError(f"Caractere inválido: {lexema}")
            else:
                tokens.append((tipo, lexema, '-'))

    tokens.append(('EOF', 'EOF', '-'))

    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        for t in tokens:
            f.write(f"{t[0]} {t[1]} {t[2]}\n")

    with open('tabela_simbolos.txt', 'w', encoding='utf-8') as f:
        for simbolo, idx in tabela_simbolos.items():
            f.write(f"{idx}: {simbolo}\n")

    return tokens