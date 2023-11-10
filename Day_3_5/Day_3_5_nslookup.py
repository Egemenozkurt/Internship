import csv
import subprocess
from urllib.parse import urlparse
import socket

def get_nslookup_results(website):
    try:
        result = subprocess.run(['nslookup', website], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout
        error = result.stderr

        if error:
            print(f"Error executing nslookup for '{website}':")
            print(error)

            return "", "", ""
        else:
            # Extract authoritative answer, name, and IP address from the nslookup output
            authoritative_answer = ""
            name = ""
            ip_address = ""
            
            for line in output.splitlines():
                if "Name:" in line:
                    name = line.split(":")[1].strip()
                elif "Address:" in line:
                    ip_address = line.split(":")[1].strip()
                elif "Non-authoritative answer" in line:
                    authoritative_answer = "Non-authoritative"
                elif "Authoritative answer" in line:
                    authoritative_answer = "Authoritative"
            return name, ip_address, authoritative_answer 

    except Exception as e:
        print(f"An error occurred while executing nslookup for '{website}':")
        print(str(e))
        return "", "", ""

# Input CSV file
input_csv = "research1.csv"

# Output CSV file
output_csv = "nslookup_results2.csv"

with open(input_csv, mode='r', newline='') as file:
    reader = csv.DictReader(file, delimiter=';')  # Specify the delimiter used in the CSV

    results = []  # Store results

    for row in reader:
        url = row['URL']

        # Parse the URL to get the hostname
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname

        if hostname:
            # Get nslookup results
            auth_answer, domain_name, ip = get_nslookup_results(hostname)

            results.append([auth_answer, domain_name, ip])
        else:
            print(f"Invalid URL: '{url}'. Skipping...")

# Write the results to a CSV file
header = ["Domain Name", "IP Address", "Authoritative Answer"]

with open(output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(results)

print(f"Results written to {output_csv}.")
