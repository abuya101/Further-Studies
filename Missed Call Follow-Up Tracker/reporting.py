import json

def save_summary(summary, filename):
    #Open the output file for writing. "w" creates the file, can also rewrite it
    with open(filename, "w", encoding="utf-8") as file:
        #convert the summary dictionary into jso then save it
        json.dump(summary, file, indent=4)