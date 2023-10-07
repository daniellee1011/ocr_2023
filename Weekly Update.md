# Weekly Update Log


## Week of 10/02 - 10/06

### Completed tasks:

- Extracted data from 2013 (Panama) through 2020.
- Inspected the output files by comparing them to the input PDFs.

### Questions and Plans:

- Explore advanced methods for extracting footnotes.
- Proceed with data extraction for the year 2021.
- Complete data extraction from non-scanned PDFs and inspect the overall output from these non-scanned files.


## Week of 09/25 - 09/29

### Completed tasks:

- Extracted data from the years 2007 to 2013 (Oman).
- Inspected the extracted data for any anomalies.
- Added names of committees that had not previously appeared into committee_list.txt.


### Questions and Plans:

- Explore advanced methods for extracting footnotes.
- Update the helper files to include recent modifications.
- Proceed with data extraction for the year 2013 (Panama).


## Week of 09/18 - 09/22

### Completed tasks:

- ncreased the disk quota of the VM instance from 15GB to 40GB due to the requirements for input PDF files and output files. The impact on cost is as yet unknown, but I don't anticipate a significant increase as we're sticking with the c2-standard-4 configuration. I will provide updates on cost implications as I receive them.
- Extracted data from the years 2004 to 2006.
- Successfully set up the OCR project to run on Google Cloud Platform.
- Preliminary performance metrics on GCP indicate an average processing time of 9.73 seconds per PDF file for Afghanistan 2007 data, compared to 10 seconds on my local laptop. More samples are needed to make a definitive assessment.


### Questions and Plans:

- Explore advanced methods for extracting footnotes.
- Proceed with data extraction for the year 2007.


## Week of 09/11 - 09/15

### Completed tasks:

- Chose c2-standard-4 (4 vCPU, 2 core, 16 GB memory) for the GCP VM instance over E2, N2 due to its higher vCPUs. This is essential for running PyTesseract. (Monthly estimate: $123.44, Hourly: $0.17)
- Set up the necessary environment on the Google Cloud Platform to run the program.
- Extracted data from the years 2001 (Namibia) to 2003.

### Questions and Plans:

- Explore advanced methods for footnote extraction.
- Continue setting up the environment on the Google Cloud Platform for the program.
- Proceed with data extraction for 2004.
- How much budget do I have available for running GCP? I don't want to waste it, but I need this information to decide on the best model for the program.
- I was in the process of setting up environments on the 'ocr' VM instance when I noticed some settings in GCP had been changed by someone. Initially, I couldn't even access the 'ocr' instance, but after adjusting the firewalls for Identity-Aware Proxy, I regained access. For the next steps, I need to access the instance via NoMachine, which I could do until recently. Can you explain why this changed? If these modifications aren't essential, I'd like to revert to the previous environment. If they are necessary, please inform me, and I'll explore alternative ways to continue my work.


## Week of 09/04 - 09/08

### Completed tasks:

- Set up the environment on Discover server to run program. Average duration of extracting data from one pdf file is 463 sec, on the other hand it takes about 10 secs in my personal laptop.
- Implement error handling to keep running, even though encoutering abnormal pdf files.
- Extracted data from 1999 to 2001 (Myanmmar).

### Questions and Plans:

- Delve into advanced methods for footnote extraction.
- Set up the necessary environment on the Google Cloud Platform to run the program.
- Keep extracting from rest of pdf files of 2001.


## Week of 08/28 - 09/01

### Completed tasks:

- Enhanced extract_body_title to manage corner cases, specifically titles with words such as 'draft' and situations where body titles are absent.
- Refined error handling in extract_body_title for files with no input, like the 1999_1493912.pdf from Guinea.
- Augmented the is_not_body method with conditions to better sift out non-body texts.
- Successfully extracted data for 1999, spanning countries from Germany to Honduras.

### Questions and Plans:

