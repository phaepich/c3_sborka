import math

def dual_function(x, n):
    """
    Вариант 22 (7–4):
    Если x < n, используется левая функция: x - sqrt(x)
    Если x >= n, используется правая функция: 1/(x*x - 4) + sqrt(|x|)
    
    >>> dual_function(1, 2)
    0.0
    >>> dual_function(4, 3)  # doctest: +ELLIPSIS
    2.083333333333333...
    >>> [dual_function(x, 5) for x in [4.9, 5, 5.1]]  # doctest: +ELLIPSIS
    [2.686405637882135, 2.2836870251188373, 2.3037518518119318]
    >>> dual_function("aahahahaha", 2)
    Traceback (most recent call last):
    ...
    TypeError: '<' not supported between instances of 'str' and 'int'
    """
    if x < n:
        return x - math.sqrt(x)
    else:
        return 1/(x*x - 4) + math.sqrt(abs(x))

def plot_functions(n_values=(2, 5), x_range=(0.1, 10), num_points=100):
    import matplotlib.pyplot as plt
    import numpy as np
    
    x_vals = np.linspace(x_range[0], x_range[1], num_points)
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    for ax, n in zip(axes, n_values):
        y_vals = []
        for x in x_vals:
            try:
                y_vals.append(dual_function(x, n))
            except Exception:
                y_vals.append(float('nan'))
        ax.plot(x_vals, y_vals, label=f"dual_function(x, n={n})")
        ax.axvline(n, color='red', linestyle='--', label=f"x = n (n={n})")
        ax.set_title(f"График для n={n}")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.legend()
    
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    plot_functions()
