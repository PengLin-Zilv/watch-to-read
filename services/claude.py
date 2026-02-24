import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import anthropic
import json
from config import ANTHROPIC_API_KEY

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# Difficulty level instructions — this is the prompt engineering core
DIFFICULTY_PROMPTS = {
    "eli5": "Explain everything as if the reader is 12 years old. Use simple words, fun analogies, and avoid jargon completely.",
    "beginner": "Assume the reader has no prior knowledge. Define every concept clearly and use everyday examples.",
    "intermediate": "Assume the reader is familiar with the basics. Focus on connecting concepts and explaining the 'why'.",
    "expert": "Assume the reader is highly knowledgeable. Be dense and technical. Skip definitions, focus on nuance and depth."
}


def process_transcript(transcript: str, difficulty: str) -> dict:
    """
    Main function: takes raw transcript + difficulty level,
    returns structured content as a dict.
    """
    difficulty = difficulty.lower()
    if difficulty not in DIFFICULTY_PROMPTS:
        raise ValueError(f"Invalid difficulty: {difficulty}. Choose from: {list(DIFFICULTY_PROMPTS.keys())}")

    tone_instruction = DIFFICULTY_PROMPTS[difficulty]

    prompt = f"""You are an expert at converting raw video transcripts into clean, structured eBooks.

Tone instruction: {tone_instruction}

Here is the raw transcript:
{transcript}

Convert this transcript into a structured eBook in JSON format with this exact structure:
{{
  "title": "A compelling title for this eBook",
  "summary": "A 2-3 sentence overview of the entire content",
  "chapters": [
    {{
      "chapter_title": "Chapter title",
      "content": "Full chapter content written in prose, not bullet points",
      "key_concepts": ["concept 1", "concept 2", "concept 3"]
    }}
  ]
}}

Rules:
- Create 3 to 5 chapters that flow logically
- Each chapter content should be at least 3 paragraphs
- Key concepts should be the most important terms or ideas from that chapter
- Write in prose, not bullet points
- Apply the tone instruction strictly throughout
- Return only valid JSON, no extra text"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text

    # Strip markdown code fences if Claude wraps response in ```json
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    return json.loads(raw.strip())


# Local testing
if __name__ == "__main__":
    sample = """
    What is a neural network? It's a machine learning model inspired by the human brain.
    It consists of layers of nodes, each connected to the next. Data flows through the network,
    getting transformed at each layer. The network learns by adjusting weights during training.
    Gradient descent helps minimize error. Backpropagation calculates how much each weight
    contributed to the error. With enough data and training, neural networks can recognize
    images, translate languages, and even generate text.
    """

    result = process_transcript(sample, "beginner")
    print(json.dumps(result, indent=2))