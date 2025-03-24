from bardapi import Bard
import json

# Set Bard API key
BARD_API_KEY = "g.a000uQjr2geasosZbndACDSmPdMWNWliPGApTFrARHHsaKq67kZ9srRC1fEE-f65Go4WOnZuTAACgYKAYcSARISFQHGX2MipvZ33vPn9Vo8o809cyr4pBoVAUF8yKpCJN2XIimnHgdzUTN4O7C20076"

# Initialize the Bard API
bard = Bard(token=BARD_API_KEY)

def generate_interview_qa(topic, num_questions=10):
    """Generate interview questions and answers using Bard API."""
    qa_pairs = []
    prompt = f"Generate {num_questions} short interview questions and answers about {topic} in point form."
    try:
        response = bard.get_answer(prompt)
        print("Raw API Response:", response)  # Debugging line
        if response and 'content' in response:
            generated_text = response['content']
            print("Generated Text:", generated_text)  # Debugging line
            qa_pairs = generated_text.strip().split("\n\n")  # Split into individual Q&A pairs
        else:
            print("Invalid response from Bard API.")
    except Exception as e:
        print(f"Error generating questions: {e}")
    return qa_pairs

# Example usage
if __name__ == "__main__":
    topic = "Python programming"
    qa_pairs = generate_interview_qa(topic, num_questions=15)
    print("QA Pairs:", qa_pairs)  # Debugging line
    
    # Format the data
    formatted_data = []
    for qa in qa_pairs:
        try:
            # Ensure the generated text contains both question and answer
            if "Question:" in qa and "Answer:" in qa:
                question = qa.split("Question:")[1].split("Answer:")[0].strip()
                answer = qa.split("Answer:")[1].strip()
                formatted_data.append({
                    "context": question,
                    "answer": answer,
                })
            else:
                print(f"Skipping malformed QA pair: {qa}")
        except Exception as e:
            print(f"Error formatting data: {e}")
    
    # Print the formatted data
    print("Formatted Data:", json.dumps(formatted_data, indent=4))