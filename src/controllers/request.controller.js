import { spawn } from "child_process";
import { io } from "../server.js";

export const requestHandler = (req, res) => {
  const { url, clientId } = req.body;

  if (!url || !clientId)
    return res.status(400).json({ error: "No URL or clientId provided" });

  const pythonProcess = spawn("/app/venv/bin/python3", [
    "src/scripts/main.py",
    url,
  ]);

  pythonProcess.stderr.on("data", (data) => {
    console.error(`Python stderr: ${data.toString()}`);
  });

  pythonProcess.stdout.on("data", (data) => {
    const message = data.toString().trim().split("\n");

    message.forEach((message) => {
      try {
        const parsedMessage = JSON.parse(message);
        io.to(clientId).emit("download_status", parsedMessage); // Send real-time download status updates to the client
      } catch (err) {
        console.error("Error parsing JSON:", err.message);
      }
    });
  });

  res.json({ success: true, message: "Download started", clientId });
};
