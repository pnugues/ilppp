import sys

[source, target] = sys.argv[1:]

length_s = len(source)
length_t = len(target)

# Initialize first row and column
table = [None] * (length_s + 1)

for i in range(length_s):
    table[i] = [None] * (length_t + 1)
    table[i][0] = i
for j in range(length_t):
    table[0][j] = j

# Get the characters. Start index is 0
source = list(source)
target = list(target)

# Fills the table. Start index of rows and columns is 1
for i in range(1, length_s):
    for j in range(1, length_t):
        # Is it a copy or a substitution?
        cost = 0 if source[i - 1] == target[j - 1] else 2
        # Computes the minimum
        minimum = table[i - 1][j - 1] + cost
        if minimum > table[i][j - 1] + 1:
            minimum = table[i][j - 1] + 1
        if minimum > table[i - 1][j] + 1:
            minimum = table[i - 1][j] + 1
        table[i][j] = minimum

for j in range(length_t):
    for i in range(length_s):
        print(table[i][j], " ", end='')
    print()

print("Minimum distance: ", table[length_s - 1][length_t - 1])
