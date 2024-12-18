genai.configure(api_key="AIzaSyD4qZRg6vSkW97sdwRVlgtD7rcehMFgrsA")
import PyPDF2

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        extracted_text = ""
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text
        return extracted_text


def analysing_matching(cv_pdf, job_pdf):

    sample_file_2 = extract_text_from_pdf('pdf/CV_BOCCO_Seyram_Fabrice_Geoffrey.pdf')
    sample_file_3 = extract_text_from_pdf('pdf/Tesla_Offre.pdf')



    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt1 = "Tell me to what percentage this CV and this job offer match, speak French please"
    prompt2 = "Give advice on how to improve your CV and have a much better chance of being hired, speak French please"
    response1 = model.generate_content([prompt1, sample_file_2, sample_file_3])
    response2 = model.generate_content([prompt2])

    return response1.text, response2.text