def get():
    return (1, '111')


x, y = get()

print(x, type(x))
print(y, type(y))

from datetime import datetime

d = datetime.now()
print(d.date())