# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from uagents import Model, Protocol
import asyncio
import logging
from pathlib import Path
from typing import Dict

# Import your existing PDFProcessor and agent-related code
from legal_analysis_agent import PDFProcessor, CaseAnalysis, PetitionAnalysisRequest, legal_agent

app = Flask(__name__)
CORS(app)

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# Initialize PDFProcessor
pdf_processor = PDFProcessor()

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({"status": "healthy"})

@app.route('/analyze_petition', methods=['POST'])
def analyze_petition():
    """
    Endpoint to analyze a new petition
    Expected JSON: {"petition_text": "text content"}
    """
    try:
        data = request.json
        if not data or 'petition_text' not in data:
            return jsonify({"error": "No petition text provided"}), 400

        petition_text = data['petition_text']

        # Create async event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Send message to agent and wait for response
        async def send_to_agent():
            try:
                msg = PetitionAnalysisRequest(petition_text=petition_text)
                response = await legal_agent.send_message(
                    legal_agent.address,
                    msg
                )
                return response
            except Exception as e:
                # logger.error(f"Error communicating with agent: {str(e)}")
                return None

        # Run the async function
        result = loop.run_until_complete(send_to_agent())
        loop.close()

        if result:
            return jsonify({
                "status": "success",
                "analysis": result
            })
        else:
            return jsonify({"error": "Failed to get analysis from agent"}), 500

    except Exception as e:
        # logger.error(f"Error processing petition: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    """
    Endpoint to upload and process a PDF file
    """
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if not file.filename.endswith('.pdf'):
            return jsonify({"error": "File must be a PDF"}), 400

        # Create uploads directory if it doesn't exist
        upload_dir = Path("pdfs")
        upload_dir.mkdir(exist_ok=True)
        
        # Save the file
        file_path = upload_dir / file.filename
        file.save(file_path)

        # Process the PDF using your existing PDFProcessor
        result = pdf_processor.extract_text_from_pdf(str(file_path))

        return jsonify({
            "status": "success",
            "analysis": result
        })

    except Exception as e:
        # logger.error(f"Error processing PDF: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

def run_app():
    """Run both the Flask app and the agent"""
    import threading
    
    # Start the agent in a separate thread
    def run_agent():
        legal_agent.run()
    
    agent_thread = threading.Thread(target=run_agent)
    agent_thread.daemon = True
    agent_thread.start()
    
    # Run Flask app
    app.run(debug=True, port=5000)

if __name__ == '__main__':
    run_app()# # app.py

# from flask import Flask, request, jsonify
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# from flask import Flask, request, jsonify
# from uagents import Agent, Context
# import asyncio

# app = Flask(__name__)

# legal_agent_address = "myseed"

# # Create an async function to send a message to the agent and get a response
# async def analyze_petition_with_agent(petition_text):
#     class PetitionAnalysisRequest(Model):
#         petition_text: str

#     result = await legal_agent.send_and_wait(
#         recipient=legal_agent_address,
#         msg=PetitionAnalysisRequest(petition_text=petition_text),
#         timeout=10.0  # Set a reasonable timeout for waiting for a response
#     )
    
#     return result

# @app.route('/analyze_petition', methods=['POST'])
# def analyze_petition():
#     petition_data = request.json.get('petition_text')

#     # Call the async function that communicates with the agent
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     result = loop.run_until_complete(analyze_petition_with_agent(petition_data))

#     # Return the result from the agent as JSON back to the frontend
#     if result:
#         return jsonify(result)
#     else:
#         return jsonify({"error": "No response from agent"}), 500


# # @app.route('/analyze_petition', methods=['POST'])
# # def analyze_petition():
# #     petition_data = request.json.get('petition_text')
    
# #     response_data = {
# #       'success_probability': 0.75,
# #       'key_arguments': [
# #           "Persistent maintenance issues reported multiple times",
# #           "Violations of local housing codes",
# #           "Documented communication attempts with landlord"
# #       ],
# #       'suggested_precedents': [
# #           "Case #2021-15: Similar maintenance issues, favorable outcome",
# #           "Case #2022-08: Successful petition based on code violations"
# #       ],
# #       'improvement_areas': [
# #           "Include more photographic evidence",
# #           "Add specific dates of maintenance requests",
# #           "Reference relevant local ordinances"
# #       ]
# #     }
    
# #     return jsonify(response_data)

# if __name__ == '__main__':
#     app.run(debug=True)