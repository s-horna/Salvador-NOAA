n = open("5222_41363_fixed_dates.hex", "w")

with open("5222_41363.hex") as f:
    for line in f:
        minute = int(line[20:22])
        second = int(line[23:25])
        if second > 59:
            n.write(line[0:20] + "%02d" % (minute + 1) +
                    " " + "%02d" % (second - 60) + line[25:-1])
            n.write("\n")
        else:
            n.write(line)
            # n.write("\n")

# with open("3508_95256.hex") as f:
#     for line in f:
#         minute = int(line[20:22])
#         second = int(line[23:25])
#         if second > 59:
#             print(line)
        #     n.write(line[0:20] + "%02d" % (minute + 1) +
        #             " " + "%02d" % (second - 60) + line[25:-1])
        #     n.write("\n")
        # else:
        #     n.write(line)
        #     # n.write("\n")

n.close()
