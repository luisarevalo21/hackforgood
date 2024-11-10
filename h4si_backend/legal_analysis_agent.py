from uagents import Agent, Context, Model
from typing import List, Dict
import pdfplumber
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from PyPDF2 import PdfReader
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import io
from pdf2image import convert_from_path
import tempfile


# import fitz  # PyMuPDF for PDF processing
import re
from pathlib import Path
import spacy
from datetime import datetime
from PyPDF2 import PdfReader
from PIL import Image
import io


# Define models for petition analysis request and response
class PetitionAnalysisRequest(Model):
    petition_text: str

class CaseAnalysis(Model):
    case_number: str
    date: str
    address: str
    findings: List[str]
    decision: str
    outcome: str


class PDFProcessor:

    #  def __init__(self):
    #     self.endpoint = "https://h4sg.cognitiveservices.azure.com/"
    #     self.key = "4W7MJ8fl9BT2WQ8GvQhILjLLKJVVzAJ3buj0alQdzJ8Wx1dZEpPWJQQJ99AKACYeBjFXJ3w3AAALACOGexE4"
    #     self.client = DocumentAnalysisClient(
    #         endpoint=self.endpoint, 
    #         credential=AzureKeyCredential(self.key)
    #     )

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.endpoint = "https://h4sg.cognitiveservices.azure.com/"
        self.key = "4W7MJ8fl9BT2WQ8GvQhILjLLKJVVzAJ3buj0alQdzJ8Wx1dZEpPWJQQJ99AKACYeBjFXJ3w3AAALACOGexE4"
        self.client = DocumentAnalysisClient(
            endpoint=self.endpoint, 
            credential=AzureKeyCredential(self.key)
        )
        

    def extract_text_from_pdf(self, pdf_path: str) -> Dict:
        # Initialize the Azure client
        endpoint = "https://h4sg.cognitiveservices.azure.com/"
        key = "4W7MJ8fl9BT2WQ8GvQhILjLLKJVVzAJ3buj0alQdzJ8Wx1dZEpPWJQQJ99AKACYeBjFXJ3w3AAALACOGexE4"
        client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

        # First verify total pages using PyPDF2
        pdf_reader = PdfReader(pdf_path)
        total_pages = len(pdf_reader.pages)
        print(f"Total pages detected by PyPDF2: {total_pages}")

        pdf_text = ""
          # Initialize metadata dictionary
        metadata = {
            "case_number": None,
            "date": None,
            "address": None,
            "decision": None,
            "findings": [],
            "outcome": None
        }
        
        # Method 1: Process each page separately with Azure
        for page_num in range(total_pages):
            try:
                # Convert PDF page to images
                images = convert_from_path(pdf_path, first_page=page_num + 1, last_page=page_num + 1)
                
                # Process each page image
                for image in images:
                    # Save image temporarily
                    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                        image.save(temp_file.name, 'PNG')
                        
                        # Analyze the image with Azure
                        with open(temp_file.name, 'rb') as image_file:
                            poller = client.begin_analyze_document("prebuilt-document", document=image_file)
                            result = poller.result()
                            
                            # Extract text from the page
                            if result.pages:
                                page = result.pages[0]  # Since we're processing one page at a time
                                for line in page.lines:
                                    pdf_text += line.content + " "
                            
                            print(f"Processed page {page_num + 1}")

                            print(f"Extracted text from {pdf_path}:\n{pdf_text}\n")

                            # Extract case metadata using regex patterns (adjust these as needed)
                            case_pattern = r"Case\s+(\d{4}-\d+)"
                            date_pattern = r"(\d{4}-\d{2}-\d{2})"
                            address_pattern = r"\d{1,5}\s+\w+\s+(?:Street|St|Avenue|Ave|Road|Rd|Way|Drive|Dr)\s+(?:Apt|Unit|#)?\s*\w*"

                            # # Find case number
                            case_pattern = r"CASE NO\.\s*(\d{4}-\d+)"
                            case_match = re.search(case_pattern, pdf_text, re.IGNORECASE)
                            if case_match:
                                metadata["case_number"] = case_match.group(1)
                            
                            date_pattern = r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}"
                            date_match = re.search(date_pattern, pdf_text)
                            if date_match:
                                metadata["date"] = date_match.group(0)

                            address_pattern = r"\d{1,5}\s+\w+\s+(?:Street|St|Avenue|Ave|Road|Rd|Way|Drive|Dr)\s+(?:Apt|Unit)?\s*\w*"
                            address_match = re.search(address_pattern, pdf_text)
                            if address_match:
                                metadata["address"] = address_match.group(0)

                            decision_pattern = r"DECISION(.*?)(?=\n\n|\Z)"
                            decision_match = re.search(decision_pattern, pdf_text, re.DOTALL | re.IGNORECASE)
                            if decision_match:
                                metadata["decision"] = decision_match.group(1).strip()

                            findings_pattern = r"FINDINGS(.*?)(?=DECISION)"
                            findings_match = re.search(findings_pattern, pdf_text, re.DOTALL | re.IGNORECASE)
                            if findings_match:
                                findings_text = findings_match.group(1)
                                numbered_findings = re.findall(r'\d+\.\s*(.*?)(?=\d+\.|$)', findings_text, re.DOTALL)
                                metadata["findings"] = [finding.strip() for finding in numbered_findings]

                            favorable_patterns = [
                                            r"petition\s+is\s+granted",
                                            r"in\s+favor\s+of\s+petitioner",
                                            r"tenant\s+is\s+entitled",
                                            r"landlord\s+shall\s+reduce",
                                            r"rent\s+shall\s+be\s+reduced"
                                        ]
                                        
                            unfavorable_patterns = [
                                r"petition\s+is\s+denied",
                                r"petition\s+is\s+dismissed",
                                r"no\s+relief\s+warranted"
                            ]
                                        
                            for pattern in favorable_patterns:
                                if re.search(pattern, pdf_text, re.IGNORECASE):
                                    metadata["outcome"] = "favorable"
                                    break
                            
                            for pattern in unfavorable_patterns:
                                if re.search(pattern, pdf_text, re.IGNORECASE):
                                    metadata["outcome"] = "unfavorable"
                                    break

                            # print("metadata")
                            print(metadata)

            
            except Exception as e:
                print(f"Error processing page {page_num + 1}: {str(e)}")

      

        return {"metadata": metadata, "full_text": pdf_text}

