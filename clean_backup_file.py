import json

def clean_backup_file(input_file, output_file):
    with open(input_file, 'r') as infile:
        data = json.load(infile)
    
    # Filter out the authtoken.Token entries
    cleaned_data = [entry for entry in data if entry['model'] != 'authtoken.token']
    
    with open(output_file, 'w') as outfile:
        json.dump(cleaned_data, outfile, indent=4)
    
    print(f"Cleaned data written to {output_file}")

# Specify your input and output file paths
input_file = 'db_backup.json'
output_file = 'cleaned_db_backup.json'

clean_backup_file(input_file, output_file)
