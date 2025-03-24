const generateBtn = document.getElementById("generate-btn");
const topicInput = document.getElementById("topic");
const questionsList = document.getElementById("questions-list");

// Backend API URL
const generateUrl = "http://127.0.0.1:5000/generate";

// Function to generate questions
generateBtn.addEventListener("click", async () => {
    const topic = topicInput.value.trim();
    if (!topic) {
        alert("Please enter a topic.");
        return;
    }

    // Clear the questions list and show loading state
    questionsList.innerHTML = "<div class='question-card'>Loading...</div>";

    try {
        const response = await fetch(generateUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ topic }),
        });

        if (!response.ok) {
            throw new Error("Failed to generate questions.");
        }

        const data = await response.json();
        console.log("Backend Response:", data); // Debugging line
        displayQuestions(data.questions);
    } catch (error) {
        console.error("Error fetching questions:", error); // Debugging line
        alert("An error occurred while generating questions. Please try again.");
        questionsList.innerHTML = "<div class='question-card'>Failed to load questions.</div>";
    }
});

// Function to display questions in the UI
function displayQuestions(questions) {
    questionsList.innerHTML = "";
    if (!questions || !Array.isArray(questions) || questions.length === 0) {
        questionsList.innerHTML = "<div class='question-card'>No questions available.</div>";
        return;
    }

    questions.forEach((q) => {
        const card = document.createElement("div");
        card.className = "question-card";

        // Create a separate box for the question
        const questionBox = document.createElement("div");
        questionBox.className = "question-box";
        questionBox.innerHTML = `<strong>Q:</strong> ${q.context}`;

        // Create a separate box for the answer
        const answerBox = document.createElement("div");
        answerBox.className = "answer-box";
        answerBox.innerHTML = `<strong>A:</strong> ${q.answer}`;

        // Append the question and answer boxes to the card
        card.appendChild(questionBox);
        card.appendChild(answerBox);

        // Append the card to the questions list
        questionsList.appendChild(card);
    });
}

