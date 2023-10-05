import os
import re
import PyPDF2
import requests

# Step 1: Read the Original PDF. Return all pdf links found in the BMA overview
def extract_urls_from_pdf(original_pdf_filename):
    urls = []
    annotation_key = '/Annots' #ref https://pypdf2.readthedocs.io/en/3.0.0/user/reading-pdf-annotations.html
    uri = '/URI'
    anchor = '/A'
    pdf_link_pattern = r'\d+_[\w\d_]+2023\.pdf'  # Regex pattern for matching links (bmanumber_name_2023.pdf)
    with open(original_pdf_filename, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        pages = len(pdf_reader.pages)
        for page_num in range(pages):
            page_sliced = pdf_reader.pages[page_num]
            page_object = page_sliced.get_object()
            if annotation_key in page_object.keys():
                annotation = page_object[annotation_key]
                for all_details in annotation: 
                    detail = all_details.get_object()

                    if uri in detail[anchor].keys():
                        link = detail[anchor][uri]
                        no_limit = -1
                        filename = link.split('/')[no_limit]
                        # Check if the link ends with a valid pdf filename 
                        if re.match(pdf_link_pattern, filename):
                            urls.append(link)
                            #print(link)
    return urls



# Step 3: Download Linked PDFs
def download_linked_pdfs(urls, folder):
    for url in urls:
        #extract the filename from the  URL
        filename = os.path.join(folder, url.split('/')[-1])

        # only download the file if it doesn't exist already
        if os.path.exists(filename):
            print(f"Skipping download of '{filename}' as it already exists on file")
        else:
            response = requests.get(url)
            if response.status_code == 200:
                # Assuming URLs end with .pdf, you may need to adjust this for specific cases
                #filename = url.split('/')[-1]
                with open(filename, 'wb') as pdf_file:
                    pdf_file.write(response.content)
                    print(f"Downloaded: {filename}")

# Step 4: Read and Search in Linked PDFs
def search_keywords_in_pdfs(keywords, folder):
    results = []  # List to store the search results
    for keyword in keywords:
        keyword = keyword.lower()
        # Iterate through downloaded PDFs and search for keywords
        for pdf_filename in downloaded_pdf_files:
            print(f"parsing file: {pdf_filename}")
            pdf_filepath = os.path.join(folder, pdf_filename)
            with open(pdf_filepath, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text().lower()
                    if keyword in text:
                        result = f"Keyword '{keyword}' found in '{pdf_filename}' on page {page_num + 1}"
                        results.append(result)
    for result in results:
        print(result)
    return results

def get_region_filename(): 
   region_folder = "region_pdfs" 
   region = [
    "region1maps2023.pdf",
    "region2maps2023.pdf", 
    "region3maps2023.pdf", 
    "region4maps2023.pdf", 
    "region5maps2023.pdf", 
    "region6maps2023.pdf", 
    "region7maps2023.pdf", 
    "region8maps2023.pdf", 
    ]
   
   while True:
        region_number = input("Which region would you like to see shotgun specific BMAs for? (1 - 7): ")
        if region_number.isdigit():
            region_number = int(region_number)
            if 1 <= region_number <= 7:
                break
            else:
                print(f"{region_number} is not a number between 1 and 7.")
        else:
            print(f"'{region_number}' is not a valid number.")
   filepath = os.path.join(region_folder, region[region_number -1])  # Adjust the path
   return filepath

def store_results_in_file(results, original_pdf_filename, keyword):
    # Construct the output filename
    filename = original_pdf_filename.replace('.pdf', '_')
    region_name = os.path.splitext(os.path.basename(filename))[0]
    keywords_str = '_'.join(keyword).replace(' ', '_')
    output_filename = f"{region_name}_{keywords_str}.txt"

    # Write the results to the file
    with open(output_filename, 'w') as output_file:
        for result in results:
            output_file.write(result + '\n')

            
# Step 5: Print Information
if __name__ == "__main__":

    # Get user input for the region number
    original_pdf_filename = get_region_filename()
    download_folder = original_pdf_filename.replace('.pdf', '_pdfs')

    # Create the download folder if it doesn't exist
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Get user input for keywords
    keywords_input = input("Which keyword do you want to search the BMAs for?: ")
    # Split the input by commas and take the first keyword
    keyword_to_search = [keywords_input.strip().lower().split(',')[0]]

    # Step 1 and 2: Extract URLs from the original PDF
    extracted_urls = extract_urls_from_pdf(original_pdf_filename)

    # Step 3: Download linked PDFs
    download_linked_pdfs(extracted_urls, download_folder)
    if len(extracted_urls) == 0: 
        print (" no pdf URLs found to parse")
    # Store downloaded PDF filenames in a list for later use
    no_limit = -1
    downloaded_pdf_files = [url.split('/')[no_limit] for url in extracted_urls]

    # Step 4: Search for keywords in linked PDFs
    results = search_keywords_in_pdfs(keyword_to_search, download_folder)
    store_results_in_file(results, original_pdf_filename, keyword_to_search)

