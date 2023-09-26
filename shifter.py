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

# Function to convert timestamp to milliseconds
def timestamp_to_milliseconds(timestamp):
    hours, minutes, seconds_milliseconds = timestamp.split(':')
    seconds, milliseconds = seconds_milliseconds.split(',')
    return int(hours) * 3600000 + int(minutes) * 60000 + int(seconds) * 1000 + int(milliseconds)

# Function to convert milliseconds to timestamp
def milliseconds_to_timestamp(milliseconds):
    hours, milliseconds = divmod(milliseconds, 3600000)
    minutes, milliseconds = divmod(milliseconds, 60000)
    seconds, milliseconds = divmod(milliseconds, 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

# Function to shift the timestamp
def shift_timestamp(timestamp, shift_ms):
    timestamp_ms = timestamp_to_milliseconds(timestamp)
    new_timestamp_ms = timestamp_ms + shift_ms
    if new_timestamp_ms < 0:
        return None  # Invalid shift, return None
    return milliseconds_to_timestamp(new_timestamp_ms)

def timestamp_shifter_by_subtitle_number(subtitle_number, individual_or_consecutive, choice_consecutive=0, milliseconds_consecutive=0, seconds_consecutive=0, minutes_consecutive=0, hours_consecutive=0):
    current_subtitle_string = ""

    for text in script_parsed_dictionary[str(subtitle_number)]:
        current_subtitle_string += text
        current_subtitle_string += "\n"

    print(f"\nCurrent subtitle ({subtitle_number}):\n")
    print(current_subtitle_string)

    start = current_subtitle_string.split()[0]
    end = current_subtitle_string.split()[2]

    print("Current start timestamp: " + start)
    print("Current end timestamp: " + end)

    if (individual_or_consecutive == 1):
        choice = int(input("\n1. Shift start\n2. Shift end\n3. Shift both start and end\n4. Exit\n\n"))

        while (choice < 1 or choice > 4):
            print("\nError, invalid choice!\n")
            choice = int(input("1. Shift start\n2. Shift end\n3. Shift both start and end\n4. Exit\n\n"))

        if (choice == 4):
            exit()

        milliseconds = int(input("\nShift by how many milliseconds? "))
        seconds = int(input("Shift by how many seconds? "))
        minutes = int(input("Shift by how many minutes? "))
        hours = int(input("Shift by how many hours? "))

    else:
        choice = choice_consecutive

        milliseconds = milliseconds_consecutive
        seconds = seconds_consecutive
        minutes = minutes_consecutive
        hours = hours_consecutive
        
    shift_values = [milliseconds, seconds, minutes, hours]
    
    shift_ms = 0
                    
    for value in range(len(shift_values)):
        if value == 0:
            shift_ms += shift_values[value]
        elif value == 1:
            shift_ms += shift_values[value] * 1000
        elif value == 2:
            shift_ms += shift_values[value] * 60000
        elif value == 3:
            shift_ms += shift_values[value] * 3600000

    if (choice == 1):
        new_start_timestamp = shift_timestamp(start, shift_ms)
        if new_start_timestamp:
            new_start_ms = timestamp_to_milliseconds(new_start_timestamp)
            end_ms = timestamp_to_milliseconds(end)
            if new_start_ms < end_ms:
                print(f"\nNew start timestamp: {new_start_timestamp}")
                new_timestamp = new_start_timestamp + " --> " + end
                script_parsed_dictionary[str(subtitle_number)][0] = new_timestamp
            else:
                print("\nInvalid shift or resulting start timestamp is equal to or later than the end timestamp.")
                exit()
        else:
            print("\nInvalid shift, resulting in a negative timestamp.")
            exit()
        
    if (choice == 2):
        new_end_timestamp = shift_timestamp(end, shift_ms)
        if new_end_timestamp:
            new_end_ms = timestamp_to_milliseconds(new_end_timestamp)
            start_ms = timestamp_to_milliseconds(start)
            if new_end_ms > start_ms:
                print(f"\nNew end timestamp: {new_end_timestamp}")
                new_timestamp = start + " --> " + new_end_timestamp
                script_parsed_dictionary[str(subtitle_number)][0] = new_timestamp
            else:
                print("\nInvalid shift or resulting end timestamp is equal to or earlier than the start timestamp.")
                exit()
        else:
            print("\nInvalid shift, resulting in a negative timestamp.")
            exit()

    if (choice == 3):
        new_start_timestamp = shift_timestamp(start, shift_ms)
        new_end_timestamp = shift_timestamp(end, shift_ms)
        if new_start_timestamp and new_end_timestamp:
            print(f"\nNew start timestamp: {new_start_timestamp}")
            print(f"New end timestamp: {new_end_timestamp}")
            new_timestamp = new_start_timestamp + " --> " + new_end_timestamp
            script_parsed_dictionary[str(subtitle_number)][0] = new_timestamp
        else:
            print("\nInvalid shift, resulting in a negative timestamp.")
            exit()

    new_subtitle_string = ""

    for text in script_parsed_dictionary[str(subtitle_number)]:
        new_subtitle_string += text
        new_subtitle_string += "\n"

    print(f"\nNew subtitle ({subtitle_number}):\n")
    print(new_subtitle_string[:-1])
                
if (choice == 1):
    subtitle_number = int(input("Select subtitle number\n\n"))

    while (subtitle_number < 1 or subtitle_number > len(script_parsed_dictionary)):
        print("\nError, invalid subtitle number!\n")
        subtitle_number = int(input("Select subtitle number\n\n"))

    timestamp_shifter_by_subtitle_number(subtitle_number, 1)

elif (choice == 2):
    subtitle_start_number = int(input("Select subtitle start number\n\n"))

    while (subtitle_start_number < 1 or subtitle_start_number >= len(script_parsed_dictionary)):
        print("\nError, invalid subtitle start number!\n")
        subtitle_start_number = int(input("Select subtitle start number\n\n"))

    subtitle_end_number = int(input("\nSelect subtitle end number\n\n"))

    while (subtitle_end_number <= subtitle_start_number or subtitle_end_number > len(script_parsed_dictionary)):
        print("\nError, invalid subtitle end number!\n")
        subtitle_end_number = int(input("Select subtitle end number\n\n"))

    individual_or_consecutive = int(input("\nDo you want the shift to be 1. individual (for each subtitle, something different) or 2. consecutive (for each subtitle, the same thing)?\n\n"))

    while (individual_or_consecutive < 1 or individual_or_consecutive > 2):
        print("\nError, invalid individual or consecutive choice!\n")
        individual_or_consecutive = int(input("Do you want the shift to be 1. individual (for each subtitle, something different) or 2. consecutive (for each subtitle, the same thing)?\n\n"))

    if (individual_or_consecutive == 1):
        for i in range(subtitle_start_number, subtitle_end_number + 1):
            timestamp_shifter_by_subtitle_number(i, individual_or_consecutive)
            
    else:
        choice = int(input("\n1. Shift start\n2. Shift end\n3. Shift both start and end\n4. Exit\n\n"))

        while (choice < 1 or choice > 4):
            print("\nError, invalid choice!\n")
            choice = int(input("1. Shift start\n2. Shift end\n3. Shift both start and end\n4. Exit\n\n"))

        if (choice == 4):
            exit()

        milliseconds = int(input("\nShift by how many milliseconds? "))
        seconds = int(input("Shift by how many seconds? "))
        minutes = int(input("Shift by how many minutes? "))
        hours = int(input("Shift by how many hours? "))

        for i in range(subtitle_start_number, subtitle_end_number + 1):
            timestamp_shifter_by_subtitle_number(i, individual_or_consecutive, choice, milliseconds, seconds, minutes, hours)

elif (choice == 3):
    individual_or_consecutive = int(input("Do you want the shift to be 1. individual (for each subtitle, something different) or 2. consecutive (for each subtitle, the same thing)?\n\n"))

    while (individual_or_consecutive < 1 or individual_or_consecutive > 2):
        print("\nError, invalid individual or consecutive choice!\n")
        individual_or_consecutive = int(input("Do you want the shift to be 1. individual (for each subtitle, something different) or 2. consecutive (for each subtitle, the same thing)?\n\n"))

    if (individual_or_consecutive == 1):
        for i in range(1, len(script_parsed_dictionary) + 1):
            timestamp_shifter_by_subtitle_number(i, individual_or_consecutive)
            
    else:
        choice = int(input("\n1. Shift start\n2. Shift end\n3. Shift both start and end\n4. Exit\n\n"))

        while (choice < 1 or choice > 4):
            print("\nError, invalid choice!\n")
            choice = int(input("1. Shift start\n2. Shift end\n3. Shift both start and end\n4. Exit\n\n"))

        if (choice == 4):
            exit()

        milliseconds = int(input("\nShift by how many milliseconds? "))
        seconds = int(input("Shift by how many seconds? "))
        minutes = int(input("Shift by how many minutes? "))
        hours = int(input("Shift by how many hours? "))

        for i in range(1, len(script_parsed_dictionary) + 1):
            timestamp_shifter_by_subtitle_number(i, individual_or_consecutive, choice, milliseconds, seconds, minutes, hours)

output_file_name = "output.srt"
f = open(output_file_name, "w")

count = 0

for key_value_pair in script_parsed_dictionary.items():
    f.write(key_value_pair[0])
    f.write("\n")
    for text in key_value_pair[1]:
        f.write(text)
        
        # No first extra \n at thess end of the file
        if (count + 1 != len(script_parsed_dictionary) or text != key_value_pair[1][-1]):
            f.write("\n")

    # No second extra \n at the end of the file     
    if (count + 1 != len(script_parsed_dictionary)):
        f.write("\n")

    count += 1

f.close()
