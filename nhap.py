import numpy as np
arr = np.array([[1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]])

# Loại bỏ cột đầu tiên
arr_no_first_column = arr[:, 1:]
print(arr_no_first_column)