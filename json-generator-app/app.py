import json
import streamlit as st
import datetime

###############################################################################
# CALLBACKS AND INITIALIZATION
###############################################################################

def init_session_state():
    if "meta_data" not in st.session_state:
        st.session_state["meta_data"] = {
            "id": "",
            "parents": [""],
            "title": "",
            "acronyms": ["", "", "", ""],
            "shortDescription": ""
        }
    if "preparation_meta_data" not in st.session_state:
        st.session_state["preparation_meta_data"] = {
            "prepared_by": "",
            "confirmed_by": "",
            "date_of_preparation": datetime.date.today().isoformat(),
            "planned_next_review": "",
            "requires_completion": ""
        }
    if "rawtext_headings" not in st.session_state:
        # Each entry is [number, title, content]
        st.session_state["rawtext_headings"] = []
    if "table_headings" not in st.session_state:
        # Each entry is {"number": str, "title": str, "table": [ [col headers], [row1 data], ... ]}
        st.session_state["table_headings"] = []
    if "show_review_page" not in st.session_state:
        st.session_state["show_review_page"] = False

# Callbacks for the "Data Type Information" (raw markdown headings)
def add_rawtext_row():
    st.session_state["rawtext_headings"].append(["", "", ""])

def remove_last_rawtext_row():
    if len(st.session_state["rawtext_headings"]) > 0:
        st.session_state["rawtext_headings"].pop()

# Callbacks for Table Headings
def add_table_heading():
    """
    Creates a new empty table with 1 header row (by default 1 column),
    plus 1 empty data row. The user can add columns/rows in the UI.
    """
    st.session_state["table_headings"].append({
        "number": "",
        "title": "",
        "table": [
            ["Column 1"],  # row 0 -> column headers
            [""],          # row 1 -> first data row
        ]
    })

def add_conversion_table():
    """
    Creates a new table with 4 preset column headers for conversions,
    plus one empty data row.
    """
    st.session_state["table_headings"].append({
        "number": "",
        "title": "",
        "table": [
            ["conversion_from", "conversion_to", "description", "link to code/software"],
            ["", "", "", ""]
        ]
    })

def add_row_table(idx):
    """
    Adds a new data row to the table 'table_headings[idx]',
    leaving the header row alone.
    """
    if 0 <= idx < len(st.session_state["table_headings"]):
        table_data = st.session_state["table_headings"][idx]["table"]
        if len(table_data) == 0:
            # if no rows at all, create 1 header row + 1 data row
            table_data.append(["Column 1"])
            table_data.append([""])
        else:
            col_count = len(table_data[0])  # number of columns from the header row
            new_row = ["" for _ in range(col_count)]
            table_data.append(new_row)

def add_column_table(idx):
    """
    Adds a new column to the table 'table_headings[idx]'.
    The first row is headers, subsequent rows are data.
    """
    if 0 <= idx < len(st.session_state["table_headings"]):
        table_data = st.session_state["table_headings"][idx]["table"]
        for r, row in enumerate(table_data):
            if r == 0:
                # For the header row, create a default column name
                row.append(f"Column {len(row) + 1}")
            else:
                row.append("")

# Page switching
def go_to_review_page():
    st.session_state["show_review_page"] = True

def back_to_editor():
    st.session_state["show_review_page"] = False


###############################################################################
# PARSE & BUILD JSON
###############################################################################

