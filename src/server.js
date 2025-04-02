import express from "express";
import { createServer } from "http";
import { Server } from "socket.io";
import cors from "cors";
import path from "path";
import { fileURLToPath } from "url";
import { dotenvConfig } from "./configs/env.config.js";
import router from "./routes/route.js";

const PORT = dotenvConfig.PORT;
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const server = createServer(app);
export const io = new Server(server, {
  cors: {
    origin: dotenvConfig.FRONTEND_ORIGIN,
    credentials: true,
    methods: ["POST"],
  },
});

app.use(cors());
app.use(express.json());

// Serve downloaded video files from the "temp" directory
app.use("/temp", express.static(path.join(__dirname, "../temp")));

// routes
app.use("/api/v1", router);

server.listen(PORT, () => {
  console.log(`Server is running on port: ${PORT}`);
});
