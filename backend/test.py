a = "ajmkm mdfm  rer"
number = [int(s) for s in a.split() if s.isdigit()]
if number:
    print(number)