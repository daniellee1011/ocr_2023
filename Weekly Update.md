# Weekly Update Log

## Week of 07/17 - 07/21

### Completed tasks:

- Created a git repository.
- Analyzed and tested the code to improve the extraction of council names.
- Operated Tesseract using various options, such as OEM and language selection. The tests confirmed that these adjustments did not significantly improve council name extraction.

### Questions and Plans:

- Has the extraction of council names always been problematic?
- Tesseract first segments an image file before extracting text from each segment. The current code combines all the text into a single string, from which dates, council names, etc., are then extracted. Sometimes, these elements are matched with data from helper files. I had to create missing files based on the council_frequency.csv file, assuming it to contain meaningful data. What is the purpose of council_frequency.csv? Is council_frequency.csv an output that you specifically requested? For example, 'Commission On Human Rights', listed in council_frequency.csv, seems not to be a council name, but a session name. Similarly, 'First Committee', 'Second Committee', etc., do not seem to be council names.
- Could you please re-share the Dropbox link with the data files? There were additional files that I still needed to download.
- It might be necessary to use different approaches for PDF files before 1994, such as preprocessing or other techniques, for scanned versions. Tesseract tends to perform poorly on lower quality images. We might need to use a different OCR engine due to Tesseract's limitations in dealing with low-quality images. Given that this project is in the early stages, I suggest that we first build a broad framework using high-quality, non-scanned files, and then focus on OCR for scanned versions.

## Week of 07/10 - 07/14

### Completed tasks:

- Downloaded PDF files from Dropbox.
- Conducted research on OCR and Tesseract.
- Set up the development environment for using Tesseract.
- Created two missing files, council_list.txt and util.txt, to run the program.
- Executed the previous Research Assistant's code with various DPI values, which are crucial for optimal OCR performance, to determine the best DPI setting.

### Questions and Plans:

- If I continue to work on the project, I plan to continue using Tesseract. The previous worker's rationale for choosing Tesseract was compelling, as it is one of the best performing OCR engines and is regularly updated.
- In the initial Weekly Report (February 14-19), the previous Research Assistant used Image Preprocessing. However, it doesn't seem to be in use now. Could it be that the PDF files after 1994 don't require image preprocessing because they are not scanned files?
- I am considering creating a Git repository based on the previous work. Would this be acceptable?
- From my results, the extracted data in the Council column is not accurate. I plan to investigate how to improve this.
- The current usage of Tesseract operates without options. I will test it with options to see if the results improve.

### Answer from Prof. Yang
1. It is worth noting that the majority of PDF files dating before 1994 are scanned versions. Thus, it will be necessary for you to devise a method to extract text from these files.
2. If it suits your working preferences, please feel free to utilize your git repository.
3. During the process of extracting council names, it is crucial to ensure the accuracy of the names, as there have been consistent errors in this regard.