- Delve into advanced methods for footnote extraction.
- Set up the necessary environment on the Discovery server to facilitate continuous data extraction from input PDF files.
- General case of footnotes are well filtered, but the cases like 1999_359762.pdf of Ghana are very hard to distinguish with body text. When they are recognized through OCR engines, those footnotes are captured like '3 United Nations, Treaty Series, vol. 189, No. 2545.' and '4 Ibid., vol. 606, No. 8791.' without distinct characters. Could I have a advice to distinguish those kinds of footnotes from genuine body text?

### Timeline:

The timeline below outlines the plan for the OCR project. Please note that while I aim to adhere to this schedule, manual verification of the output and potential code modifications may introduce delays. If the output showcases promising performance, some tasks might be expedited.

- 09/04 - 09/08:
 - Set up the Discovery server.
 - Enhance the process for extracting footnotes.
 - Extract data for 1999 - 2000.

- 09/11 - 09/15:
 - Refine and improve the extraction code based on prior outputs.
 - Extract data for 2001 - 2005.

- 09/18 - 09/22:
 - Refine and improve the extraction code based on prior outputs.
 - Extract data for 2006 - 2010.

- 09/25 - 09/29:
 - Refine and improve the extraction code based on prior outputs.
 - Extract data for 2011 - 2021.


## Week of 08/21 - 08/25

### Completed tasks:

- Reviewed mechanism and output of current extract_body function.
- Designed a strategy or method has been formulated to distinguish between body text and footnotes.
- Implementated the design has been translated into code with helper (is_footnote and is_not_body) functions created for the purpose of classification.
- Updated whole extract_body, has been updated to utilize these helper functions.

### Questions and Plans:

- It is very tricky to distinguish foodnote from body text because footnote has so many patterns. Work on classyfing body text and footnote


## Week of 08/14 - 08/18

### Completed tasks:

- extract_body_title Update: Current code often includes body text when extracting body title details. This leads to inaccuracies in the body title details and negatively affects the accuracy of the extracted body text. I refined the function to properly extract body title details and return a more refined body text, ensuring better input for the extract_body function.
- Adjusted the kernel size for image segmentation to 30 (height) and 35 (width) for the 1999 files.
- Changed the format for creating CSV files to UTF-8 to prevent character corruption, e.g., turning certain characters into '?'.
- Updated .gitignore.
- Completed data extraction for the year 1999, covering countries from Georgia to Germany. The output files, ranging from Ecuador to Gambia, were generated using the latest codes.

### Questions and Plans:

- The extract_body_title function sometimes produces inappropriate body title details in edge cases. I need to refine it, especially for instances where the body title detail includes specific words like 'draft'. This word presents a duplicate pattern when extracting the list of countries. There's also a need to handle cases where the body title detail is absent.
- I'll be working on implementing code to handle exception errors. Currently, if a broken file is processed, the entire code fails and further data processing is halted.


## Week of 08/07 - 08/11

### Completed tasks:

- Extract_agenda_countries Update: Frequently missed agenda items prompted a revisit of this component. Previously, the segmentation for Tesseract was undefined, resulting in erratic splits such as ‘Agenda’, ‘item 24’, and ‘and (b)’ across three segments. For effective extraction, a combined format like ‘Agenda item 24 (b)’ is needed. As a mitigation strategy, I utilized sequences, leveraging preceding agenda items to aid in current extraction. This approach delivered partial success but remains imperfect.
- Preprocessing Implementation: In the past, unprocessed images were directly passed to Tesseract, our OCR engine. This led to tiny segment blocks, making extraction of crucial data like council names, committee names, and agendas difficult. By enlarging these segments, Tesseract now extracts more coherent text chunks. As a result, instead of isolated fragments like 'item 24', we obtain complete data such as 'Agenda item 24 (b)'. The previous segmentation can be viewed in ‘image_with_contours.png’, while the current segmentation samples are available in the ‘segment_image’ directory. For reference, ‘Ecuador_1999_.csv’ represents output from older codes, and ‘Ecuador_1999.csv’ showcases the output from our refined processes.
- Update council_list.txt
- Data extraction was completed for countries spanning Ecuador to Gambia for the year 1999. The output files, ranging from Ecuador to Gambia, have been produced using the updated codes.

