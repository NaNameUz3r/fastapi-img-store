import os
from pathlib import Path
import csv
import argparse
import requests
import glob
import sys

def upload_images(image_dir, csv_name, csv_delimiter, api_url):
    if not os.path.exists(image_dir):
        print(f"Error: '{image_dir}' directory not found.")
        return

    images = glob.glob(os.path.join(image_dir, "*"))

    results = []
    for image_path in images:
        with open(image_path, 'rb') as f:
            files = {"file": ('image.jpeg', f, 'multipart/form-data')}
            response = requests.post(api_url, files=files)

            if response.status_code == 201:
                data = response.json()
                image_id = data.get("ID")
                results.append((image_path, image_id))
                print(f"Uploaded '{image_path}' with ID: {image_id}")
            else:
                print(f"Failed to upload '{image_path}'. Status code: {response.status_code}")

    if results:
        with open(csv_name, "w", newline="") as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=csv_delimiter)
            csv_writer.writerow(["path_to_file", "id_from_server"])
            for path, image_id in results:
                csv_writer.writerow([path, image_id])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload images to server and generate CSV.")
    parser.add_argument("--image_dir", type=str, required=True, help="Path to the directory with images.")
    parser.add_argument("--csv_name", type=str, default="uploaded_images.csv", help="Name of the CSV file.")
    parser.add_argument("--csv_delimiter", type=str, default=";", help="Delimiter for the CSV file.")
    parser.add_argument("--api_url", type=str, default="http://127.0.0.1:8000/images/", help="Server API URL.")

    try:
        args = parser.parse_args()
    except argparse.ArgumentError as e:
        print("Error parsing arguments:", e)
        sys.exit(1)

    upload_images(args.image_dir, args.csv_name, args.csv_delimiter, args.api_url)