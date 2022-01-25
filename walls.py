wall = ''

for k in range(0, 20):
    wall += f'{k},10 '

for k in range(20, 28):
    wall += f'{k},20 '

print(wall[:-1])
