# DataTypeHub

[![DataTypeHub](https://img.shields.io/badge/Visit-DataTypeHub-blue?style=for-the-badge)](https://project-pars-peace.github.io/DataTypeHub)

Welcome to the **DataTypeHub** repository! DataTypeHub is a centralized resource showcasing diverse medical data modalities, with each modality card  describing best practices for streamlined data ingestion.

---
# Guide for Contributors
Below is a  guide that explains how you should send us your contributions:
	•	Add team info to team.json
	•	Add brief info to data.json
	•	Add full info in the correct modalities/<id>.json file

## 1. Team Information

Our **team page** (`team.html`) displays profiles from `team.json`. To add a new team member:

1. Open `team.json`.
2. Append a new JSON object with the following fields:
   ```json
   {
     "name": "Dr. Alice Johnson",
     "contributedTo": ["Mammography", "XRay_DR"], 
     "email": "alice@example.com",
     "affiliation": "Example University",
     "image": "images/alice.jpg"
   }
   ```

•	name: Full name.
•	contributedTo: List of modalities the member worked on (e.g., ["Mammography", "PET"]).
•	email: Their preferred contact email address.
•	affiliation: University, institution, or organization.
•	image (optional): Path to an image in docs/images/. If no image is provided, leave this field empty (e.g., "").

Important: Make sure each new object is separated by a comma (if you’re adding multiple members) and that the JSON syntax remains valid (no trailing commas, matching brackets, etc.).

## 2. Guide to adding a new modality

You should enter the information of the modality into this graphical interface created for adding a new modality. You should download the JSON file (it will automatically name the file as the modality ID) and upload it to this location: docs/modalities/

Link to JSON-generator interface: https://project-pars-peace-json-generator.streamlit.app/

<details>
	<summary>Previous deprecated guide to add data modality files </summary>


## 2.1. Brief Info for a adding a New Modality

We maintain data.json as the main reference for all modalities. Each entry here briefly describes the modality and includes:
	•	id (unique string, also used for the JSON file name in modalities/)
	•	parents (an array of parent categories, e.g., ["X-Ray"] or ["MRI"])
	•	title (the user-facing title)
	•	acronyms (array of strings for abbreviations, if any)
	•	shortDescription (a short summary or highlight)
	•	status (the publication status, e.g. "Published" or "Planned")

A minimal object might look like:
```json
{
  "id": "functional_mri",
  "parents": ["MRI"],
  "title": "Functional MRI (fMRI)",
  "acronyms": ["fMRI"],
  "shortDescription": "Captures changes in blood oxygen to map brain activity.",
  "status": "Published"
}
```

To add a new modality:
	1.	Open data.json.
	2.	Insert a new object inside the array with the above fields.
	3.	Avoid trailing commas and ensure each entry is properly wrapped in curly braces {}.

## 2.2. Full Info for a Modality (in modalities/<id>.json)

For detailed data about each modality (sections 1–12, references, etc.), create or edit a JSON file in modalities/, named exactly as the id in data.json plus the .json extension.

Example

If id is "mammography", the file is modalities/mammography.json. It should follow the full structure:

```json
{
  "id": "mammography",
  "parents": ["X-Ray"],
  "title": "Mammography",
  "acronyms": ["MG"],
  "shortDescription": "Low-dose X-ray imaging for breast tissue screening.",
  "imagingPrinciple": "...",
  "dataTypeFileFormat": {
    "primaryFileFormats": [...],
    "dataType": [...],
    "relatedDataTypes": [...],
    "standardStorageFormat": "...",
    "conversionSolutions": [...]
  },
  "typicalResolutionImageDims": {
    "spatialResolution": "...",
    "voxelSize": "...",
    "temporalResolution": "..."
  },
  "dataSize": {
    "singleImageSize": "...",
    "typicalStudySize": "..."
  },
  "acquisitionHardware": {
    "equipmentUsed": "...",
    "typicalManufacturers": [...]
  },
  "commonClinicalApps": {
    "primaryUses": [...],
    "specializedUses": [...]
  },
  "radiationSafety": {
    "ionizingRadiation": "Yes",
    "radiationDose": "...",
    "safetyConcerns": "..."
  },
  "preprocessingData": {
    "commonPreprocessingSteps": [...],
    "compressionMethods": [...]
  },
  "challengesLimitations": {
    "technicalChallenges": [...],
    "clinicalLimitations": [...]
  },
  "references": [
    "..."
  ],
  "preparation_meta": [
    {
      "prepared_by": "...",
      "confirmed_by": "...",
      "date_of_preparation": "...",
      "planned_next_review": "...",
      "requires_completion": "false"
    }
  ]
}
```

You can fill in each section (1–12) with as much detail as you have. The search and tabs on the main page rely only on data.json, but the detail page uses this full JSON to display all info.

Remember:
	•	The fields in your detailed JSON should match the structure we discussed (i.e., imagingPrinciple, dataTypeFileFormat, challengesLimitations, etc.).
	•	The id, parents, title, acronyms, and shortDescription should match what’s in data.json.
 
</details>

## 3. Verification & Pushing Changes

1.	Commit/Pull the latest repository changes to avoid merge conflicts.
2.	Add or update the relevant JSON files:
•	team.json for team info
•	data.json for the brief listing of modalities
•	modalities/<id>.json for detailed modality data
3.	Push your changes.
4.	Wait a moment—GitHub Pages automatically rebuilds. Refresh DataTypeHub to see your updates.

---

**Contact / Questions**

If anything is unclear or you need help with JSON syntax, please reach out to the admin/lead developer or consult our issues tab in GitHub. You can reach out to Hossein Toreyhi or Amir Safavi (sdamirsa@gmail.com).

Thank you for contributing to DataTypeHub!


