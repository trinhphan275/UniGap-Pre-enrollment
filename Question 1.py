#### Trinh Phan
#### UniGap Pre-Enrollment Test

### Question 1:
import json
def def_word_cnt (input_string):
    result = dict()
    # put the string into lowercase and split it into words
    words = input_string.lower().split()

    # Count the words using a standard dictionary
    for word in words:
        if word in result:
            result[word] += 1
        else:
            result[word] = 1

    # Write the dictionary to a JSON file
    with open("result.json", "w") as json_file:
        json.dump(result, json_file, indent=4)

    return result
