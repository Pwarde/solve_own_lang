import string
from operator import eq, ge, gt, le, lt, ne
from typing import Callable


class MyLanguage:
    def __init__(self, program):
        self.program = program
        self.variables: dict[str, int] = {char: 0 for char in string.ascii_uppercase}
        self.print_list: list[int] = []
        self.goto_lookup: dict[str, int] = self.create_goto_lookup()

    def handle_line(self, idx):
        print(f"{idx=}")
        match self.program[idx].split(" "):
            case ["MOV", variable, value]:
                print(f"Set {variable=} to {value}")
                self.variables[variable] = self.get_value(value)
                return idx + 1
            case ["ADD", value1, value2]:
                print(f"Add {value2} to {value1}")
                self.variables[value1] = self.get_value(value1) + self.get_value(value2)
                return idx + 1
            case ["SUB", value1, value2]:
                print(f"Sub {value2} from {value1}")
                self.variables[value1] = self.get_value(value1) - self.get_value(value2)
                return idx + 1
            case ["MUL", value1, value2]:
                print(f"Multiply {value2} with {value1}")
                self.variables[value1] = self.get_value(value1) * self.get_value(value2)
                return idx + 1
            case ["JUMP", value]:
                print(f"Jump to {value}")
                return self.goto_lookup.get(value)
            case ["IF", lhs, operator, rhs, _, jump]:
                print(f"{lhs=}, {operator=}, {rhs=}, {jump=}")
                callable = self.get_operator(operator)
                print(f"{callable=}")
                if callable(self.get_value(lhs), self.get_value(rhs)):
                    print(f"Jump to {jump}")
                    return self.goto_lookup[jump]
                else:
                    print("Go to next line")
                    return idx + 1
            case ["PRINT", value]:
                print(f"Append {value} to print_list")
                self.print_list.append(self.get_value(value))
                return idx + 1
            case [value]:
                print(f"Set idx lookup for {value[:-1]}")
                self.goto_lookup[value[:-1]] = idx
                return idx + 1

    def get_value(self, value) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return self.variables.get(value)

    def get_operator(self, operator_string: str) -> Callable:
        print(operator_string)
        match operator_string:
            case "==":
                return eq
            case "!=":
                return ne
            case "<=":
                return le
            case "<":
                return lt
            case ">=":
                return ge
            case ">":
                return gt

    def create_goto_lookup(self):
        lookup = {
            value[:-1]: idx
            for idx, value in enumerate(self.program)
            if value.endswith(":")
        }
        print(lookup)
        return lookup


def run(program: list[str]) -> list[int]:
    my_lang = MyLanguage(program)
    idx = 0
    while idx < len(program):
        idx = my_lang.handle_line(idx)
    return my_lang.print_list


if __name__ == "__main__":
    program4 = []
    program4.append("MOV N 50")
    program4.append("PRINT 2")
    program4.append("MOV A 3")
    program4.append("begin:")
    program4.append("MOV B 2")
    program4.append("MOV Z 0")
    program4.append("test:")
    program4.append("MOV C B")
    program4.append("new:")
    program4.append("IF C == A JUMP error")
    program4.append("IF C > A JUMP over")
    program4.append("ADD C B")
    program4.append("JUMP new")
    program4.append("error:")
    program4.append("MOV Z 1")
    program4.append("JUMP over2")
    program4.append("over:")
    program4.append("ADD B 1")
    program4.append("IF B < A JUMP test")
    program4.append("over2:")
    program4.append("IF Z == 1 JUMP over3")
    program4.append("PRINT A")
    program4.append("over3:")
    program4.append("ADD A 1")
    program4.append("IF A <= N JUMP begin")
    result = run(program4)
    print(result)
