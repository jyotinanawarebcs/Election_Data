# import fitz  # PyMuPDF
# import cv2
# import numpy as np
# import os

# # --- Configuration ---
# PDF_FILE = r"C:\Users\LENOVO pro\Desktop\JYOTI\kbnmc\kbnmc\kbmc\bmc_2017\PDF-2017\FinalList_Ward_40.pdf"  # The name of your PDF
# OUTPUT_DIR = r"C:\Users\LENOVO pro\Desktop\JYOTI\kbnmc\kbnmc\kbmc\bmc_2017\cropped_voters_ward40"  # Folder to save the cropped images
# DPI = 300  # Resolution for converting PDF to image (higher is better)

# # --- Parameters to Tune ---
# # You may need to adjust these values based on your PDF's scan quality
# # to correctly identify the voter blocks.
# MIN_BLOCK_AREA = 80000  # Minimum area of a block (width * height)
# MAX_BLOCK_AREA = 500000  # Maximum area of a block
# CROP_PADDING = 10  # Pixels to add around the crop to avoid cutting text
# ROW_TOLERANCE = 50  # How close (in pixels) Y-coordinates can be to be in the "same row"


# # ---------------------------


# def sort_contours(contours):
#     """
#     Sorts contours from top-to-bottom, then left-to-right.
#     """
#     bounding_boxes = [cv2.boundingRect(c) for c in contours]

#     # Sort by 'y' coordinate, but group by rows first
#     # This groups boxes whose 'y' coordinates are within ROW_TOLERANCE
#     def get_sort_key(box):
#         # 'box' is (x, y, w, h)
#         return (box[1] // ROW_TOLERANCE, box[0])

#     # Sort the (contour, bounding_box) pairs together
#     cnt_boxes = sorted(zip(contours, bounding_boxes), key=lambda pair: get_sort_key(pair[1]))

#     # Unzip back into separate lists
#     sorted_cnts = [cnt for cnt, box in cnt_boxes]
#     sorted_boxes = [box for cnt, box in cnt_boxes]

#     return sorted_cnts, sorted_boxes


# def process_pdf():
#     print(f"Starting processing for '{PDF_FILE}'...")

#     # Create output directory if it doesn't exist
#     os.makedirs(OUTPUT_DIR, exist_ok=True)

#     voter_serial_number = 1

#     try:
#         doc = fitz.open(PDF_FILE)
#     except Exception as e:
#         print(f"Error opening PDF: {e}")
#         print("Please make sure 'voter_list.pdf' is in the same directory as the script.")
#         return

#     for page_num in range(len(doc)):
#         print(f"Processing page {page_num + 1}/{len(doc)}...")

#         page = doc.load_page(page_num)

#         # 1. Render PDF page to a high-resolution image
#         pix = page.get_pixmap(dpi=DPI)
#         try:
#             # Convert pixmap to a numpy array for OpenCV
#             img_data = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)

#             # Handle different image formats (RGB, CMYK, Grayscale)
#             if pix.n == 4:  # CMYK
#                 img_bgr = cv2.cvtColor(img_data, cv2.COLOR_CMYK2BGR)
#             elif pix.n == 3:  # RGB
#                 img_bgr = cv2.cvtColor(img_data, cv2.COLOR_RGB2BGR)
#             else:  # Grayscale
#                 img_bgr = cv2.cvtColor(img_data, cv2.COLOR_GRAY2BGR)

#         except Exception as e:
#             print(f"  Error converting page {page_num + 1} to image: {e}")
#             continue

#         # 2. Process the image to find blocks
#         img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

#         # Invert the image (blocks become white, background black)
#         # Use adaptive thresholding to handle uneven lighting
#         img_thresh = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#                                            cv2.THRESH_BINARY_INV, 11, 2)

#         # 3. Find contours
#         # We find *all* contours and filter them
#         contours, _ = cv2.findContours(img_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#         valid_contours = []
#         for cnt in contours:
#             x, y, w, h = cv2.boundingRect(cnt)
#             area = w * h

#             # 4. Filter contours based on area
#             if MIN_BLOCK_AREA < area < MAX_BLOCK_AREA:
#                 valid_contours.append(cnt)

#         print(f"  Page {page_num + 1}: Found {len(valid_contours)} potential voter blocks.")

#         if not valid_contours:
#             print("  No blocks found. Try adjusting MIN/MAX_BLOCK_AREA in the script.")
#             continue

#         # 5. Sort the valid blocks
#         sorted_contours, sorted_boxes = sort_contours(valid_contours)

#         # 6. Crop and save each block
#         for i, (x, y, w, h) in enumerate(sorted_boxes):
#             # Add padding, but don't go out of bounds
#             y1 = max(0, y - CROP_PADDING)
#             y2 = min(img_bgr.shape[0], y + h + CROP_PADDING)
#             x1 = max(0, x - CROP_PADDING)
#             x2 = min(img_bgr.shape[1], x + w + CROP_PADDING)

#             # Crop from the *original color image*
#             cropped_image = img_bgr[y1:y2, x1:x2]

