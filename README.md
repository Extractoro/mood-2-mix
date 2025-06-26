# Mood2Mix 🎧

Full-stack FastAPI-based service that analyzes the user’s emotional prompt using GPT and recommends music tracks accordingly. It integrates with YouTube Music and Spotify to recommend or create playlists, using OpenAI, ytmusicapi, and Spotify Web API. Async-ready, Dockerized, and structured for scalability.

## Table of Contents

* [✨ Features](#-features)
* [🛠 Project Structure](#-project-structure)
* [⚙️ Getting Started](#-getting-started)

  * [1. Clone the Repository](#1-clone-the-repository)
  * [2. Configure Environment](#2-configure-environment)
  * [3. Run with Docker](#3-run-with-docker)
* [🧪 Testing](#-testing)
* [📊 API Endpoints](#-api-endpoints)

  * [🎭 Mood Analysis](#-mood-analysis)
  * [🎵 Recommendations](#-recommendations)
  * [🎧 Spotify Integration](#-spotify-integration)
* [🔍 Interactive Docs](#-interactive-docs)

## ✨ Features

* 🎭 Analyze free-form emotional text using OpenAI (GPT-4o)
* 📈 Extract mood, valence, energy, genres, and a music query
* 🎶 Recommend music from YouTube Music and/or Spotify
* 🧠 GPT-based intelligent search query generation
* ✅ Async FastAPI backend with exception handling
* 🎧 Spotify playlist creation & track addition support
* 🛠 Dockerized environment
* 🔑 OAuth 2.0 authentication for Spotify
* 🔍 Swagger + ReDoc interactive documentation

## 🛠 Project Structure

```
🔹 gpt/
🔹 └── mood_analyzer.py        # GPT prompt logic
🔹 music_providers/
🔹 ├── base.py                 # Abstract music provider
🔹 ├── spotify.py              # Spotify integration
🔹 └── ytmusic.py              # YouTube Music integration
🔹 routes/
🔹 ├── mood.py                 # Mood analysis routes
🔹 ├── recommend.py            # Song recommendation endpoint
🔹 └── spotify.py              # Spotify-related endpoints
🔹 utils/
🔹 ├── get_spotify_token_from_header.py  # Extract Bearer token
🔹 └── spotify_list_ids.py               # Map tracks to Spotify URIs
🔹 schemas/
🔹 ├── schemas.py              # Pydantic models
🔹 └── enums.py                # Enum for music providers
🔹 .env
🔹 docker-compose.yml
🔹 Dockerfile
🔹 README.md
```

## ⚙️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Extractoro/mood-2-mix.git
cd mood2mix
```

### 2. Configure Environment

Create a `.env` file:

```
OPENAI_API_KEY=your_openai_key
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_USER_ID=your_user_id
REDIRECT_URI=http://127.0.0.1:8000/callback
```

### 3. Run with Docker

```bash
docker-compose up --build
```

## 🧪 Testing

```bash
pytest/tests
flake8 .
```

## 📊 API Endpoints

### 🎭 Mood Analysis

| Method | Endpoint                    | Description                     |
| ------ | --------------------------- | ------------------------------- |
| POST   | /mood/analyze               | Analyze emotional text          |
| POST   | /mood/analyze-and-recommend | Analyze and get recommendations |

### 🎵 Recommendations

| Method | Endpoint         | Description                    |
| ------ | ---------------- | ------------------------------ |
| POST   | /recommend/songs | Recommend songs from mood data |

### 🎧 Spotify Integration

| Method | Endpoint                       | Description                           |
| ------ | ------------------------------ | ------------------------------------- |
| GET    | /spotify/auth/link             | Get Spotify auth URL                  |
| GET    | /spotify/callback              | Exchange code for token               |
| POST   | /spotify/create-playlist       | Create a new playlist                 |
| POST   | /spotify/{playlist\_id}/tracks | Add tracks to a playlist              |
| POST   | /spotify/prompt-to-playlist    | Full flow: prompt → tracks → playlist |

## Moods examples
### 🎧 Example 1: Neutral, relaxing
> It was just an ordinary day. I had some coffee, did a bit of work, and enjoyed the quiet. No rush, no noise.

---

### 🎵 Example 2: Happy, uplifting
> Finally finished the project! It feels like a huge weight has been lifted. I’m so full of energy — I could jump for joy!

---

### 🌧 Example 3: Sad, melancholic
> Everything feels so empty. It’s been raining all day, and my thoughts keep drifting… I feel kind of lost.

---

### 😠 Example 4: Frustrated, tense
> I’m so fed up! These constant crashes and deadlines are driving me crazy. I just can’t deal with this mess anymore.

---

### 😌 Example 5: Calm, peaceful
> I sat by the window with a book while the setting sun filled the room with soft light. Total peace.


## 🔍 Interactive Docs

* Swagger → [http://localhost:8000/docs](http://localhost:8000/docs)
* ReDoc → [http://localhost:8000/redoc](http://localhost:8000/redoc)