### Questions and Plans:

- Continue to evaluate the impact on remaining columns. Experiment to determine the optimal segment size for files and document the findings based on the respective year.
- Update the helper files.

## Week of 07/31 - 08/04

### Completed tasks:

- Evaluated each required column for possible improvements and confirmed that all columns are necessary
- Implemented the extract_committee function to extract committee/commission information from raw data
- Extracted data for countries from Central African Republic to Equatorial Guinea for the year 1999. Output files from the Dominican Republic to Equatorial Guinea have been generated using the latest codes.
- Worked on improving the accuracy of agenda item extraction

### Questions and Plans:

- Continue extraction from the remaining 1999 files and assess the quality of the extracted data
- Improve the extract_agenda_countries function to increase the accuracy of agenda item extraction
- Continue working on improving the remaining functions

### Answers from Prof. Yang:

1. Regarding committee names, It is important information that needs to be collected.  I have noticed that there are certain documents that lack the necessary details regarding the committee names. Please examine the various committee names and devise some function to extract their names from documents correctly.


## Week of 07/24 - 07/28

### Completed tasks:

- Successfully downloaded all raw data files (PDF files for each country).
- Conducted a random check on the format of files related to 1999.
- Introduced a new function, extract_committee, as the existing extract_council function was not adequately robust for precise council name extraction. The revamped extract_council function addresses this by dividing the 'part1_text', which encompasses the initial segment of each PDF file, including the council name. It then compares each split text block with the first two words of every council name to determine the most pertinent council name. This is possible because the first two words of each council name are unique and organize the council list based on the frequency of the council name, with the most frequently appearing council listed at the top. After manually checking over a hundred files, only one file was not correctly matched. Thus, the accuracy score is over 99%. You can observe the improved result by comparing 'Afghanistan_1999' with 'Afghanistan_1999_(extracted by existing extract_council function)'.
- Completed the extraction process for files related to 1999, from Afghanistan to Canada.
- Identified a faulty file (Albania: 1999_287751) that cannot be opened.
- Discovered some files (specifically, from Albania and Azerbaijan: 1999_341823) that seem challenging to categorize as written in English.

### Questions and Plans:

- Is the committee (or commission) name crucial data? The previous Research Assistant used the council name and committee (or commission) name interchangeably, but I believe they are distinctly different. Committees (or commissions) such as the First Committee, COMMISSION ON HUMAN RIGHTS, and so on do not appear in every file. If these are necessary, we need to devise a method to extract them from the raw data files.
- Obtain the output for other 1999 files.
- Review the next column to identify potential improvements.


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

### Answers from Prof. Yang:

1. Finding the correct name of the council can indeed be tricky, as the names are randomly located. My previous RA attempted to verify the council names by creating a descriptive statistics file stored in council_frequency.csv. By analyzing the distribution of names and checking if her current work captured any unusual council names, she was able to identify discrepancies. It's worth noting that some names in the csv file may not actually represent council names. This file was created to aid in this verification process. Most files follow a similar format, but some may have unique characteristics due to few countries using their own formatting or certain years adopting specific patterns in their reporting systems. However, it will be necessary for you to verify these patterns of uniqueness yourself. For example, my previous RA discovered that Russia has its own unique reporting format. Please review her previous report regarding this issue.

2. You can access the work/ocrproject in Discovery and download all the relevant files, which is the same file I shared with you via a Dropbox share link. Once you have completed your work, you will also be responsible for uploading all the files back to Discovery by simply uploading your GitHub folder to the designated directory.

3. I agree with your plan, and I am excited to see your framework using non-scanned files!


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

### Answer from Prof. Yang:

1. It is worth noting that the majority of PDF files dating before 1994 are scanned versions. Thus, it will be necessary for you to devise a method to extract text from these files.
2. If it suits your working preferences, please feel free to utilize your git repository.
3. During the process of extracting council names, it is crucial to ensure the accuracy of the names, as there have been consistent errors in this regard.
