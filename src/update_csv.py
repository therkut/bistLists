def update_csv(fetched_data, csv_file_path):
    import pandas as pd
    import os

    # Create 'data' directory if it doesn't exist
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)

    # Load existing data
    if os.path.exists(csv_file_path):
        try:
            existing_data = pd.read_csv(csv_file_path)
        except Exception as e:
            print(f"Error reading existing CSV file: {e}")
            existing_data = pd.DataFrame()
    else:
        existing_data = pd.DataFrame()

    # Convert new data to DataFrame
    new_data = pd.DataFrame(fetched_data)

    # Check for changes
    if existing_data.empty or not existing_data.equals(new_data):
        try:
            # Write new data to CSV
            new_data.to_csv(csv_file_path, index=False)
            print(f"CSV file '{csv_file_path}' updated successfully.")
        except Exception as e:
            print(f"Error writing to CSV file '{csv_file_path}': {e}")
    else:
        print(f"No changes detected. CSV file '{csv_file_path}' remains the same.")