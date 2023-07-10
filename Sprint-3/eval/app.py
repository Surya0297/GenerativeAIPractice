# Program to reverse a string

def reversedString(str):
    reverse=""
    for char in str:
        reverse=char+reverse
    return reverse

str =input("Enter String to be reversed:")
print(reversedString(str))
