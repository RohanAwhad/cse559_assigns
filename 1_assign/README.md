Z-Algorithm for exact pattern matching
---
The algorithm for calculation of `z_array` is written in q1.py file, and it can be run using the following cmd:
```python3 q1.py samples/sample_0```
and it will create a "outputs" directory and save the output in a filenamed "sol_0"

The calulation proceeds in 0-based indexing, but while saving the solution indices, I add "1" to the output for 1-based indexing as specified in the question.

Also, for debugging purposes, I log important messages in "logs" file. We can checkout how the z-array is getting filled.