def parse_json_into_session(json_data):
    st.session_state["meta_data"] = {
        "id": "",
        "parents": [""],
        "title": "",
        "acronyms": ["", "", "", ""],
        "shortDescription": ""
    }
    st.session_state["preparation_meta_data"] = {
        "prepared_by": "",
        "confirmed_by": "",
        "date_of_preparation": datetime.date.today().isoformat(),
        "planned_next_review": "",
        "requires_completion": ""
    }
    st.session_state["rawtext_headings"] = []
    st.session_state["table_headings"] = []

    for item in json_data:
        level = item.get("level", "")
        ctype = item.get("content-type", "")
        content = item.get("content", "")
        title = item.get("title", "")

        # meta-data
        if level == "meta-data-id":
            st.session_state["meta_data"]["id"] = content
        elif level == "meta-data-parents" and ctype == "list_of_strings":
            st.session_state["meta_data"]["parents"] = content if isinstance(content, list) else []
        elif level == "meta-data-title":
            st.session_state["meta_data"]["title"] = content
        elif level == "meta-data-acronyms" and ctype == "list_of_strings":
            st.session_state["meta_data"]["acronyms"] = content if isinstance(content, list) else []
        elif level == "meta-data-shortDescription":
            st.session_state["meta_data"]["shortDescription"] = content

        # prep meta-data
        elif level == "prepration-meta-data-prepared_by":
            st.session_state["preparation_meta_data"]["prepared_by"] = content
        elif level == "prepration-meta-data-confirmed_by":
            st.session_state["preparation_meta_data"]["confirmed_by"] = content
        elif level == "prepration-meta-data-date_of_preparation":
            st.session_state["preparation_meta_data"]["date_of_preparation"] = content
        elif level == "prepration-meta-data-planned_next_review":
            st.session_state["preparation_meta_data"]["planned_next_review"] = content
        elif level == "prepration-meta-data-requires_completion":
            st.session_state["preparation_meta_data"]["requires_completion"] = content

        # headings
        else:
            if ctype == "table":
                # expecting a list of lists, where row 0 = column headers
                st.session_state["table_headings"].append({
                    "number": level,
                    "title": title,
                    "table": content
                })
            elif ctype == "markdown":
                # data type info row
                st.session_state["rawtext_headings"].append([level, title, content])
            # else ignore older format or unrecognized

    # Cleanup empty strings
    st.session_state["meta_data"]["parents"] = [
        p for p in st.session_state["meta_data"]["parents"] if p.strip()
    ] or [""]
    st.session_state["meta_data"]["acronyms"] = [
        a for a in st.session_state["meta_data"]["acronyms"] if a.strip()
    ] or ["", "", "", ""]

def build_final_json():
    final_list = []

    meta = st.session_state["meta_data"]
    # meta-data with single dictionary for parents & acronyms
    final_list.append({
        "level": "meta-data-id",
        "title": "id",
        "content-type": "rawtext",
        "content": meta["id"]
    })
    final_list.append({
        "level": "meta-data-parents",
        "title": "parents",
        "content-type": "list_of_strings",
        "content": meta["parents"]
    })
    final_list.append({
        "level": "meta-data-title",
        "title": "title",
        "content-type": "rawtext",
        "content": meta["title"]
    })
    final_list.append({
        "level": "meta-data-acronyms",
        "title": "acronyms",
        "content-type": "list_of_strings",
        "content": meta["acronyms"]
    })
    final_list.append({
        "level": "meta-data-shortDescription",
        "title": "shortDescription",
        "content-type": "rawtext",
        "content": meta["shortDescription"]
    })

    # headings
    combined = []
    # store data type info as markdown
    for rt in st.session_state["rawtext_headings"]:
        num_str, heading_title, heading_content = rt
        # If the row is fully empty, skip adding to final JSON
        if num_str.strip() == "" and heading_title.strip() == "" and heading_content.strip() == "":
            continue
        combined.append({
            "number": num_str,
            "title": heading_title,
            "content-type": "markdown",
            "content": heading_content
        })
    for tb in st.session_state["table_headings"]:
        combined.append({
            "number": tb["number"],
            "title": tb["title"],
            "content-type": "table",
            "content": tb["table"]
        })

    # sort
    def parse_num(n):
        parts = [p for p in n.split(".") if p.strip()]
        try:
            return tuple(int(p) for p in parts)
        except ValueError:
            return (999999,)

    combined.sort(key=lambda x: parse_num(x["number"]))

    for c in combined:
        final_list.append({
            "level": c["number"],
            "title": c["title"],
            "content-type": c["content-type"],
            "content": c["content"]
        })

    # prep meta-data
    prep = st.session_state["preparation_meta_data"]
    final_list.append({
        "level": "prepration-meta-data-prepared_by",
        "title": "prepared_by",
        "content-type": "rawtext",
        "content": prep["prepared_by"]
    })
    final_list.append({
        "level": "prepration-meta-data-confirmed_by",
        "title": "confirmed_by",
        "content-type": "rawtext",
        "content": prep["confirmed_by"]
    })
    final_list.append({
        "level": "prepration-meta-data-date_of_preparation",
        "title": "date_of_preparation",
        "content-type": "rawtext",
        "content": prep["date_of_preparation"]
    })
    final_list.append({
        "level": "prepration-meta-data-planned_next_review",
        "title": "planned_next_review",
        "content-type": "rawtext",
        "content": prep["planned_next_review"]
    })
    final_list.append({
        "level": "prepration-meta-data-requires_completion",
        "title": "requires_completion",
        "content-type": "rawtext",
        "content": prep["requires_completion"]
    })

    return final_list

