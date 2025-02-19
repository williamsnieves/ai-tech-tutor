import { OpenAI } from "openai";
import { ChatCompletionMessageParam } from "openai/resources/index";
import dotenv from "dotenv";

dotenv.config();

const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
const MODEL_GPT = "gpt-4o-mini";

if (!OPENAI_API_KEY) {
  throw new Error("❌ Missing OPENAI_API_KEY in .env file");
}

// Initialize OpenAI Client
const openai = new OpenAI({ apiKey: OPENAI_API_KEY });

// System prompt (Identical to Python version)
const systemPrompt = `You are an expert tutor in technology and programming. 
Your role is to provide clear and structured explanations in Markdown format about:
- Programming concepts and best practices.
- Code snippets provided by the user, including their functionality and possible optimizations.
- General technology topics, including AI, software development, networking, hardware, and emerging technologies.
- Comparisons between technologies, frameworks, or programming paradigms.
- Recommendations on tools, best practices, and industry trends.
Your responses must be **structured, educational, and formatted in Markdown**. 
Use headings, bullet points, code blocks, and bold/italic text where appropriate.`;

// User prompt function (Identical to Python version)
const userPromptFor = (
  query: string,
  isCode: boolean,
  language: string
): string => {
  if (isCode) {
    return (
      `I will provide you with a code snippet written in ${language}. Your task is to explain it in detail in **Markdown format**, including what it does and why it works.\n\n` +
      `**Code:**\n\`\`\`${language}\n${query}\n\`\`\`\n\n` +
      "Please provide a structured breakdown of its functionality and suggest any improvements if applicable. Also, explain key concepts that would help me understand the code better."
    );
  } else {
    return (
      `I have a question about technology. Please provide your response in **Markdown format**.\n\n` +
      `**Question:** ${query}\n\n` +
      "Please structure your response clearly using **headings, bullet points, and examples** where appropriate."
    );
  }
};

// Generate messages (Identical to Python version)
const messagesFor = (
  query: string,
  isCode: boolean,
  language: string
): ChatCompletionMessageParam[] => [
  { role: "system", content: systemPrompt },
  { role: "user", content: userPromptFor(query, isCode, language) },
];

// Get AI Response from OpenAI (Using the Python-equivalent prompt)
export const getExplanation = async (
  query: string,
  isCode: boolean,
  language: string
): Promise<string> => {
  try {
    const response = await openai.chat.completions.create({
      model: MODEL_GPT,
      messages: messagesFor(query, isCode, language),
    });

    return response.choices[0].message.content || "No response from OpenAI";
  } catch (error) {
    console.error("Error fetching response from OpenAI:", error);
    throw new Error("Failed to fetch AI response");
  }
};
