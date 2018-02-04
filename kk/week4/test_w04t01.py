from week4.w04t01 import File

first = File(File.temp_path())
first.write('you shall\n')
second = File(File.temp_path())
second.write('not pass\n')
third = first + second
for line in third:
    print(line)
print(third)
