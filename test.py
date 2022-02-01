def f(a,b):
    return a+b

ma_liste = [1,2]
print(f(*ma_liste))

ma_dict = {"a":1, "c":2 }

print(f(**ma_dict))