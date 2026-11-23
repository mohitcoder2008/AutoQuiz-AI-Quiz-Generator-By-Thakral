import ollama
import json

def generate_questions(text_chunk):
    prompt = f"""
You are an expert quiz generator.

You MUST generate exactly 3 separate questions.
Do not stop after generating the first question.
Complete all 3 questions before returning the JSON.
The questions must have different wording and test different aspects of the material.

Rules:
1. Every question must be based on the study material.
2. Each question must have exactly 4 meaningful options.
3. Only one option must be correct.
4. correct_answer must contain only A, B, C, or D.
5. Write a real explanation for every answer.
6. Do not use placeholder text.
7. Do not add any extra keys.

Return valid JSON using this structure:

{{
    "questions": [
        {{
            "question": "Write an actual question",
            "options": {{
                "A": "Option A",
                "B": "Option B",
                "C": "Option C",
                "D": "Option D"
            }},
            "correct_answer": "A",
            "explanation": "Explain why A is correct"
        }}
    ]
}}

Study Material:
{text_chunk}
"""
    response = ollama.chat(                        # ai ko prompt bhejta hai
    model="llama3.2:1b",                           # hmara downloaded ai model
    format = "json" ,                                                
    messages=[                                     # ai ko instructions
        {"role": "user", "content": prompt}
    ]
)
    
    questions = json.loads(response.message.content)

    return questions