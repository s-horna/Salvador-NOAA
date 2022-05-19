with open("5222_41363_fixed_dates.hex") as f:
    length_list = []
    for line in f:
        if line[65:67] == "01":
            length_list.append(int(line[75:77], 16))
    print(length_list)

# Take median, mean, st. dev.. Check is mean is very diff. from mean. If value > 2-3 st.dev. from mean discard it.