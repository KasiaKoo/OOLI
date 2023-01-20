from instrument_control.stage import *
print('import is done')


iris = Stage("Iris").initiate()

print(iris.get_position())

while True:
    s = input('Enter New Position')
    iris.set_position(s)
    
