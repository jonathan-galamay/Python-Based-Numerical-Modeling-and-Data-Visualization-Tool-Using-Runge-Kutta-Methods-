import numpy as np
import matplotlib.pyplot as plt
from math import sin, cos, exp, log, tan, sqrt, pi
import matplotlib as mpl

mpl.rcParams["font.family"] = "Times New Roman"

allowed_names = {
    "x": 0,
    "y": 0,
    "y0": 0,
    "sin": sin,
    "cos": cos,
    "tan": tan,
    "exp": exp,
    "log": log,
    "sqrt": sqrt,
    "pi": pi,
    "np": np,
}


def get_numeric_input(prompt):
    value = input(prompt).strip()
    try:
        return float(value)
    except ValueError:
        raise ValueError(f"Invalid numeric input: '{value}'")


while True:
    try:
        print("Runge-Kutta Methods First to Fourth Order")
        print("Choose a derivative function f(x,y).")
        print()
        print("Functions containing function of x:")
        print("1  - sin(x)")
        print("2  - cos(x)")
        print("3  - exp(x)")
        print("4  - log(x+1)")
        print("5  - x^2")
        print("6  - 1/(1+x^2)")
        print()
        print("Functions containing function of y:")
        print("7  - x + y")
        print("8  - y - x^2 + 1")
        print("9  - x*y")
        print("10 - sin(x) + y")
        print()
        print("11 - Custom function (user will enter f(x,y) and exact solution)")
        print()

        choice = input("Please enter your choice from 1 to 11: ").strip()

        step_size = get_numeric_input("Enter step size h: ")
        TotalX = get_numeric_input("Enter final x-value (number of iterations (n)): ")
        y0 = get_numeric_input("Enter initial value y(0): ")

        if step_size <= 0:
            raise ValueError("Step size must be positive.")
        if TotalX <= 0:
            raise ValueError("Final x-value must be positive.")

        allowed_names["y0"] = y0

        if choice == "1":
            func_name = "sin(x)"
            exact_name = "y0 + 1 - cos(x)"

            def f(x, y):
                return sin(x)

            def exact(x):
                return y0 + 1 - cos(x)

        elif choice == "2":
            func_name = "cos(x)"
            exact_name = "y0 + sin(x)"

            def f(x, y):
                return cos(x)

            def exact(x):
                return y0 + sin(x)

        elif choice == "3":
            func_name = "exp(x)"
            exact_name = "y0 + exp(x) - 1"

            def f(x, y):
                return exp(x)

            def exact(x):
                return y0 + exp(x) - 1

        elif choice == "4":
            func_name = "log(x+1)"
            exact_name = "y0 + (x+1)log(x+1) - x"

            def f(x, y):
                return log(x + 1)

            def exact(x):
                return y0 + ((x + 1) * log(x + 1) - x)

        elif choice == "5":
            func_name = "x^2"
            exact_name = "y0 + x^3/3"

            def f(x, y):
                return x**2

            def exact(x):
                return y0 + (x**3) / 3

        elif choice == "6":
            func_name = "1/(1+x^2)"
            exact_name = "y0 + arctan(x)"

            def f(x, y):
                return 1 / (1 + x**2)

            def exact(x):
                return y0 + np.arctan(x)

        elif choice == "7":
            func_name = "x + y"
            exact_name = "(y0 + 1)exp(x) - x - 1"

            def f(x, y):
                return x + y

            def exact(x):
                return (y0 + 1) * exp(x) - x - 1

        elif choice == "8":
            func_name = "y - x^2 + 1"
            exact_name = "x^2 + 2*x + 1 + (y0 - 1)exp(x)"

            def f(x, y):
                return y - x**2 + 1

            def exact(x):
                return x**2 + 2 * x + 1 + (y0 - 1) * exp(x)

        elif choice == "9":
            func_name = "x*y"
            exact_name = "y0 * exp(x^2 / 2)"

            def f(x, y):
                return x * y

            def exact(x):
                return y0 * exp((x**2) / 2)

        elif choice == "10":
            func_name = "sin(x) + y"
            exact_name = "(y0 + 1/2)exp(x) - (sin(x) + cos(x))/2"

            def f(x, y):
                return sin(x) + y

            def exact(x):
                return (y0 + 0.5) * exp(x) - 0.5 * (sin(x) + cos(x))

        elif choice == "11":
            func_name = input("Enter your custom derivative f(x,y): ").strip()
            exact_name = input("Enter the exact solution y(x): ").strip()

            def f(x, y):
                allowed_names["x"] = x
                allowed_names["y"] = y
                return eval(func_name, {"__builtins__": {}}, allowed_names)

            def exact(x):
                allowed_names["x"] = x
                return eval(exact_name, {"__builtins__": {}}, allowed_names)

            _ = f(0.5, y0)
            _ = exact(0.5)

        else:
            raise ValueError("Invalid menu choice.")

        _ = f(0.5, y0)
        _ = exact(0.5)

        print(f"\nSelected derivative: y' = {func_name}")
        print(f"Exact solution used in plot: {exact_name}")
        break

    except Exception as e:
        print("\nInvalid input or function detected.")
        print("Please start again from the first question.")
        print("Error:", e)
        print("-" * 50)


