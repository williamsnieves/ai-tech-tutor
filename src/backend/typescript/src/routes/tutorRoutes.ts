import express from "express";
import { tutorHandler } from "../controllers/tutorController";

const router = express.Router();

router.post("/", tutorHandler);

export default router;
