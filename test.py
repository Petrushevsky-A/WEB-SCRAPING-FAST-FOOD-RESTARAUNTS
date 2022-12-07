def func():
    try:
        return True
        print(1)
    finally:
        return False

print(func())