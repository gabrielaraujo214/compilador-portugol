class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def token_atual(self):
        return self.tokens[self.pos][0]

    def consumir(self, esperado):
        if self.token_atual() == esperado:
            self.pos += 1
        else:
            raise SyntaxError(f"Esperado {esperado}, encontrado {self.tokens[self.pos]}")

    def programa(self):
        while self.token_atual() != 'EOF':
            if self.token_atual() == 'TIPO':
                self.declaracao()
            else:
                self.comando()

    def declaracao(self):
        self.consumir('TIPO')
        self.consumir('ID')
        self.consumir(';')

    def comando(self):
        if self.token_atual() == 'ID':
            self.atribuicao()
        elif self.token_atual() == 'LEIA':
            self.leia()
        elif self.token_atual() == 'ESCREVA':
            self.escreva()
        elif self.token_atual() == 'SE':
            self.se()
        elif self.token_atual() == 'PARA':
            self.para()
        else:
            raise SyntaxError(f"Comando inválido: {self.tokens[self.pos]}")

    def atribuicao(self):
        self.consumir('ID')
        self.consumir('ATR')
        self.expressao()
        self.consumir(';')

    def leia(self):
        self.consumir('LEIA')
        self.consumir('PARAB')
        self.consumir('ID')
        self.consumir('PARFE')
        self.consumir(';')

    def escreva(self):
        self.consumir('ESCREVA')
        self.consumir('PARAB')
        if self.token_atual() in ['ID', 'STRING', 'NUMINT']:
            self.consumir(self.token_atual())
        else:
            raise SyntaxError("Erro em escreva: argumento inválido")
        self.consumir('PARFE')
        self.consumir(';')

    def se(self):
        self.consumir('SE')
        self.expressao_logica()
        self.consumir('ENTAO')
        while self.token_atual() not in ['SENAO', 'FIMSE']:
            self.comando()
        if self.token_atual() == 'SENAO':
            self.consumir('SENAO')
            while self.token_atual() != 'FIMSE':
                self.comando()
        self.consumir('FIMSE')

    def para(self):
        self.consumir('PARA')
        self.atribuicao()
        self.consumir('ATE')
        self.expressao()
        if self.token_atual() == 'PASSO':
            self.consumir('PASSO')
            self.consumir('NUMINT')
        while self.token_atual() != 'FIMPARA':
            self.comando()
        self.consumir('FIMPARA')

    def expressao(self):
        self.termo()
        while self.token_atual() in ['OPMAIS', 'OPMENOS']:
            self.consumir(self.token_atual())
            self.termo()

    def termo(self):
        self.fator()
        while self.token_atual() in ['OPMULTI', 'OPDIVI']:
            self.consumir(self.token_atual())
            self.fator()

    def fator(self):
        if self.token_atual() in ['ID', 'NUMINT']:
            self.consumir(self.token_atual())
        elif self.token_atual() == 'PARAB':
            self.consumir('PARAB')
            self.expressao()
            self.consumir('PARFE')
        else:
            raise SyntaxError(f"Fator inválido: {self.tokens[self.pos]}")

    def expressao_logica(self):
        self.expressao()
        if self.token_atual() in [
            'LOGIGUAL', 'LOGDIFF', 'LOGMAIOR',
            'LOGMENOR', 'LOGMAIORIGUAL', 'LOGMENORIGUAL']:
            self.consumir(self.token_atual())
        else:
            raise SyntaxError("Esperado operador lógico")
        self.expressao()