###############################################################################
# RENDERING FUNCTIONS (EDITOR PAGES)
###############################################################################

def render_table_editor(prefix, table_data, idx):
    """
    Renders the table. The first row is interpreted as column headers (user-editable).
    Subsequent rows are data, each row begins with a read-only row number.
    """
    if not table_data:
        # If there's no data, create a default structure
        table_data.append(["Column 1"])  # row 0: column headers
        table_data.append([""])          # row 1: first data row

    row_count = len(table_data)
    col_count = len(table_data[0])

    # --- Render header row ---
    # We'll create col_count + 1 columns in Streamlit so that the first col can label "Row # / Columns".
    header_cols = st.columns(col_count + 1)
    with header_cols[0]:
        # You can place any label or empty text here
        st.write("Row # / Columns")
    for c in range(col_count):
        with header_cols[c + 1]:
            cell_key = f"{prefix}_hdr_c{c}"
            table_data[0][c] = st.text_input(
                cell_key,
                value=table_data[0][c],
                label_visibility="collapsed"
            )

    # --- Render data rows (row 1 onward) ---
    for r in range(1, row_count):
        row_cols = st.columns(col_count + 1)
        with row_cols[0]:
            # Display a read-only row number
            st.write(str(r))
        for c in range(col_count):
            with row_cols[c + 1]:
                cell_key = f"{prefix}_r{r}_c{c}"
                table_data[r][c] = st.text_input(
                    cell_key,
                    value=table_data[r][c],
                    label_visibility="collapsed"
                )

    #  Add row/column buttons, e.g.:
    btn_cols = st.columns(2)
    with btn_cols[0]:
        st.button("Add Row", on_click=add_row_table, args=(idx,), key=f"addrow_{idx}")
    with btn_cols[1]:
        st.button("Add Column", on_click=add_column_table, args=(idx,), key=f"addcol_{idx}")

    return table_data


