import os
import json
import glob
import pandas as pd

def extract_modality_metadata_from_json(file_path):
    """Extract required metadata from a modality JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Initialize variables
        modality_info = {
            "id": "",
            "parents": [],
            "title": "",
            "acronyms": [],
            "shortDescription": "",
            "status": "complete",
            "prepared_by": "",
            "date_of_preparation": ""
        }
        
        # Extract metadata from the structured JSON
        for item in data:
            if item.get("level") == "meta-data-id":
                modality_info["id"] = item.get("content", "")
            elif item.get("level") == "meta-data-parents":
                modality_info["parents"] = item.get("content", [])
            elif item.get("level") == "meta-data-title":
                modality_info["title"] = item.get("content", "")
            elif item.get("level") == "meta-data-acronyms":
                # Filter out empty acronyms
                acronyms = [a for a in item.get("content", []) if a.strip()]
                modality_info["acronyms"] = acronyms
            elif item.get("level") == "meta-data-shortDescription":
                modality_info["shortDescription"] = item.get("content", "")
            elif item.get("level") == "prepration-meta-data-prepared_by":
                modality_info["prepared_by"] = item.get("content", "")
            elif item.get("level") == "prepration-meta-data-date_of_preparation":
                modality_info["date_of_preparation"] = item.get("content", "")
            elif item.get("level") == "prepration-meta-data-requires_completion" and item.get("content"):
                modality_info["status"] = f"in progress: {item.get('content')}"
        
        return modality_info
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def read_excel_and_create_data_json():
    """Read data from the Excel file and create data.json."""
    # Path to Excel file
    excel_path = os.path.join(os.path.dirname(__file__), 'SAFA - Datatypes.xlsx')
    
    # Path to data.json
    data_json_path = os.path.join(os.path.dirname(__file__), 'data.json')
    
    try:
        # Read the Excel file
        df = pd.read_excel(excel_path)
        
        # Prepare the data
        modality_data = []
        
        for _, row in df.iterrows():
            # Skip rows with empty or NaN id
            if pd.isna(row.get('id', '')) or str(row.get('id', '')).strip() == '':
                continue
                
            entry = {
                "id": str(row.get('id', '')).strip(),
                "parents": [p.strip() for p in str(row.get('parents', '')).split(',') if p.strip()],
                "title": str(row.get('title', '')).strip(),
                "acronyms": [a.strip() for a in str(row.get('acronyms', '')).split(',') if a.strip()],
                "shortDescription": str(row.get('shortDescription', '')).strip(),
                "prepared_by": str(row.get('prepared_by', '')).strip(),
                "status": str(row.get('status', '')).strip(),
                "date_of_preparation": str(row.get('date_of_preparation', '')).strip()
            }
            
            # Only add entries with a valid ID
            if entry["id"]:
                modality_data.append(entry)
        
        # Sort by id for consistency
        modality_data.sort(key=lambda x: x["id"])
        
        # Write to data.json
        with open(data_json_path, 'w', encoding='utf-8') as f:
            json.dump(modality_data, f, indent=2)
        
        print(f"Updated data.json with {len(modality_data)} modalities from Excel file")
        return modality_data
        
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return []

def update_data_json_from_modalities():
    """Update data.json by scanning all JSON files in the modalities folder."""
    # Path to modalities folder
    modalities_dir = os.path.join(os.path.dirname(__file__), 'modalities')
    
    # Path to data.json
    data_json_path = os.path.join(os.path.dirname(__file__), 'data.json')
    
    # Find all JSON files in the modalities folder
    json_files = glob.glob(os.path.join(modalities_dir, '*.json'))
    
    # Extract metadata from each file
    modality_data = []
    for file_path in json_files:
        metadata = extract_modality_metadata_from_json(file_path)
        if metadata:
            modality_data.append(metadata)
    
    # Sort by id for consistency
    modality_data.sort(key=lambda x: x["id"])
    
    # Write to data.json
    with open(data_json_path, 'w', encoding='utf-8') as f:
        json.dump(modality_data, f, indent=2)
    
    print(f"Updated data.json with {len(modality_data)} modalities from JSON files")
    return modality_data

def validate_json_compatibility():
    """Validate that JSON files in modalities folder match IDs in data.json."""
    # Path to modalities folder
    modalities_dir = os.path.join(os.path.dirname(__file__), 'modalities')
    
    # Path to data.json
    data_json_path = os.path.join(os.path.dirname(__file__), 'data.json')
    
    # Get all JSON files in the modalities folder
    json_files = glob.glob(os.path.join(modalities_dir, '*.json'))
    json_file_basenames = [os.path.splitext(os.path.basename(f))[0] for f in json_files]
    
    # Load data.json
    try:
        with open(data_json_path, 'r', encoding='utf-8') as f:
            data_json = json.load(f)
    except Exception as e:
        print(f"Error loading data.json: {e}")
        return
    
    # Extract IDs from data.json
    data_json_ids = [entry.get('id', '') for entry in data_json]
    
    # Check for files without corresponding ID
    correct_files = []
    json_files_without_id = []
    
    for filename in json_file_basenames:
        if filename in data_json_ids:
            correct_files.append(filename)
        else:
            json_files_without_id.append(filename)
    
    # Check for IDs without corresponding file
    ids_without_json = []
    
    for id_value in data_json_ids:
        if id_value not in json_file_basenames:
            ids_without_json.append(id_value)
    
    # Print results
    print(f"\nValidation Results:")
    print(f"Correct files with matching IDs: {len(correct_files)}")
    print(f"JSON files without matching ID in data.json: {len(json_files_without_id)}")
    print(f"IDs in data.json without matching JSON file: {len(ids_without_json)}")
    
    # Write results to check_summary.txt
    check_summary_path = os.path.join(os.path.dirname(__file__), 'check_summary.txt')
    
    with open(check_summary_path, 'w', encoding='utf-8') as f:
        f.write("=== CORRECT FILES WITH MATCHING IDS ===\n")
        for filename in sorted(correct_files):
            f.write(f"{filename}\n")
        
        f.write("\n=== JSON FILES WITHOUT MATCHING ID IN DATA.JSON ===\n")
        for filename in sorted(json_files_without_id):
            f.write(f"{filename}\n")
        
        f.write("\n=== IDS IN DATA.JSON WITHOUT MATCHING JSON FILE ===\n")
        for id_value in sorted(ids_without_json):
            f.write(f"{id_value}\n")
    
    print(f"Results written to check_summary.txt")

def main():
    """Main function to update data.json from Excel and validate JSON files."""
    print("1. Reading data from Excel file to create data.json...")
    excel_data = read_excel_and_create_data_json()
    
    if not excel_data:
        print("Falling back to reading from modality JSON files...")
        update_data_json_from_modalities()
    
    print("\n2. Validating JSON files in modalities folder...")
    validate_json_compatibility()

if __name__ == "__main__":
    main()
