from django.test import TestCase

# Create your tests here.

nodes = []
for j in [0, 1]:
    if j == 0:
        for i in [0, 1]:
            nodes.append([i, j])
    else:
        for i in [1, 0]:
            nodes.append([i, j])
print(nodes)