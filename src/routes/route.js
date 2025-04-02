import express from "express";
import { requestHandler } from "../controllers/request.controller.js";

const router = express.Router();

router.post("/download", requestHandler);

export default router;
