import time
import getpass
from selenium.webdriver.common.by import By
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import units
from reportlab.platypus.flowables import KeepInFrame
from PIL import Image as PilImage  # Import Image from Pillow to avoid name clash with ReportLab's Image


def generate_pdf_report(driver):
    timestamp = time.strftime("%B %d, %Y    %H:%M", time.localtime())
    pdf_filename = "test_report.pdf"
    # Adjust margins to give more space if needed
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter,
                            leftMargin=0.75 * units.inch,
                            rightMargin=0.75 * units.inch,
                            topMargin=0.75 * units.inch,
                            bottomMargin=0.75 * units.inch)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>Test Report</b>", styles['h1']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"<b>Date and Time:</b> {timestamp}", styles['Normal']))

    executor = getpass.getuser()
    story.append(Paragraph(f"<b>Test executor:</b> {executor}", styles['Normal']))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Test: Open the web site and create screenshot</b>", styles['h2']))
    story.append(Paragraph("<b>Status:</b> PASS", styles['Normal']))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Steps:</b>", styles['h3']))

    # Define a maximum width for images, for consistent scaling in PDF
    # The image will be scaled to fit this width, maintaining aspect ratio
    pdf_display_width = 5 * units.inch  # This is the desired width in the PDF document

    try:
        driver.get("https://billyal.netlify.app/")
        driver.maximize_window()

        # --- Handle screenshot1 ---
        screenshot1_path = 'screenshot1.png'
        driver.save_screenshot(screenshot1_path)

        # Get actual image dimensions using Pillow
        with PilImage.open(screenshot1_path) as img:
            original_width, original_height = img.size
            # Calculate aspect ratio
            aspect_ratio = original_height / original_width
            # Calculate height to maintain aspect ratio based on desired PDF width
            pdf_display_height = pdf_display_width * aspect_ratio

        story.append(Paragraph("1. Page opened: https://billyal.netlify.app/", styles['Normal']))
        story.append(Paragraph("Screenshot 1:", styles['Normal']))
        # Use explicit calculated width and height for the Image flowable
        img1_flowable = Image(screenshot1_path, width=pdf_display_width, height=pdf_display_height)
        # Wrap it in KeepInFrame to ensure it stays within bounds if needed,
        # but with explicit dimensions, it's more about placement.
        story.append(KeepInFrame(pdf_display_width + units.inch, pdf_display_height + units.inch, [img1_flowable],
                                 hAlign='CENTER', vAlign='MIDDLE'))
        story.append(Spacer(1, 12))  # Increased space after image for better readability
        time.sleep(1)

        elements = driver.find_elements(By.CSS_SELECTOR, '.mx-3.my-1.text-dark.text-decoration-none.fw-bold')
        if elements:
            elements[1].click()
            story.append(Paragraph("2. The element found and selected.", styles['Normal']))

            # --- Handle screenshot2 ---
            screenshot2_path = 'screenshot2.png'
            driver.save_screenshot(screenshot2_path)

            # Get actual image dimensions for screenshot2
            with PilImage.open(screenshot2_path) as img:
                original_width, original_height = img.size
                aspect_ratio = original_height / original_width
                pdf_display_height_2 = pdf_display_width * aspect_ratio

            story.append(Paragraph("3. Second page opened.", styles['Normal']))
            story.append(Paragraph("Screenshot 2:", styles['Normal']))
            img2_flowable = Image(screenshot2_path, width=pdf_display_width, height=pdf_display_height_2)
            story.append(KeepInFrame(pdf_display_width + units.inch, pdf_display_height_2 + units.inch, [img2_flowable],
                                     hAlign='CENTER', vAlign='MIDDLE'))
            story.append(Spacer(1, 12))  # Increased space after image
        else:
            story.append(Paragraph("2. Elements was not found.", styles['Normal']))

        time.sleep(1)
    except Exception as e:
        story.append(Paragraph(f"<b>Error during test execution:</b> {e}", styles['Normal']))

    doc.build(story)
    print(f"PDF отчет сохранен в файле: {pdf_filename}")


def test_billy_al(driver):
    generate_pdf_report(driver)