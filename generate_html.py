# generate_html.py
# This script reads a YAML file from a local path, extracts a message,
# and generates an HTML file from a template.

import sys
import yaml

def generate_page(yaml_path, template_path, output_path):
    """
    Reads a message from a local YAML file and generates an HTML page.

    Args:
        yaml_path (str): The local file path to the message.yaml file.
        template_path (str): The path to the local HTML template file.
        output_path (str): The path where the final index.html will be saved.
    """
    print(f"Reading YAML data from local file: {yaml_path}")

    # --- Step 1: Read and parse the local YAML file ---
    try:
        with open(yaml_path, 'r') as file:
            data = yaml.safe_load(file)
        
        message = data.get('message')
        if not message:
            print("Error: 'message' key not found in the YAML file.")
            sys.exit(1)
    except FileNotFoundError:
        print(f"Error: YAML file not found at '{yaml_path}'")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error: Could not parse the YAML file. {e}")
        sys.exit(1)

    print(f"Successfully parsed message: '{message}'")

    # --- Step 2: Read the HTML template ---
    try:
        with open(template_path, 'r') as f:
            template_content = f.read()
    except FileNotFoundError:
        print(f"Error: Template file not found at '{template_path}'")
        sys.exit(1)

    # --- Step 3: Replace the placeholder with the actual message ---
    final_html = template_content.replace('{{MESSAGE}}', message)

    # --- Step 4: Write the final HTML file ---
    try:
        with open(output_path, 'w') as f:
            f.write(final_html)
        print(f"Successfully generated HTML file at: {output_path}")
    except IOError as e:
        print(f"Error: Could not write the output file. {e}")
        sys.exit(1)


if __name__ == '__main__':
    # The script now expects local file paths
    if len(sys.argv) != 4:
        print("Usage: python generate_html.py <path_to_yaml> <path_to_template> <path_to_output>")
        sys.exit(1)

    local_yaml_path = sys.argv[1]
    html_template_path = sys.argv[2]
    output_html_path = sys.argv[3]

    generate_page(local_yaml_path, html_template_path, output_html_path)
