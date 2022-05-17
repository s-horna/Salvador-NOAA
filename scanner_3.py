import datetime
from statistics import mode

# TODO: make code readable for software devs
# TODO: include profile lengths, determine if they're all 47. document for others to continue.

##################################################### READ DOC #####################################################


class Profile:
    def __init__(self, number=-1):
        self.dates = []
        self.lines = []
        self.first_message_lines = []
        self.number = number
        self.numbers = []

    def add_line(self, line):
        self.lines.append(line)
        if line.get_profile_num() != -1:
            self.first_message_lines.append(line)

    def add_first_line(self, line):
        self.lines.insert(0, line)

    def add_number(self, number):
        self.numbers.append(number)
        self.number = mode(self.numbers)

    def set_number(self, number):
        self.number = number

    def get_last_line(self):
        return self.lines[-1]

    def get_last_line(self):
        return self.lines[0]

    def get_last_date(self):
        return self.lines[-1].get_date()

    def get_first_date(self):
        return self.lines[0].get_date()

    def get_number(self):
        return self.number

    def get_num_messages(self):
        return len(self.numbers)

    def has_number(self, number):
        return number in self.numbers

    def get_lines_array(self):
        return self.lines

    def get_first_message_lines_array(self):
        return self.first_message_lines


class Line:
    def __init__(self, hex_line):

        self.hex_line = hex_line
        self.profile_num = "N/A"

        if hex_line.index(" ") == 6:
            self.line_date = datetime.datetime(
                year=int(hex_line[7:11]),
                month=int(hex_line[12:14]),
                day=int(hex_line[15:17]),
                hour=int(hex_line[18:20]),
                minute=int(hex_line[21:23]),
                second=int(hex_line[24:26])
            )
            self.message_num = hex_line[66:68]
            if self.message_num == "01":
                self.profile_num = hex_line[74:76]

        if hex_line.index(" ") == 5:
            self.line_date = datetime.datetime(
                year=int(hex_line[6:10]),
                month=int(hex_line[11:13]),
                day=int(hex_line[14:16]),
                hour=int(hex_line[17:19]),
                minute=int(hex_line[20:22]),
                second=int(hex_line[23:25])
            )
            self.message_num = hex_line[65:67]
            if self.message_num == "01":
                self.profile_num = hex_line[73:75]

    def get_date(self):
        return self.line_date

    def get_profile_num(self):
        if self.profile_num != "N/A":
            return int(self.profile_num, 16)
        else:
            return -1

    def get_string(self):
        return self.hex_line


all_lines = []
profiles = []


# open desired file, make sure file is in same directory and use file name here
with open("5222_41363_fixed_dates.hex") as f:
    for line in f:
        text_line = Line(line)
        all_lines.append(text_line)


profiles.append(Profile())
profiles[0].add_line(all_lines[0])
started_other_cycle = False

# load all profiles
for i in range(1, len(all_lines)):
    c = all_lines[i].get_date() - all_lines[i-1].get_date()
    days_diff = c.total_seconds() / 86400
    # may have to change number from 5 days to a smaller number (2,3) for certain floats that cycle faster than 10 days
    if days_diff > 5:
        profiles.append(Profile())
    profiles[-1].add_line(all_lines[i])


for profile in profiles:
    profile_array = profile.get_first_message_lines_array()
    if len(profile_array) > 1:
        for i in range(0, len(profile_array) - 1):
            if profile_array[i].get_profile_num() == 0 and profile_array[i+1].get_profile_num() == 0:
                started_other_cycle = True
            if started_other_cycle:
                if profile_array[i].get_profile_num() != -1:
                    profile.add_number(
                        profile_array[i].get_profile_num() + 256)
            else:
                if profile_array[i].get_profile_num() != -1:
                    profile.add_number(profile_array[i].get_profile_num())
            if i == len(profile_array) - 2:
                profile.add_number(profile_array[i+1].get_profile_num())
    if len(profile_array) == 1:
        profile.add_number(profile_array[0].get_profile_num())


continuous_profiles = []
continuous_profiles.append([])
continuous_profiles[0].append(profiles[0])

# get lists of continuous profiles
for i in range(1, len(profiles)):
    c = profiles[i].get_first_date() - profiles[i-1].get_last_date()
    days_diff = c.total_seconds() / 86400
    if days_diff > 15:
        continuous_profiles.append([])
    continuous_profiles[-1].append(profiles[i])


