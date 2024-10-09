import csv
from datetime import datetime

f = open('./students.txt', 'rb')
students = {}
for line in f:
    line = line.decode('utf-8')
    students[line.strip()] = 'absent'
print(students)
f.close()

p = open('./presentees.txt', 'rb')
for line in p:
    line = line.decode('utf-8')
    students[line.strip()] = 'present'
print(students)
p.close()

current_date = datetime.now().strftime('%Y-%m-%d')
filename = f'{current_date}.csv'

with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    for name, status in students.items():
        writer.writerow([name, status])
