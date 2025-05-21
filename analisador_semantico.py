from analisador_sintatico import Parser

class AnalisadorSemantico(Parser):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.variaveis_declaradas = set()

    def declaracao(self):
        self.consumir('TIPO')
        nome_var = self.tokens[self.pos][1]
        if nome_var in self.variaveis_declaradas:
            raise RuntimeError(f"Variável '{nome_var}' já declarada.")
        self.consumir('ID')
        self.variaveis_declaradas.add(nome_var)

    def atribuicao(self):
        nome_var = self.tokens[self.pos][1]
        if nome_var not in self.variaveis_declaradas:
            raise RuntimeError(f"Variável '{nome_var}' usada sem declaração.")
        self.consumir('ID')
        self.consumir('ATR')
        self.expressao()

    def leia(self):
        self.consumir('LEIA')
        self.consumir('PARAB')
        nome_var = self.tokens[self.pos][1]
        if nome_var not in self.variaveis_declaradas:
            raise RuntimeError(f"Variável '{nome_var}' usada sem declaração em 'leia'.")
        self.consumir('ID')
        self.consumir('PARFE')

    def escreva(self):
        self.consumir('ESCREVA')
        self.consumir('PARAB')
        if self.token_atual() == 'ID':
            nome_var = self.tokens[self.pos][1]
            if nome_var not in self.variaveis_declaradas:
                raise RuntimeError(f"Variável '{nome_var}' usada sem declaração em 'escreva'.")
            self.consumir('ID')
        elif self.token_atual() in ['STRING', 'NUMINT']:
            self.consumir(self.token_atual())
        else:
            raise RuntimeError("Erro em escreva: argumento inválido.")
        self.consumir('PARFE')
