# HMM
To run:

```python3 test_HMM.py"```

It takes no arguments, to test on new mazes see comments within `test_HMM.py`

Output will look like this for each timestep:

```
time 0 -----------
square color: 0
sensor color: 0

robot location:
#.#.
....
.#..
A###

distribution:
[[0.  0.1 0.  0.1]
 [0.1 0.1 0.1 0.1]
 [0.1 0.  0.1 0.1]
 [0.1 0.  0.  0. ]]

smoothed distribution:
[[0.         0.00769203 0.         0.03997642]
 [0.08232761 0.04212038 0.04355323 0.03976207]
 [0.21174238 0.         0.00222788 0.03797574]
 [0.49262225 0.         0.         0.        ]]
```