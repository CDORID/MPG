input_var = input("What is the number of the match to scrap ? ")
print ("Adding match n° " + input_var + " to the list")
up_list = [1,2,3]
down_list = [2,3,4]
up_list.append(int(input_var)-1)
down_list.append(int(input_var))

print(up_list)
print(down_list)