# Create an agent using Fetch.AI's uAgents framework
legal_agent = Agent(name="legal_analysis_agent", seed="myseed")

pdf_processor = PDFProcessor()
processed_cases = {}

@legal_agent.on_interval(period=600)  # Check for new PDFs every 10 minutes
async def process_new_pdfs(ctx: Context):
    """Monitor and process new PDF documents"""
    pdf_dir = Path("C:/Users/budhr/OneDrive/Desktop/H4SI/h4si_backend/pdfs")
    print(pdf_dir)
    for pdf_path in pdf_dir.glob("*.pdf"):
        if str(pdf_path) not in processed_cases:
            try:
                case_data = pdf_processor.extract_text_from_pdf(str(pdf_path))
                processed_cases[str(pdf_path)] = case_data
                
                ctx.logger.info(f"Processed new case: {case_data['metadata']['case_number']}")
                
            except Exception as e:
                ctx.logger.error(f"Error processing {pdf_path}: {str(e)}")

@legal_agent.on_message(model=PetitionAnalysisRequest)
async def analyze_new_petition(ctx: Context, sender: str, msg: PetitionAnalysisRequest):
    """Analyze a new petition by comparing with processed cases"""
    
    try:
        # Simulate extracting key information from the petition (replace with actual logic)
        response_data = CaseAnalysis(
            case_number="NEW",
            date=datetime.now().strftime("%Y-%m-%d"),
            address="123 Example Street",
            findings=["Persistent maintenance issues", "Violations of local housing codes"],
            decision="PENDING",
            outcome="ANALYSIS"
        )

        # Send the response back to the sender (Flask API)
        await ctx.send(sender, response_data)

    except Exception as e:
        ctx.logger.error(f"Error analyzing petition: {str(e)}")

# Start the agent if running directly
if __name__ == "__main__":
    legal_agent.run()