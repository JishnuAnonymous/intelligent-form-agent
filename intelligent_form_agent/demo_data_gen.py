import cv2
import numpy as np
import os

def create_image_with_text(filename, text_lines):
    # Create white image
    img = np.ones((800, 600, 3), dtype=np.uint8) * 255
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    y = 50
    for line in text_lines:
        cv2.putText(img, line, (50, y), font, 0.7, (0, 0, 0), 2, cv2.LINE_AA)
        y += 40
        
    cv2.imwrite(filename, img)
    print(f"Created {filename}")

def generate_samples():
    output_dir = 'data/samples'
    os.makedirs(output_dir, exist_ok=True)

    # Form 1
    create_image_with_text(f"{output_dir}/form_1.jpg", [
        "INVOICE #001",
        "Date: 2026-02-01",
        "Name: Alice Smith",
        "Address: 123 Maple St, Springfield",
        "Phone: 555-0101",
        "Amount: $500.00",
        "Description: Web Design Services",
        "Signature: [Alice Smith]"
    ])

    # Form 2
    create_image_with_text(f"{output_dir}/form_2.jpg", [
        "INVOICE #002",
        "Date: 2026-02-02",
        "Name: Bob Jones",
        "Email: bob@example.com",
        "Amount: $150.50",
        "Description: Hosting Fees",
        "Signature: [Bob Jones]"
    ])
    
    # Form 3
    create_image_with_text(f"{output_dir}/form_3.jpg", [
        "MEDICAL FORM",
        "Date: 2026-01-15",
        "Name: Charlie Brown",
        "DOB: 1980-05-20",
        "Diagnosis: Common Cold",
        "Prescription: Rest and fluids",
        "Signature: [Dr. White]"
    ])

if __name__ == "__main__":
    generate_samples()
