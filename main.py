import math
import matplotlib.pyplot as plt

# ========== CHANGE THE FOLLOWING ==========

# FUNCTION DEFINITION

# returns dy/dx given x and y
#def y_prime(x, y):
#  return math.cos(x)

def y_prime(x, y):
  return y

# change to the real function to test the values
#def y_check(x):
#  return math.sin(x)

def y_check(x):
  return math.pow(math.e, x)

# SCALE / DELTA X
delta_xs = [1, 0.5, 0.1, 0.05, 0.01, 0.001] # enter all the delta xs you want to test
end_x = 10

# CONSOLE PRINTING VARIABLES
print_rounding = 3 # how many decimal places to display
print_freq = 1 # how often to print updates

# ========== DON'T CHANGE THE FOLLOWING ==========

end_x = int(end_x)
end_x += min(delta_xs) # include both 0 and the final value

euler_method_table = {}

def round_x(num):
    return round(num, max(round(math.log(1 / min(delta_xs), 10)), 1))

def test_print_freq(x):
    return (x/print_freq % 1) == 0

def format_num(num, smallest, largest):
    # convert numbers to decimal/digit places
    decimal_places = int(math.log(1/smallest, 10))
    preceding_zeros = int(math.log(largest))

    return f"{num:.{decimal_places}f}".zfill(preceding_zeros + decimal_places)

for i in range(int(end_x / min(delta_xs))):
    x = round_x(i * min(delta_xs))

    if test_print_freq(x): # prints out x
        print(f"x = {format_num(x, print_freq, end_x)} : ", end="")

    for delta_x in delta_xs:
        if round_x(x/delta_x) % 1 == 0: # if the step fits into the x value
            # get y value from previous table entry and predict the new value with the slope of the previous
            try:
                y = euler_method_table[round_x(x-delta_x)][round_x(delta_x)]["y"]
                y += delta_x * y_prime(x, y)
            except KeyError as er: # if its the first value define it at 0
                y = y_check(0)

            # create/add to entry in the table
            try:
                euler_method_table[x]
            except KeyError as er:
                euler_method_table[x] = {}

            euler_method_table[x][delta_x] = {"y": y, "dy": y_prime(x, y)}
        else:
            nearest_decimal = round_x(math.floor(x/delta_x) * delta_x)

            try:
                euler_method_table[x]
            except KeyError as er:
                euler_method_table[x] = {}

            euler_method_table[x][delta_x] = {
                "y": euler_method_table[nearest_decimal][delta_x]["y"],
                "dy": euler_method_table[nearest_decimal][delta_x]["dy"]
            }

        # if the print frequency lines up then print out the state

        if test_print_freq(x):
            print(f"(delta = {delta_x}: {euler_method_table[x][delta_x]['y']:.{print_rounding}f}) ", end="")
    euler_method_table[x]["real_value"] = y_check(x)
    if test_print_freq(x):
        print(f"real : {euler_method_table[x]['real_value']:.{print_rounding}f}")

x_axis = list(euler_method_table.keys())
y_axes = {"actual_value": [euler_method_table[x]["real_value"] for x in x_axis]}

for delta_x in delta_xs:
    y_axes[delta_x] = [euler_method_table[x][delta_x]["y"] for x in list(euler_method_table.keys())]

for y_name in y_axes.keys():
    y_axis = y_axes[y_name]
    plt.plot(x_axis, y_axis, label=y_name)

plt.legend()
plt.show()