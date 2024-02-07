import os

for f in os.listdir('piece_images/'):
    original = f
    f = f.replace('_2x_ns', '')
    if f.startswith('b'):
        f = 'black' + f[1:]
    else:
        f = 'white' + f[1:]

    os.rename('piece_images/' + original, 'piece_images/' + f)
