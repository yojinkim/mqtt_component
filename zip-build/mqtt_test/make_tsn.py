import os

file_name ="ThingName"
with open(file_name, 'w') as file:
    file.write("PHM_test_0001")
    
os.system(f'cat {file_name}')