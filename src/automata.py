
from typing import List, Dict, Tuple

def load_automata(filename: str) -> Tuple[List[str], List[str], List[Tuple[str, str, str]], str, List[str]]:
    with open(filename, 'r') as file:
        lines = file.readlines()

    alfabeto = lines[0].strip().split()
    estados = lines[1].strip().split()
    estados_finais = lines[2].strip().split()
    estado_inicial = lines[3].strip()
    transicoes = []

    for line in lines[4:]:
        partes = line.strip().split()
        if len(partes) != 3:
            raise Exception(f"Formato de transição inválido: {line}")
        transicoes.append((partes[0], partes[1], partes[2]))

    return alfabeto, estados, transicoes, estado_inicial, estados_finais

def process(automato: Tuple[List[str], List[str], List[Tuple[str, str, str]], str, List[str]], palavras: List[str]) -> Dict[str, str]:
    alfabeto, estados, delta, estado_inicial, estados_finais = automato
    resultado = {}

    def fecho_epsilon(estado, visitados):
        visitados.add(estado)
        fecho = set()
        fecho.add(estado)
        for transicao in delta:
            if transicao[0] == estado and transicao[1] == '&' and transicao[2] not in visitados:
                fecho |= fecho_epsilon(transicao[2], visitados)
        return fecho

    def transicao(estados, simbolo):
        proximos_estados = set()
        for estado in estados:
            for transicao in delta:
                if transicao[0] == estado and transicao[1] == simbolo:
                    proximos_estados.add(transicao[2])
        return proximos_estados

    for palavra in palavras:
        estados_atuais = fecho_epsilon(estado_inicial, set())
        palavra_valida = True

        for simbolo in palavra:
            if simbolo not in alfabeto:
                resultado[palavra] = 'INVÁLIDA'
                palavra_valida = False
                break
            estados_atuais = fecho_epsilon(transicao(estados_atuais, simbolo), set())

        if palavra_valida and any(estado in estados_finais for estado in estados_atuais):
            resultado[palavra] = 'ACEITA'
        elif palavra_valida:
            resultado[palavra] = 'REJEITA'

    return resultado

def convert_to_dfa(automato: Tuple[List[str], List[str], List[Tuple[str, str, str]], str, List[str]]) -> Tuple[List[str], List[str], List[Tuple[str, str, str]], str, List[str]]:
    
    pass



import unittest
from automata import load_automata, process, convert_to_dfa

class TestFuncoesAutomato(unittest.TestCase):

    def test_load_automata(self):
        filename = 'exemplo_automato.txt' 
        automato = load_automata(filename)
        self.assertIsInstance(automato, tuple)
      

    def test_process(self):
        automato = (['a', 'b'], ['q0', 'q1', 'q2', 'q4'], [('q0', 'a', 'q0'), ('q0', 'b', 'q0'), ('q0', '&', 'q1'),
                                                           ('q1', 'a', 'q2'), ('q2', 'a', 'q3'), ('q2', 'b', 'q3'),
                                                           ('q3', 'a', 'q4'), ('q3', 'b', 'q4')],
                    'q0', ['q4'])
        palavras = ['ab', 'ba', 'aaa', '']
        resultados = process(automato, palavras)
        self.assertEqual(resultados['ab'], 'REJEITA')
      

    def test_convert_to_dfa(self):
        automato = (['a', 'b'], ['q0', 'q1', 'q2', 'q4'], [('q0', 'a', 'q0'), ('q0', 'b', 'q0'), ('q0', '&', 'q1'),
                                                           ('q1', 'a', 'q2'), ('q2', 'a', 'q3'), ('q2', 'b', 'q3'),
                                                           ('q3', 'a', 'q4'), ('q3', 'b', 'q4')],
                    'q0', ['q4'])
        automato_dfa = convert_to_dfa(automato)
     

if __name__ == '__main__':
    unittest.main()