supposed_lists = []

# find progressive numbers index (at least 2) and create supposed lists
for continuous_list in continuous_profiles:
    length = len(continuous_list)
    index = -1
    start_progressive_number = -1
    i = 0
    while i < length - 3 and index == -1:
        print(str(continuous_list[i].get_number()))
        if continuous_list[i].get_number() + 1 == continuous_list[i+1].get_number() and continuous_list[i].get_number() + 2 == continuous_list[i+2].get_number():
            index = i
            start_progressive_number = continuous_list[i].get_number()
        i += 1
    supposed_lists.append([])
    if start_progressive_number != -1:
        starting_number = start_progressive_number - index
        supposed_lists[-1] = [x for x in range(
            starting_number, starting_number + length)]


# identify wrong profile numbers and match with actual profile numbers
compared_profiles = []
matched_wrong_profiles = []
wrong_number_index = -1

for i in range(0, len(supposed_lists)):
    supposed_list = supposed_lists[i]
    actual_list = continuous_profiles[i]
    if len(supposed_list) > 0:
        for j in range(0, len(supposed_list)):
            if actual_list[j].has_number(supposed_list[j]):
                compared_profiles.append(supposed_list[j])
            else:
                compared_profiles.append(wrong_number_index)
                matched_wrong_profiles.append(
                    [wrong_number_index, supposed_list[j]])
                wrong_number_index -= 1


missing_messages = 0
for profile_num in compared_profiles:
    if profile_num < 0:
        missing_messages += 1


for i in range(0, len(profiles)):
    profiles[i].set_number(compared_profiles[i])


profile_numbers = []
for profile in profiles:
    profile_numbers.append(profile.get_number())


print(str(matched_wrong_profiles))
print(str(profile_numbers))

##################################################### WRITE DOC #####################################################

# use desired file name for new file
new_file = open("5222_41363_new.hex", "w")

for profile in profiles:
    profile_lines = profile.get_lines_array()
    if profile.get_number() < 0:
        new_first_message_date = profile.get_first_date() - datetime.timedelta(seconds=1)
        test_line = profile_lines[0].get_string()
        new_first_line = ""
        true_hex_profile_number = None

        for list in matched_wrong_profiles:
            if list[0] == profile.get_number():
                true_deci_profile_number = list[1]
                if true_deci_profile_number > 255:
                    true_deci_profile_number = true_deci_profile_number - 256
                true_hex_profile_number = hex(
                    true_deci_profile_number).lstrip("0x").rstrip("L")

        if test_line.index(" ") == 6:
            new_first_line += test_line[0:7]
            new_first_line += new_first_message_date.strftime("%Y")
            new_first_line += " "
            new_first_line += new_first_message_date.strftime("%m")
            new_first_line += " "
            new_first_line += new_first_message_date.strftime("%d")
            new_first_line += " "
            new_first_line += new_first_message_date.strftime("%H")
            new_first_line += " "
            new_first_line += new_first_message_date.strftime("%M")
            new_first_line += " "
            new_first_line += new_first_message_date.strftime("%S")
            new_first_line += test_line[26:66]
            new_first_line += "01"
            new_first_line += test_line[68:74]
            new_first_line += str(true_hex_profile_number)
            new_first_line += "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00\n"

        if test_line.index(" ") == 5:
            new_first_line += test_line[0:6]
            new_first_line += new_first_message_date.strftime("%Y")
            new_first_line += " "
            new_first_line += new_first_message_date.strftime("%m")
            new_first_line += " "
            new_first_line += new_first_message_date.strftime("%d")
            new_first_line += " "
            new_first_line += new_first_message_date.strftime("%H")
            new_first_line += " "
            new_first_line += new_first_message_date.strftime("%M")
            new_first_line += " "
            new_first_line += new_first_message_date.strftime("%S")
            new_first_line += test_line[25:65]
            new_first_line += "01"
            new_first_line += test_line[67:73]
            new_first_line += str(true_hex_profile_number)
            new_first_line += "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00\n"

        profile.add_first_line(Line(new_first_line))

    profile_lines = profile.get_lines_array()
    for line in profile_lines:
        new_file.write(line.get_string())

new_file.close()
