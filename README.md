# Instructions to Candidates

- You have **90 minutes** to complete 1 design question
- Use any LLM or AI coding assistant of your choice to help you build the application
- Your goal is to have the application running locally in your IDE
- Be creative about how you want to demo your application to the interviewer

# Boostly — boost morale, one kudos at a time

Build a working application that enables college students to recognize their peers, allocate monthly credits, and redeem earned rewards. The platform should encourage appreciation and engagement across student communities — a simple, transparent system for celebrating contributions and converting recognition into tangible value.

Use any language, framework, or database (e.g., Flask/FastAPI, Express, Spring Boot, Django, Go, etc.) of your choice.

## Core Functionality

### 1. Recognition
Allows one student to recognize another and transfer a certain number of credits.

**Business Rules:**
- Each student receives **100 credits every month** (reset at the start of each calendar month)
- Students **cannot send credits to themselves** (self-recognition is not allowed)
- Each student has a **monthly sending limit of 100 credits** (per calendar month)
- A student cannot send more credits than they currently have in their balance
- A student cannot exceed their monthly sending limit

### 2. Endorsements
Enables students to endorse an existing recognition entry (like/cheer).

**Business Rules:**
- Each endorser can endorse a recognition entry **only once**
- Endorsements are just a count — they don't affect credit balances or any other functionality

### 3. Redemption
Lets students redeem the credits they've received.

**Business Rules:**
- Credits are converted into a fixed-value voucher at **₹5 per credit**
- When credits are redeemed, they are **permanently deducted** from the student's balance
- A student can only redeem credits they have received

## Deliverables

### Folder Structure
Organize your submission using the following folder structure in your GitHub repository:

```
your-repository/
├── src/                           # All source code goes here
│   └── readme.md                  # Project documentation (setup, API endpoints, etc.)
├── prompt/                        # LLM chat exports go here
│   └── llm-chat-export.txt        # Exported LLM/AI assistant conversations
├── test-cases/                    # Test cases documentation goes here
│   └── test-cases.txt             # Documentation on how to run each use case
└── README.md                      # Project README (optional, can include assignment context)
```

### Required Files

1. **Complete source code** in the `src/` folder

2. **readme.md** in the `src/` folder with:
   - Setup instructions
   - Run instructions
   - API endpoints documentation
   - Sample requests and responses


3. **LLM Chat Export** - Update `prompt/llm-chat-export.txt`:
   - If you used LLMs/AI assistants, paste your complete exported conversation in this file
   - Replace the placeholder content with your actual LLM chat export

4. **Test Cases Documentation** - Update `test-cases/test-cases.txt`:
   - Document how to run each use case from the problem (Recognition, Endorsements, Redemption)
   - For each core functionality, include:
     - How to test the feature
     - Steps to execute the test
     - Expected results
   - Replace the placeholder content with your test case documentation

---

# How to Submit Your Assignment

Follow these steps to submit your completed assignment:

1. **Create a private GitHub repository** with the following naming format:
   ```
   firstname-lastname-collegeid
   ```
   Example: `john-doe-2024CS001`
   
   - Go to GitHub and create a new repository
   - **Make it private** (not public)
   - Initialize with a README if you want, or start with an empty repository

2. **Organize your files** according to the folder structure specified in the Deliverables section:
   - Place all source code in the `src/` folder
   - Update `src/readme.md` with your project documentation
   - Update `prompt/llm-chat-export.txt` with your LLM chat export (if applicable)
   - Update `test-cases/test-cases.txt` with your test case documentation

3. **Ensure all required files** are included:
   - Complete source code in `src/`
   - `src/readme.md` updated with setup, run instructions, and API documentation
   - Sample requests (cURL/Postman) with example responses (can be in `src/readme.md`)
   - `prompt/llm-chat-export.txt` updated with your LLM chat export (if you used LLMs)
   - `test-cases/test-cases.txt` updated with documentation on how to run each use case

4. **Verify your application** runs locally and is ready to demo

5. **Commit and push** your code to your GitHub repository:
   ```bash
   git add .
   git commit -m "Initial submission"
   git push -u origin main
   ```

6. **Add the interviewer as a collaborator and confirm access**:
   - Go to your repository's **Settings** → **Collaborators**
   - Click **Add people**
   - Search for the interviewer's GitHub username and add them with **Read** access
   - The interviewer's GitHub username will be provided separately
   - Ensure the interviewer has been added and can access your repository

---

***Remember: You are using LLMs and they hallucinate. Your ability to explain the code, think logically, and design effectively will be the key focus.***

***Good Luck!***
