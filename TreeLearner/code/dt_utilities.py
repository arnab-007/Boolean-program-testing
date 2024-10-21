import random

moves = [(1, 'hello', 'zalih'), (5, 'zauhar', {}), (2, [], 'pander'), (3, 100, []), (10, {}, {})]

# Set the seed for reproducibility
random.seed(42)

# Example list of tuples
x = 0
all_moves = []
while x < 5:
    moves.sort(key=lambda x: x[0], reverse=True)
    sampled_move = random.choice(moves)
    all_moves.append(sampled_move)
    x += 1

print(all_moves)