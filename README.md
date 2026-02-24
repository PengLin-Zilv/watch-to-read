WatchToRead

Turn any YouTube video into a structured eBook — tailored to your level.

Demo
🔗 Coming soon

What It Does
YouTube is full of great educational content, but video is passive, unsearchable, and easy to forget. WatchToRead takes any YouTube video and converts it into a clean, structured PDF eBook — customized for how deep you want to go.
Input: YouTube URL + audience level
Output: PDF with chapters, key concepts, and summaries

Audience Levels
LevelWho It's For🟢 ELI5No background, explain like I'm 12🔵 BeginnerNew to the topic🟡 IntermediateFamiliar with the basics🔴 ExpertJust the dense, technical content

Tech Stack
LayerTechnologyBackendPython, FlaskAI ProcessingClaude API (Anthropic)Transcript ExtractionYouTube Transcript APIPDF GenerationReportLabDeploymentGoogle Cloud Run

Architecture
User Input (URL + difficulty level)
        ↓
Flask App — coordinates the pipeline
        ↓
├── youtube.py   → extract transcript from video
├── claude.py    → process and structure content with AI
└── ebook.py     → render structured content as PDF
        ↓
PDF Download
Each module has a single responsibility. Swapping Claude for another LLM only touches claude.py. Changing the output format only touches ebook.py.

Getting Started
bash# Clone the repo
git clone https://github.com/PengLin-Zilv/watch-to-read.git
cd watch-to-read

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env

# Run locally
python app.py

Project Structure
watch-to-read/
├── app.py                 # Flask entry point
├── config.py              # Configuration and environment
├── requirements.txt
├── .env.example
├── services/
│   ├── youtube.py         # Transcript extraction
│   ├── claude.py          # AI processing
│   └── ebook.py           # PDF generation
├── templates/
│   └── index.html         # Frontend
└── outputs/               # Generated PDFs (git-ignored)

Environment Variables
bashANTHROPIC_API_KEY=your_key_here

Built by Peng — CS @ Syracuse University