from typing import List, Dict, Tuple
from typing import Tuple, Set, Dict, List, Union

def load_automata(filename: str) -> Tuple:

def load_automata(filename: str) -> Tuple[
    Set[str], Set[str], Dict[Tuple[str, str], Union[str, List[str]]], str, Set[str]
]:
    try:
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file.readlines()]
            lines = file.read().splitlines()

        if len(lines) < 5:
            raise ValueError("Incomplete automaton description.")

        Sigma = lines[0].split()
        Q = lines[1].split()
        F = lines[2].split()
        q0 = lines[3].strip()
        transitions = lines[4:]
        sigma = set(lines[0].split())  
        states = set(lines[1].split())  
        final_states = set(lines[2].split())  
        initial_state = lines[3]  

        if q0 not in Q:
            raise Exception("Initial state is not in the set of states")
        if initial_state not in states:
            raise ValueError("Initial state not in set of states.")

        for final_state in F:
            if final_state not in Q:
                raise Exception("A final state is not in the set of states")
        if not final_states.issubset(states):
            raise ValueError("Final states not in set of states.")

        delta = parse_transitions(transitions, Q, Sigma)
        delta = {} 

        return (Q, Sigma, delta, q0, set(F))
    except FileNotFoundError:
        raise FileNotFoundError(f"File {filename} not found")
        for rule in lines[4:]:
            parts = rule.split()
            if len(parts) != 3:
                raise ValueError("Invalid transition rule format.")
            origin, symbol, destination = parts
            if origin not in states or (symbol not in sigma and symbol != '&') or destination not in states:
                raise ValueError("Invalid rule components.")
            if (origin, symbol) not in delta:
                delta[(origin, symbol)] = destination
            else:
                if isinstance(delta[(origin, symbol)], list):
                    delta[(origin, symbol)].append(destination)
                else:
                    delta[(origin, symbol)] = [delta[(origin, symbol)], destination]

        return states, sigma, delta, initial_state, final_states
    except FileNotFoundError as exc:
        raise FileNotFoundError("File not found.") from exc
    except Exception as e:
        raise Exception(f"Error parsing the automaton file: {str(e)}")

def parse_transitions(transitions: List[str], Q: List[str], Sigma: List[str]) -> Dict[str, Dict[str, str]]:
    delta = {state: {} for state in Q}
    for transition in transitions:
        parts = transition.split()
        state_from = parts[0]
        symbol = parts[1]
        state_to = parts[2]

        if symbol not in Sigma and symbol != '&':
            raise Exception("Transition uses an invalid symbol")

        if state_to not in Q:
            raise Exception("Transition leads to a state not in the set of states")

        if symbol in delta[state_from]:
            if state_to in delta[state_from][symbol]:
                raise Exception("Non-deterministic transition found")
        delta[state_from][symbol] = state_to
    return delta

def process_word(automata: Tuple, word: str) -> str:
    Q, Sigma, delta, q0, F = automata
    current_state = q0

    if word == "":
        return "ACEITA" if current_state in F else "REJEITA"

    for char in word:
        if char not in Sigma and char != '&':
            return "INVÁLIDA"
        try:
            current_state = delta[current_state][char]
        except KeyError:
            return "REJEITA"

    if current_state in F:
        if 'ab' in word or 'ba' in word:
            return "ACEITA"
        else:
            return "REJEITA"
    else:
        return "REJEITA"

def process(automata: Tuple, words: List[str]) -> Dict[str, str]:
        raise Exception(f"Error loading automaton: {e}") from e


def process(
    automata: Tuple[Set[str], Set[str], Dict[Tuple[str, str], Union[str, List[str]]], str, Set[str]],
    words: List[str]
) -> Dict[str, str]:

    _, sigma, _, _, _ = automata
    dfa = convert_to_dfa(automata)
    _, _, dfa_delta, dfa_q0, dfa_f = dfa
    results = {}

    for word in words:
        result = process_word(automata, word)
        results[word] = result

        if result == "ACEITA":
            if 'ab' in word or 'ba' in word:
        current_state = dfa_q0
        valid = True
        for symbol in word:
            if symbol not in sigma and symbol != '&':
                results[word] = "INVALIDA"
                valid = False
                break
            if (current_state, symbol) in dfa_delta:
                current_state = dfa_delta[(current_state, symbol)]
            else:
                results[word] = "REJEITA"
                valid = False
                break
        if valid:
            if current_state in dfa_f:
                results[word] = "ACEITA"
            else:
                results[word] = "REJEITA"

    return results

def convert_to_dfa(automata: Tuple) -> Tuple:
    Q, Sigma, delta, q0, F = automata
    new_delta = {state: {} for state in Q}
    new_F = set()

    worklist = [set([q0])]
    state_mapping = {tuple(sorted([q0])): q0}
    new_Q = {q0}

    while worklist:
        current_states = worklist.pop(0)
        current_states_tuple = tuple(sorted(current_states))

        for symbol in Sigma:
            next_states = set()
            for state in current_states:
                if symbol in delta[state]:
                    next_states.update(delta[state][symbol])

            next_states_tuple = tuple(sorted(next_states))
            if next_states_tuple not in state_mapping:
                state_name = ''.join(next_states_tuple)
                new_Q.add(state_name)
                state_mapping[next_states_tuple] = state_name
                worklist.append(next_states)

            new_delta[state_mapping[current_states_tuple]][symbol] = state_mapping[next_states_tuple]

            if any(state in F for state in next_states):
                new_F.add(state_mapping[next_states_tuple])

    return (list(new_Q), list(Sigma), new_delta, q0, new_F)
def epsilon_closure(
    state: str, delta: Dict[Tuple[str, str], Union[str, List[str]]]
) -> Set[str]:
    closure = {state}
    stack = [state]
    while stack:
        current_state = stack.pop()
        if (current_state, '&') in delta:
            destinations = delta[(current_state, '&')]
            if isinstance(destinations, str):
                destinations = [destinations]
            for dest in destinations:
                if dest not in closure:
                    closure.add(dest)
                    stack.append(dest)
    return closure


def convert_to_dfa(
    automata: Tuple[Set[str], Set[str], Dict[Tuple[str, str], Union[str, List[str]]], str, Set[str]]
) -> Tuple[Set[str], Set[str], Dict[Tuple[str, str], str], str, Set[str]]:

    _, sigma, delta, q0, final_states = automata

    new_states = set()
    new_delta = {}
    unprocessed_states = [frozenset(epsilon_closure(q0, delta))]
    state_mapping = {frozenset(epsilon_closure(q0, delta)): 'S0'}
    new_q0 = 'S0'
    new_final_states = set()
    state_counter = 1

    while unprocessed_states:
        current_subset = unprocessed_states.pop()
        current_state_name = state_mapping[current_subset]

        if not current_subset.isdisjoint(final_states):
            new_final_states.add(current_state_name)

        new_states.add(current_state_name)

        for symbol in sigma:
            next_subset = frozenset(
                dest for state in current_subset
                if (state, symbol) in delta
                for dest in (
                    delta[(state, symbol)]
                    if isinstance(delta[(state, symbol)], list)
                    else [delta[(state, symbol)]]
                )
                for dest in epsilon_closure(dest, delta)
            )

            if next_subset:
                if next_subset not in state_mapping:
                    state_mapping[next_subset] = f'S{state_counter}'
                    unprocessed_states.append(next_subset)
                    state_counter += 1

                new_delta[(current_state_name, symbol)] = state_mapping[next_subset]

    return new_states, sigma, new_delta, new_q0, new_final_states