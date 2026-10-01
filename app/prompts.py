LESSON_PROMPT = """
You are an AI personalized learning agent.

Create a concise and useful lesson.

Topic: {topic}
Learner Level: {level}
Learning Goal: {learning_goal}

Requirements:

- Keep the lesson concise.
- Use simple language.
- Explain the core concept.
- Include 3 to 5 important points.
- Include 1 practical example.
- Include 1 real-world use case.
- Include 2 short practice questions.
- Adapt the content to the learner level.
- Adapt the content to the learning goal.

Learning Goal Rules:

Interview Preparation:
Focus on interview concepts, important questions,
and practical understanding.

Project Development:
Focus on implementation, workflow,
and practical project usage.

Exam Preparation:
Focus on definitions, important concepts,
formulas where relevant, and exam-style questions.

Skill Development:
Focus on fundamentals, practical usage,
examples, and exercises.

IMPORTANT:
Keep the lesson under approximately 500 words.

Return only the lesson.
"""


QUIZ_PROMPT = """
You are an AI personalized educational assessment agent.

Create a quiz based on the lesson below.

Topic: {topic}
Learner Level: {level}
Learning Goal: {learning_goal}

Lesson:
{lesson}

Create exactly 5 multiple-choice questions.

The questions must match:
- Topic
- Learner level
- Learning goal
- Lesson

Use exactly this format:

Question 1: Write the question
A) First option
B) Second option
C) Third option
D) Fourth option
Correct Answer: A

Question 2: Write the question
A) First option
B) Second option
C) Third option
D) Fourth option
Correct Answer: B

Question 3: Write the question
A) First option
B) Second option
C) Third option
D) Fourth option
Correct Answer: C

Question 4: Write the question
A) First option
B) Second option
C) Third option
D) Fourth option
Correct Answer: D

Question 5: Write the question
A) First option
B) Second option
C) Third option
D) Fourth option
Correct Answer: A

IMPORTANT RULES:

- Use exactly A), B), C), D)
- Use exactly Correct Answer: A/B/C/D
- Do not use markdown.
- Do not add explanations.
- Keep questions concise.
- Do not add any extra text.
"""