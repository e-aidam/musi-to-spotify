import csv 

#creates playlist array from csv
def csv_to_array(file_path):
    data_array = []
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            data_array.append(row)
    return data_array

csv_file_path = 'results_item_eyes.csv'
csv_data_array = csv_to_array(csv_file_path)

# Extracting track names and artists separately
track_names = [row[0] for row in csv_data_array[1:]]
artists = [row[1] for row in csv_data_array[1:]]

# Combining track names and artists into a list of dictionaries
source_playlist = [{"track_name": track_name, "artist": artist} for track_name, artist in zip(track_names, artists)]
print(source_playlist)