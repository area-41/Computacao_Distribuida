from Pyro5.api import Proxy


def main():
    obj_calc = Proxy("PYRONAME:calc")
    print("2 + 3 =", obj_calc.add(2, 3))
    print("10 - 4 =", obj_calc.sub(10, 4))
    print("6 * 7 =", obj_calc.mul(6, 7))
    print("20 / 5 =", obj_calc.div(20, 5))


if __name__ == "__main__":
    main()
