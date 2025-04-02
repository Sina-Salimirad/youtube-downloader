import dotenv from "dotenv";

dotenv.config();

export const dotenvConfig = {
  PORT: process.env.PORT || 5000,
  RAILWAY_APP_URL: process.env.RAILWAY_APP_URL || "localhost://5000",
  FRONTEND_ORIGIN: process.env.FRONTEND_ORIGIN || "*",
};