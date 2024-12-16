#!/usr/bin/env python3

import os
import fitz  # PyMuPDF

# Get the directory path from the user
dir_path = input("Enter the path to the directory containing PDF files: ")

# Check if the path is valid
if not os.path.isdir(dir_path):
    print("Invalid directory.")
    exit()

# Prepare the output file
output_file = os.path.join(dir_path, "all_highlights.txt")

# Initialize a list to store highlights from all PDFs
all_highlights = []

# Process each PDF in the directory
for filename in os.listdir(dir_path):
    if filename.lower().endswith(".pdf"):  # Check if the file is a PDF
        pdf_path = os.path.join(dir_path, filename)
        try:
            doc = fitz.open(pdf_path)
            title = os.path.splitext(os.path.basename(pdf_path))[0]  # Use the file name without extension as the title
            highlights = []

            # Iterate through each page of the PDF
            for page_num in range(len(doc)):
                page = doc[page_num]
                annots = page.annots()
                if annots:
                    for annot in annots:
                        if annot.type[0] == 8:  # Highlight annotation
                            try:
                                text = page.get_text("text", clip=annot.rect).replace("\n", "")
                                highlights.append((page_num + 1, text.strip()))
                            except Exception as e:
                                print(f"Error extracting text from annotation in {filename}: {e}")

            # Add highlights to the main list
            if highlights:
                all_highlights.append((title, highlights))

            doc.close()
        except Exception as e:
            print(f"Error processing file {filename}: {e}")

# Write all highlights to the output file
try:
    with open(output_file, "w", encoding="utf-8") as file:
        for title, highlights in all_highlights:
            file.write("=" * 30 + "\n")
            file.write(f"Title: {title}\n")
            file.write("=" * 30 + "\n")
            for page_number, highlight in highlights:
                processed_text = highlight
                file.write(processed_text + "\n\n")
    print(f"*** Saved all highlights successfully to \"{output_file}\" ***")
except Exception as e:
    print(f"Error saving highlights to file: {e}")