# Initial conditions
x = 0
y1_old = y0  # RK1 (Euler)
y2_old = y0  # RK2
y3_old = y0  # RK3
y4_old = y0  # RK4

x_vals = []
y1_vals = []
y2_vals = []
y3_vals = []
y4_vals = []
y_exact_vals = []

plt.ion()

fig, ax = plt.subplots(figsize=(16, 9))
plt.subplots_adjust(left=0.50)

ax.set_title(
    f"RK1 (Euler) vs RK2 vs RK3 vs RK4 vs Exact for y' = {func_name}",
    fontsize=20,
)
ax.set_xlabel("X", fontsize=15)
ax.set_ylabel("Y", fontsize=15)

line_rk1, = ax.plot([], [], "bo-", label="RK1 (Euler)")
line_rk2, = ax.plot([], [], "gs-", label="RK2")
line_rk3, = ax.plot([], [], "c^-", label="RK3")
line_rk4, = ax.plot([], [], "m*-", label="RK4")
line_exact, = ax.plot([], [], "r--", label="Exact Solution")

ax.set_xlim(0, TotalX)
ax.set_ylim(-10, 10)
ax.legend(fontsize=12)

while x <= TotalX:
    # RK1 (Euler)
    k1 = step_size * f(x, y1_old)
    y1 = y1_old + k1

    # RK2
    k1 = step_size * f(x, y2_old)
    k2 = step_size * f(x + step_size / 2, y2_old + k1 / 2)
    y2 = y2_old + k2

    # RK3
    k1 = step_size * f(x, y3_old)
    k2 = step_size * f(x + step_size / 2, y3_old + k1 / 2)
    k3 = step_size * f(x + step_size, y3_old - k1 + 2 * k2)
    y3 = y3_old + (k1 + 4 * k2 + k3) / 6

    # RK4
    k1 = step_size * f(x, y4_old)
    k2 = step_size * f(x + step_size / 2, y4_old + k1 / 2)
    k3 = step_size * f(x + step_size / 2, y4_old + k2 / 2)
    k4 = step_size * f(x + step_size, y4_old + k3)
    y4 = y4_old + (k1 + 2 * k2 + 2 * k3 + k4) / 6

    y_exact = exact(x)

    x_vals.append(x)
    y1_vals.append(y1)
    y2_vals.append(y2)
    y3_vals.append(y3)
    y4_vals.append(y4)
    y_exact_vals.append(y_exact)

    line_rk1.set_data(x_vals, y1_vals)
    line_rk2.set_data(x_vals, y2_vals)
    line_rk3.set_data(x_vals, y3_vals)
    line_rk4.set_data(x_vals, y4_vals)
    line_exact.set_data(x_vals, y_exact_vals)

    all_y = y1_vals + y2_vals + y3_vals + y4_vals + y_exact_vals
    y_min = min(all_y)
    y_max = max(all_y)

    if y_min == y_max:
        y_min -= 1
        y_max += 1

    ax.set_xlim(0, TotalX)
    ax.set_ylim(y_min - 1, y_max + 1)

    plt.draw()
    plt.pause(0.1)

    y1_old = y1
    y2_old = y2
    y3_old = y3
    y4_old = y4

    x += step_size

plt.ioff()
plt.show()
