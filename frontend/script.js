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

    // Clear the questions list
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
        displayQuestions(data.questions);
    } catch (error) {
        alert(error.message);
        questionsList.innerHTML = "";
    }
});

// Function to display questions in the UI
function displayQuestions(questions) {
    questionsList.innerHTML = "";
    if (questions.length === 0) {
        questionsList.innerHTML = "<div class='question-card'>No questions available.</div>";
        return;
    }

    questions.forEach((q) => {
        const card = document.createElement("div");
        card.className = "question-card";
        card.innerHTML = `
            <strong>Q:</strong> ${q.context} 
            <br>
            <strong>A:</strong> ${q.answer}
        `;
        questionsList.appendChild(card);
    });
}