# generate_html.py
# This script fetches a YAML file from a URL, extracts a message,
# and generates an HTML file from a template.

import sys
import requests
import yaml

def generate_page(yaml_url, template_path, output_path):
    """
    Fetches a message from a YAML file URL and generates an HTML page.

    Args:
        yaml_url (str): The raw URL to the message.yaml file in GitLab.
        template_path (str): The path to the local HTML template file.
        output_path (str): The path where the final index.html will be saved.
    """
    print(f"Fetching YAML data from: {yaml_url}")

    # --- Step 1: Fetch the YAML file from the GitLab URL ---
    try:
        response = requests.get(yaml_url)
        response.raise_for_status()  # Raises an exception for bad status codes (4xx or 5xx)
    except requests.exceptions.RequestException as e:
        print(f"Error: Could not fetch the YAML file from the URL. {e}")
        sys.exit(1)

    # --- Step 2: Parse the YAML content to get the message ---
    try:
        data = yaml.safe_load(response.text)
        message = data.get('message')
        if not message:
            print("Error: 'message' key not found in the YAML file.")
            sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error: Could not parse the YAML file. {e}")
        sys.exit(1)

    print(f"Successfully parsed message: '{message}'")

    # --- Step 3: Read the HTML template ---
    try:
        with open(template_path, 'r') as f:
            template_content = f.read()
    except FileNotFoundError:
        print(f"Error: Template file not found at '{template_path}'")
        sys.exit(1)

    # --- Step 4: Replace the placeholder with the actual message ---
    final_html = template_content.replace('{{MESSAGE}}', message)

    # --- Step 5: Write the final HTML file ---
    try:
        with open(output_path, 'w') as f:
            f.write(final_html)
        print(f"Successfully generated HTML file at: {output_path}")
    except IOError as e:
        print(f"Error: Could not write the output file. {e}")
        sys.exit(1)


if __name__ == '__main__':
    # The script expects three command-line arguments:
    # 1. The script name (e.g., generate_html.py)
    # 2. The URL to the raw YAML file.
    # 3. The path to the HTML template.
    # 4. The path for the output HTML file.
    if len(sys.argv) != 4:
        print("Usage: python generate_html.py <yaml_url> <template_path> <output_path>")
        sys.exit(1)

    gitlab_yaml_url = sys.argv[1]
    html_template_path = sys.argv[2]
    output_html_path = sys.argv[3]

    generate_page(gitlab_yaml_url, html_template_path, output_html_path)