#             # Save the file
#             output_filename = os.path.join(OUTPUT_DIR, f"voter_{voter_serial_number}.png")
#             cv2.imwrite(output_filename, cropped_image)

#             voter_serial_number += 1

#     doc.close()
#     print(f"\nProcessing complete. {voter_serial_number - 1} images saved to '{OUTPUT_DIR}'.")


# # --- Run the script ---
# if __name__ == "__main__":
#     process_pdf()
import fitz  # PyMuPDF
import cv2
import numpy as np
import os


# ----------------------------
# CONFIG
# ----------------------------
import fitz  # PyMuPDF
import cv2
import numpy as np
import os
import re


# ----------------------------
# CONFIG
# ----------------------------
ROOT_FOLDER = r"C:\Users\LENOVO pro\Desktop\JYOTI\kbnmc\kbnmc\kbmc\bmc_2017\PDF-2017"
DPI = 300

MIN_BLOCK_AREA = 80000
MAX_BLOCK_AREA = 500000
CROP_PADDING = 10
ROW_TOLERANCE = 50


# ----------------------------
# SORTING FUNCTION
# ----------------------------
def sort_contours(contours):
    bounding_boxes = [cv2.boundingRect(c) for c in contours]

    def get_sort_key(box):
        return (box[1] // ROW_TOLERANCE, box[0])

    cnt_boxes = sorted(zip(contours, bounding_boxes), key=lambda pair: get_sort_key(pair[1]))
    sorted_cnts = [cnt for cnt, box in cnt_boxes]
    sorted_boxes = [box for cnt, box in cnt_boxes]

    return sorted_cnts, sorted_boxes


# ----------------------------
# Extract ward name from PDF filename
# ----------------------------
def extract_ward_name(pdf_name):
    pdf_name_clean = pdf_name.replace(".pdf", "")

    # Try to match patterns like Ward_40 or WARD-40 or Ward40
    match = re.search(r"(Ward[_\- ]*\d+)", pdf_name_clean, re.IGNORECASE)
    if match:
        return match.group(1).replace(" ", "_").replace("-", "_")

    # Default: use filename directly
    return pdf_name_clean.replace(" ", "_")


# ----------------------------
# PROCESS A SINGLE PDF
# ----------------------------
def process_pdf(pdf_file, ward_name):
    print(f"\n📄 Processing PDF: {pdf_file}")

    # Create output folder
    output_dir = os.path.join(ROOT_FOLDER, "cropped_output", ward_name)
    os.makedirs(output_dir, exist_ok=True)

    voter_serial_number = 1

    try:
        doc = fitz.open(pdf_file)
    except Exception as e:
        print(f"❌ Error opening PDF: {e}")
        return

    for page_num in range(len(doc)):
        print(f"  ➝ Page {page_num + 1}/{len(doc)}")

        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=DPI)

        try:
            img_data = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)

            if pix.n == 4:
                img_bgr = cv2.cvtColor(img_data, cv2.COLOR_CMYK2BGR)
            elif pix.n == 3:
                img_bgr = cv2.cvtColor(img_data, cv2.COLOR_RGB2BGR)
            else:
                img_bgr = cv2.cvtColor(img_data, cv2.COLOR_GRAY2BGR)

        except Exception as e:
            print(f"❌ Error converting page {page_num + 1}: {e}")
            continue

        img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        img_thresh = cv2.adaptiveThreshold(img_gray, 255,
                                           cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                           cv2.THRESH_BINARY_INV, 11, 2)

        contours, _ = cv2.findContours(img_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        valid_contours = []
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            area = w * h
            if MIN_BLOCK_AREA < area < MAX_BLOCK_AREA:
                valid_contours.append(cnt)

        print(f"    → Found: {len(valid_contours)} blocks")

        if not valid_contours:
            continue

        sorted_contours, sorted_boxes = sort_contours(valid_contours)

        for (x, y, w, h) in sorted_boxes:
            y1 = max(0, y - CROP_PADDING)
            y2 = min(img_bgr.shape[0], y + h + CROP_PADDING)
            x1 = max(0, x - CROP_PADDING)
            x2 = min(img_bgr.shape[1], x + w + CROP_PADDING)

            cropped = img_bgr[y1:y2, x1:x2]

            output_path = os.path.join(output_dir, f"voter_{voter_serial_number}.png")
            cv2.imwrite(output_path, cropped)
            voter_serial_number += 1

    doc.close()
    print(f"✅ Completed: {voter_serial_number - 1} images saved")


# ----------------------------
# PROCESS ALL PDFs
# ----------------------------
def process_all_pdfs():
    print(f"\n🔍 Scanning PDFs in: {ROOT_FOLDER}")

    for file in os.listdir(ROOT_FOLDER):
        if file.lower().endswith(".pdf"):
            pdf_path = os.path.join(ROOT_FOLDER, file)

            # Extract name from PDF
            ward_name = extract_ward_name(file)

            print(f"\n===============================")
            print(f"🏷️  Ward Detected from PDF: {ward_name}")
            print(f"===============================\n")

            process_pdf(pdf_path, ward_name)


# ----------------------------
# MAIN
# ----------------------------
if __name__ == "__main__":
    process_all_pdfs()