def editor_page():
    st.title("Medical Modality Definition - Editor")

    # ========== META-DATA ==========
    meta = st.session_state["meta_data"]
    st.write("**Meta-Data**")
    # Use HTML for color
    c1, c2 = st.columns([1,3])
    with c1:
        st.markdown("<span style='color:blue;font-weight:bold'>ID (lowercase)</span>", unsafe_allow_html=True)
    with c2:
        meta["id"] = st.text_input("id_lowercase", meta["id"], label_visibility="collapsed")

    st.markdown("<span style='color:blue;font-weight:bold'>Parents</span>", unsafe_allow_html=True)
    parents_copy = list(meta["parents"])
    row_size = 4
    idx_p = 0
    while idx_p < len(parents_copy):
        cols = st.columns(row_size)
        for j in range(row_size):
            if idx_p < len(parents_copy):
                with cols[j]:
                    parents_copy[idx_p] = st.text_input(
                        f"parents_{idx_p}",
                        value=parents_copy[idx_p],
                        label_visibility="collapsed"
                    )
                idx_p += 1

    def add_parent():
        st.session_state["meta_data"]["parents"].append("")
    st.button("Add parent", on_click=add_parent, key="btn_add_parent")
    meta["parents"] = parents_copy

    c3, c4 = st.columns([1,3])
    with c3:
        st.markdown("<span style='color:blue;font-weight:bold'>Title</span>", unsafe_allow_html=True)
    with c4:
        meta["title"] = st.text_input("title_field", meta["title"], label_visibility="collapsed")

    st.markdown("<span style='color:blue;font-weight:bold'>Acronyms</span>", unsafe_allow_html=True)
    acronyms_copy = list(meta["acronyms"])
    idx_a = 0
    while idx_a < len(acronyms_copy):
        cols = st.columns(row_size)
        for j in range(row_size):
            if idx_a < len(acronyms_copy):
                with cols[j]:
                    acronyms_copy[idx_a] = st.text_input(
                        f"acronyms_{idx_a}",
                        value=acronyms_copy[idx_a],
                        label_visibility="collapsed"
                    )
                idx_a += 1

    def add_acronym():
        st.session_state["meta_data"]["acronyms"].append("")
    st.button("Add acronym", on_click=add_acronym, key="btn_add_acronym")
    meta["acronyms"] = acronyms_copy

    st.markdown("<span style='color:blue;font-weight:bold'>Short Description</span>", unsafe_allow_html=True)
    meta["shortDescription"] = st.text_area(
        "shortDescription_field",
        meta["shortDescription"],
        label_visibility="collapsed"
    )

    st.write("---")

    # ========== PREPARATION META-DATA ==========
    st.write("**Preparation Meta-Data**")
    prep = st.session_state["preparation_meta_data"]

    col_pre1, col_pre2 = st.columns(2)
    with col_pre1:
        st.markdown("<span style='color:orange;font-weight:bold'>Prepared by</span>", unsafe_allow_html=True)
        prep["prepared_by"] = st.text_input("prepared_by", prep["prepared_by"], label_visibility="collapsed")
    with col_pre2:
        st.markdown("<span style='color:orange;font-weight:bold'>Confirmed by</span>", unsafe_allow_html=True)
        prep["confirmed_by"] = st.text_input("confirmed_by", prep["confirmed_by"], label_visibility="collapsed")

    col_pre3, col_pre4 = st.columns(2)
    with col_pre3:
        st.markdown("<span style='color:orange;font-weight:bold'>Date of Preparation (YYYY-MM-DD)</span>", unsafe_allow_html=True)
        prep["date_of_preparation"] = st.text_input("date_of_preparation", prep["date_of_preparation"], label_visibility="collapsed")
    with col_pre4:
        st.markdown("<span style='color:orange;font-weight:bold'>Planned next review</span>", unsafe_allow_html=True)
        prep["planned_next_review"] = st.text_input("planned_next_review", prep["planned_next_review"], label_visibility="collapsed")

    st.markdown("<span style='color:orange;font-weight:bold'>Requires completion</span>", unsafe_allow_html=True)
    prep["requires_completion"] = st.text_area("requires_completion", prep["requires_completion"], label_visibility="collapsed")

    st.write("---")

    # ========== DATA TYPE INFORMATION ==========
    st.write("**Enter Data Type Information**")
    st.info(
        "Use the columns below to specify:\n"
        "- **Number**: e.g. `1` or `1.1` (2 levels acceptable)\n"
        "- **Title**: heading title\n"
        "- **Content** (saved as **Markdown**): you can paste your data; sometimes you may need to paste twice.\n\n"
        "**Note**: If you need a table for any heading/subheading, use the next section.\n"
        "**Tip**: If you want an empty row to not appear in the final JSON, ensure all three columns are blank."
    )

    # Table headers for data type info
    head_cols = st.columns([1,2,5])
    with head_cols[0]:
        st.write("**Number**")
    with head_cols[1]:
        st.write("**Title**")
    with head_cols[2]:
        st.write("**Content** (Markdown)")

    # If no row, add one
    if not st.session_state["rawtext_headings"]:
        st.session_state["rawtext_headings"].append(["", "", ""])

    for i, row in enumerate(st.session_state["rawtext_headings"]):
        cols = st.columns([1,2,5])
        row[0] = cols[0].text_input(f"raw_number_{i}", value=row[0], label_visibility="collapsed")
        row[1] = cols[1].text_input(f"raw_title_{i}", value=row[1], label_visibility="collapsed")
        row[2] = cols[2].text_input(f"raw_content_{i}", value=row[2], label_visibility="collapsed")

    st.button("Add Row", on_click=add_rawtext_row, key="add_rawtext")
    st.button("Remove Last Row", on_click=remove_last_rawtext_row, key="remove_rawtext")

    st.write("---")

    # ========== TABLE HEADINGS ==========
    st.write("**Table Headings**")
    heading_btn_cols = st.columns(2)
    with heading_btn_cols[0]:
        st.button("Add Table Heading", on_click=add_table_heading, key="btn_add_table_heading")
    with heading_btn_cols[1]:
        st.button("Add Conversion Table", on_click=add_conversion_table, key="btn_add_conversion_table")

    new_table_headings = []
    skip_removal = False

    for idx, table_obj in enumerate(st.session_state["table_headings"]):
        if skip_removal:
            new_table_headings.append(table_obj)
            continue

        st.write(f"**Table Heading #{idx+1}**")
        sub_cols = st.columns([1,2])
        with sub_cols[0]:
            st.write("Heading Number")
            num_val = st.text_input(f"table_num_{idx}", value=table_obj["number"], label_visibility="collapsed")
        with sub_cols[1]:
            st.write("Heading Title")
            title_val = st.text_input(f"table_title_{idx}", value=table_obj["title"], label_visibility="collapsed")

        # Render the actual table
        table_val = render_table_editor(f"table_{idx}", table_obj["table"], idx)

        remove_clicked = st.button(f"Remove Table Heading #{idx+1}", key=f"remove_table_{idx}")
        if remove_clicked:
            skip_removal = True
            st.write("This table heading removed.")
        else:
            new_table_headings.append({
                "number": num_val,
                "title": title_val,
                "table": table_val
            })

        st.write("---")

    st.session_state["table_headings"] = new_table_headings

    # ========== SAVE & GO TO REVIEW PAGE ==========
    st.button("Save and go to Review Page", on_click=go_to_review_page, key="btn_go_review")


def review_page():
    st.title("Review & Download")

    final_data = build_final_json()
    st.subheader("Final JSON Preview")
    st.json(final_data)

    file_name = (st.session_state["meta_data"]["id"] or "output") + ".json"
    json_str = json.dumps(final_data, indent=4)

    st.download_button(
        label="Download JSON",
        data=json_str,
        file_name=file_name,
        mime="application/json"
    )

    st.button("Back to Editor", on_click=back_to_editor, key="btn_back_editor")


###############################################################################
# MAIN
###############################################################################

def main():
    st.set_page_config(page_title="Medical Modality Editor", layout="wide")
    init_session_state()

    st.sidebar.title("Options")
    uploaded_file = st.sidebar.file_uploader("Upload previously saved JSON", type=["json"])
    if uploaded_file is not None:
        try:
            file_contents = uploaded_file.read().decode("utf-8")
            loaded_json = json.loads(file_contents)
            parse_json_into_session(loaded_json)
            st.sidebar.success("Successfully loaded JSON!")
        except Exception as e:
            st.sidebar.error(f"Error loading JSON: {e}")

    if st.session_state["show_review_page"]:
        review_page()
    else:
        editor_page()


if __name__ == "__main__":
    main()