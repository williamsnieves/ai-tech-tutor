import express from "express";
import tutorRoutes from "./routes/tutorRoutes";
import dotenv from "dotenv";

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());

// Routes
app.use("/api/tutor", tutorRoutes);

app.get("/", (req, res) => {
  res.send("🤖 AI Tutor API is running!");
});

export default app;
