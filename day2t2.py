numbers=[10,25,30,35,40]
largest=numbers[0]
second_largest=numbers[0]
for num in numbers:
    if num > largest:
        second_largest=largest
        largest=num
    elif num != largest and num > second_largest:
       second_largest = num
print("first largest number is:",largest)
print("second_largest number is:",second_largest)