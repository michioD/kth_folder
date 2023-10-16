#existense men inte entydighet
import numpy as np
import matplotlib.pyplot as plt
import time

def tic():
    return time.time()

def toc(start_time):
    end_time = time.time()
    return end_time - start_time

def y(x,c):
    if x>-c:
        return ((x+c)/2)**2
    else:
        return -((x+c)/2)**2

def f(x, y):
    return float(np.sqrt(abs(y)))

def euler(step_size, f, starty, startx, stopx):
    dx = step_size
    n = round(abs(stopx - startx) / dx)
    x = [startx]
    y = [starty]
    for k in range(n):
        next_x = x[-1]+dx
        next_y = y[-1]+dx*f(x[-1],y[-1])
        x.append(next_x)
        y.append(next_y)
    return x,y


def runge_kutta(step_size, f, start_y, start_x, stop_x):
    dx = step_size
    n = round(abs(stop_x - start_x) / dx)
    x = [start_x]
    y = [start_y]
    for i in range(n):
        if i == 0:
            continue
        k1 = dx* f(x[-1], y[-1])
        k2 = dx*f(x[-1] + 0.5*dx, y[-1] + 0.5*k1)
        k3 = dx *f(x[-1] + 0.5*dx, y[-1] + 0.5*k2)
        k4 = dx *f(x[-1] + dx, y[-1] + k3)
        next_y = y[-1] + (k1 + 2*k2 + 2*k3 + k4) / 6
        next_x = x[-1]+dx
        x.append(next_x)
        y.append(next_y)
    return x,y

x1, y1 = euler(0.011, f, -1, -1, 5)
def get_interval(x_values,y_values):
    n_steps = len(x_values)
    for i in range(1,n_steps):
        if y_values[i-1]<0 and y_values[i]>0:
            lower_bound = x_values[i-1]
            upper_bound = x_values[i]
            return lower_bound, upper_bound

def plot_interval_against_step_size():
    step_sizes = [2**(-i) for i in range(1,12)]
    interval_lengths = []
    for step_size in step_sizes:
        x_values, y_values = euler(step_size, f, -1, -1, 5)
        lower_bound, upper_bound = get_interval(x_values, y_values)
        interval_lengths.append(upper_bound - lower_bound)

    # Convert step sizes and interval lengths to logarithmic scale
    log_step_sizes = [np.log2(step) for step in step_sizes]
    log_interval_lengths = [np.log2(length) for length in interval_lengths]

    # Create a log-log plot
    plt.scatter(log_step_sizes, log_interval_lengths)
    plt.xlabel('Log Step Size (log2)')
    plt.ylabel('Log Interval Length (log2)')
    plt.show()
plot_interval_against_step_size()

# print(get_interval(x1,y1))

# plt.grid(True)
# plt.scatter(x1,y1, marker=".", label=r"numerisk lösning, $h=0.1$")
# plt.plot(x1,[y(np.array(x),-1) for x in x1],color="orange", label=r"analytisk lösning")
# plt.xlabel('x')
# plt.ylabel('y')
# plt.legend()
# plt.show()





