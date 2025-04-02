FROM node:18

WORKDIR /app

# Copy package.json and package-lock.json first for better caching
COPY package*.json ./

# Install Nodejs dependencies
RUN npm install

# Copy all project files to the container
COPY . .

# Install Python, FFmpeg, and set up a virtual environment for dependencies
RUN apt-get update && apt-get install -y python3 python3-venv python3-pip ffmpeg
RUN python3 -m venv venv /app/venv

# Copy requirements.txt file to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Install Python dependencies in virtual environment
RUN . /app/venv/bin/activate && pip install -U yt-dlp 

# Store downloaded videos in the "temp" directory
RUN mkdir -p /app/temp

# Expose the port (Railway automatically assigns PORT)
EXPOSE 8080

# Start the server
CMD ["node", "src/server.js"]