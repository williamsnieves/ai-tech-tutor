# 🚀 AI Tech Tutor - TypeScript Backend (Express.js)

This is the **TypeScript backend** for AI Tech Tutor, built with **Express.js, OpenAI API, and TypeScript**.

## 🚀 Getting Started

### 1️⃣ Install Dependencies
```bash
cd src/backend/typescript
npm install
```

### 2️⃣ Set Up API Keys

OPENAI_API_KEY=your-openai-key-here

### 3️⃣ Run the Server

```bash
npx ts-node src/server.ts
```

### 4️⃣ Test API (Example)

```bash
curl -X POST http://localhost:3000/api/tutor \
     -H "Content-Type: application/json" \
     -d '{"query": "What is recursion?", "isCode": false, "language": "English"}'
```

### 📂 Project Structure

typescript/
│── src/
│   ├── controllers/       # API controllers
│   ├── services/          # AI logic
│   ├── utils/             # Helper functions
│   ├── config/            # Environment settings
│   ├── routes/            # API routes
│   ├── app.ts             # Express setup
│   ├── server.ts          # Server entry point
│── .env
│── package.json
│── tsconfig.json
│── README.md
