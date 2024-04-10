import pickle

# Create a dictionary
data = {
    "name": "John",
    "age": 30,
    "city": "New York"
}

# Save the dictionary to a file
with open("data.pickle", "wb") as file:
    pickle.dump(data, file)

# Read the dictionary back from the file
with open("data.pickle", "rb") as file:
    loaded_data = pickle.load(file)

# Print the loaded dictionary
print("Loaded data:", loaded_data)
