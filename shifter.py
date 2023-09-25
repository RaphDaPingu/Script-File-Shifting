import re

input_file_name = "sample.srt"
script_parsed_dictionary = {}

with open(input_file_name) as f:
    lines = f.readlines()

current_key = 0
current_value = []

for line in lines:
    line = line.strip()
    if re.match(r'^\d+$', line): # Check if line is a subtitle number
        if current_key is not 0:
            script_parsed_dictionary[current_key] = current_value
        current_key = line
        current_value = []
    elif re.match(r'^\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+$', line): # Check if line is a time range
        current_value.append(line)
    elif line: # Check if line is not empty
        current_value.append(line)

# Add the last subtitle
script_parsed_dictionary[current_key] = current_value

choice = 0

while True:
    choice = int(input("What would you like to do?\n1. Edit single subtitle\n2. Edit range of subtitles\n3. Edit all subtitles\n4. Exit\n\n"))

    if (choice < 1 or choice > 4):
        print("\nError, invalid choice!\n")

    if (choice == 4):
        exit()

    if (choice >= 1 and choice <= 3):
        break

print()

for key_value_pair in script_parsed_dictionary.items():
    print(key_value_pair)

print()

if (choice == 1):
    subtitle_number = int(input("Select subtitle number\n\n"))

    while (subtitle_number < 1 or subtitle_number > len(script_parsed_dictionary)):
        print("\nError, invalid subtitle number!\n")
        subtitle_number = int(input("Select subtitle number\n\n"))

    subtitle_string = ""

    for text in script_parsed_dictionary[str(subtitle_number)]:
        subtitle_string += text
        subtitle_string += "\n"

    print("\nYou selected this subtitle:\n")
    print(subtitle_string)

    start = subtitle_string.split()[0]
    end = subtitle_string.split()[2]

    print("Start: " + start)
    print("End: " + end)

    choice = int(input("\n1. Shift start\n2. Shift end3. Exit\n\n"))

    if (choice == 3):
        exit()
    
    while (choice < 1 or choice > 2):
        print("\nError, invalid choice!\n")
        num = int(input("1. Shift start\n2. Shift end\n\n"))

    milliseconds = int(input("\nShift by how many milliseconds?"))
    seconds = int(input("\nShift by how many seconds?"))
    minutes = int(input("\nShift by how many minutes?"))
    hours = int(input("\nShift by how many hours?"))

    if (choice == 1):
        pass
    if (choice == 2):
        pass

elif (choice == 2):
    pass

elif (choice == 3):
    pass

output_file_name = "output.srt"
f = open(output_file_name, "w")

count = 0

for key_value_pair in script_parsed_dictionary.items():
    f.write(key_value_pair[0])
    f.write("\n")
    for text in key_value_pair[1]:
        f.write(text)
        
        # No first extra \n at the end of the file
        if (count + 1 != len(script_parsed_dictionary) or text != key_value_pair[1][-1]):
            f.write("\n")

    # No second extra \n at the end of the file     
    if (count + 1 != len(script_parsed_dictionary)):
        f.write("\n")

    count += 1

f.close()
