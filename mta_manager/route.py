from enum import Enum

class Route(Enum):
    A = "A"
    C = "C"
    E = "E"

    B = "B"
    D = "D"
    F = "F"
    M = "M"

    G = "G"

    J = "J"
    Z = "Z"

    N = "N"
    Q = "Q"
    R = "R"
    W = "W"

    N1 = "1"
    N2 = "2"
    N3 = "3"
    N4 = "4"
    N5 = "5"
    N6 = "6"
    N7 = "7"

    L = "L"
    SIR = "SIR"

_routes = set(item.value for item in Route)
def is_valid_route(route: str) -> bool:
    return route in _routes