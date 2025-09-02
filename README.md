# Advanced NLP Text Analyzer

A comprehensive Natural Language Processing application that provides sentiment analysis, named entity recognition, emotion detection, and text summarization.

## Features

- **Sentiment Analysis**: Determines if text is positive, negative, or neutral with polarity scores
- **Named Entity Recognition (NER)**: Identifies people, organizations, locations, dates, and more
- **Emotion Analysis**: Detects emotions like joy, sadness, fear, anger, trust, and surprise
- **Text Summarization**: Generates concise summaries using extractive methods
- **Modern Web Interface**: Beautiful, responsive UI built with Tailwind CSS

## Tech Stack

- **Backend**: Python Flask with spaCy, TextBlob, and NRCLex
- **Frontend**: HTML5 with Tailwind CSS and vanilla JavaScript
- **NLP Libraries**: spaCy, TextBlob, NRCLex, NLTK

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

1. **Clone or download the project files**

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download required NLTK data:**
   ```bash
   python -m textblob.download_corpora
   python -c "import nltk; nltk.download('punkt')"
   ```

5. **Download spaCy English model:**
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Running the Application

1. **Start the backend server:**
   ```bash
   python app.py
   ```
   The server will start on `http://127.0.0.1:5000`

2. **Open the frontend:**
   - Open `index.html` in your web browser
   - Or serve it using a local HTTP server

3. **Test the application:**
   - Enter some text in the input area
   - Click "Analyze Text"
   - View the comprehensive analysis results

## API Endpoints

- `GET /` - Server status check
- `GET /health` - Health check for all dependencies
- `POST /analyze` - Main text analysis endpoint

## Example Usage

```json
POST /analyze
{
  "text": "The team at Apple, led by Tim Cook, was overjoyed with the fantastic launch of the new iPhone in Paris. However, some critics were angry about the high price, expressing fear it might not sell well. The event was a huge success overall."
}
```

## Troubleshooting

### Common Issues

1. **Missing NLTK data:**
   ```bash
   python -m textblob.download_corpora
   python -c "import nltk; nltk.download('punkt')"
   ```

2. **spaCy model not found:**
   ```bash
   python -m spacy download en_core_web_sm
   ```

3. **Port already in use:**
   - Change the port in `app.py` line 135
   - Or kill the process using port 5000

4. **CORS issues:**
   - Ensure the backend is running on the expected URL
   - Check that CORS is properly configured

### Health Check

Visit `http://127.0.0.1:5000/health` to verify all dependencies are working correctly.

## Project Structure

```
NLP/
├── app.py              # Flask backend server
├── index.html          # Frontend web interface
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Dependencies

- **Flask**: Web framework
- **flask-cors**: Cross-origin resource sharing
- **spacy**: Advanced NLP processing
- **textblob**: Sentiment analysis
- **nrclex**: Emotion detection
- **nltk**: Natural language toolkit

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this project.

## License

This project is open source and available under the MIT License.

## Author

Suruthi S
