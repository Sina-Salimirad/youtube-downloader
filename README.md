# YouTube Downloader API

A powerful and efficient YouTube video downloader API that supports both single video and playlist downloads. This project is built using Node.js, Express, Python (yt-dlp), and Socket.IO for real-time updates.

## Features 🚀
- ✅ Download individual videos and playlists
- ✅ Real-time progress updates via WebSocket
- ✅ Automatic file deletion after a specified time
- ✅ Docker support for easy deployment
- ✅ Open Source under MIT License

## Tech Stack 🛠️
- **Backend:** Node.js, Express, Python (yt-dlp)
- **Real-time Updates:** Socket.IO
- **Containerization:** Docker
- **Deployment:** Railway (Free Plan)

---

## Installation 🔧

### Prerequisites
Ensure you have the following installed on your system:
- Node.js (v18 or higher)
- Python 3
- FFmpeg (required for merging audio & video)
- Docker (optional, for containerized deployment)

### Local Setup ⚙️
```sh
# Clone the repository
git clone https://github.com/Sina-Salimirad/youtube-downloader-backend.git
cd your-repo

# Install Node.js dependencies
npm install

# Install Python dependencies
pip install -r requirements.txt  # if using a virtual environment

# Create an .env file
cp .env.example .env
```

### Running the Server 🚀
```sh
node src/server.js
```

### Running with Docker 🐳
```sh
docker build -t youtube-downloader .
docker run -p 8080:8080 youtube-downloader
```

---

## API Usage 📡

### Download a Video 🎥
```
POST /api/v1/download
Content-Type: application/json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "clientId": "unique-client-id"
}
```

### Real-time Progress Updates ⚡
- Connect to `ws://your-server:PORT` using Socket.IO
- Listen for `download_status` event

Example response:
```json
{
  "status": "Downloading",
  "data": {
    "title": "Video Title",
    "file_size": 1048576,
    "downloaded": 524288,
    "percent": "50%",
    "speed": "1.2 MB/s",
    "eta": "10s"
  }
}
```

---

## Environment Variables 🌍
The following variables should be set in a `.env` file:
```env
PORT=8080
RAILWAY_APP_URL="your-railway-url"
FRONTEND_ORIGIN="http://localhost:5173"
```

---

## Frontend 🎨
The frontend for this project is developed separately and available at [Youtube-downloader-GUI](https://github.com/Sina-Salimirad/Youtube-downloader-GUI).

---

## License 📜
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing 🤝
Contributions are welcome! Feel free to submit issues or pull requests to improve the project.

---

## Author ✨
Developed and maintained by **Sina Salimirad**. Follow me for more awesome projects!

