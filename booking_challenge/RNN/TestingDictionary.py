import pickle

a_file = open("dictSamples", "rb")

output = pickle.load(a_file)

for key in output:
    print(key)

    print(output[key]["X"])

