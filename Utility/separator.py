# Script used to create trasnlation tables. Very unclear code.
import csv
import json


def process_blocks():
    with open("raw_list.txt", "r") as file:
        file_content = file.read()
    curated_blocks = []
    file_blocks = file_content.split("\n")
    for file_block in file_blocks:
        length = len(file_block)
        index_1 = length - 2
        index_2 = length
        while file_block[index_1:index_2] != "  ":
            index_1 -= 1
            index_2 -= 1
        curated_blocks.append(file_block[index_2:])
    return curated_blocks


# Open a new CSV file in write mode
def csv_2(process_blocks):
    with open("curated_blocks.csv", "w", newline="") as csvfile:
        # Create a CSV writer object
        writer = csv.writer(csvfile)
        # Write each item from curated_blocks to a new row in the CSV file
        writer.writerow(["Pygame", "PyAutoGui"])
        for item in process_blocks():
            writer.writerow([item])


def dump_json():
    json_dict = {}
    with open("curated_blocks.csv", "r") as csv_file:
        for line in csv_file:
            line = line.replace("\n", "")
            json_dict[(line.split(",")[0])] = line.split(",")[1]
    with open("translated.json", "w") as json_file:
        json.dump(json_dict, json_file)


dump_json()
