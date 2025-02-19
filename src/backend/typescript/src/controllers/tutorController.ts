import { Request, Response } from "express";
import { getExplanation } from "../services/tutorService";

export const tutorHandler = async (
  req: Request,
  res: Response
): Promise<void> => {
  try {
    const { query, isCode, language } = req.body;

    if (!query) {
      res.status(400).json({ error: "Query is required" });
      return;
    }

    const response = await getExplanation(query, isCode, language);

    // Ensure a valid JSON response is sent
    res.status(200).json({ response });
  } catch (error) {
    console.error("Error in tutorHandler:", error);
    res.status(500).json({ error: "Internal Server Error" });
  }
};
