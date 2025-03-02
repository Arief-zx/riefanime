from flask import Flask, render_template_string, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# 🔹 URL sumber data anime dari Donghub.vip (bisa diganti dengan scraping)
ANIME_SOURCE = "https://raw.githubusercontent.com/username/repo/main/anime.json"

# 🔹 Ambil data anime dari sumber (bisa dari JSON lokal atau scraping)
def get_anime_data():
    try:
        response = requests.get(ANIME_SOURCE)
        return response.json()
    except:
        return {"anime_list": []}

# 🔹 API untuk mendapatkan data anime
@app.route("/api/anime", methods=["GET"])
def anime_api():
    return jsonify(get_anime_data())

# 🔹 Frontend: Menampilkan halaman utama
@app.route("/")
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Donghub Clone</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #121212; color: white; text-align: center; }
            .anime-container { display: flex; flex-wrap: wrap; justify-content: center; }
            .anime-card { width: 200px; margin: 10px; background: #1e1e1e; padding: 10px; border-radius: 8px; }
            .anime-card img { width: 100%; border-radius: 5px; }
            .anime-card h3 { font-size: 16px; margin: 10px 0; }
            .anime-card button { background: #ff6600; color: white; border: none; padding: 5px; cursor: pointer; }
            .anime-card button:hover { background: #ff4500; }
            #video-modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); }
            #video-modal video { width: 90%; max-width: 800px; margin-top: 10%; }
            #close-btn { color: white; font-size: 30px; position: absolute; top: 10px; right: 20px; cursor: pointer; }
        </style>
    </head>
    <body>

        <h1>Anime Streaming</h1>
        <div class="anime-container" id="anime-list"></div>

        <div id="video-modal">
            <span id="close-btn">&times;</span>
            <video id="anime-video" controls></video>
        </div>

        <script>
            document.addEventListener("DOMContentLoaded", function () {
                fetch("/api/anime")
                    .then(response => response.json())
                    .then(data => {
                        let animeList = document.getElementById("anime-list");
                        data.anime_list.forEach(anime => {
                            let card = document.createElement("div");
                            card.className = "anime-card";
                            card.innerHTML = `
                                <img src="${anime.thumbnail}" alt="${anime.title}">
                                <h3>${anime.title}</h3>
                                <button onclick="playVideo('${anime.video_url}')">Tonton</button>
                            `;
                            animeList.appendChild(card);
                        });
                    })
                    .catch(error => console.error("Gagal mengambil data:", error));
            });

            function playVideo(url) {
                let modal = document.getElementById("video-modal");
                let video = document.getElementById("anime-video");
                video.src = url;
                modal.style.display = "block";
            }

            document.getElementById("close-btn").addEventListener("click", function () {
                document.getElementById("video-modal").style.display = "none";
            });
        </script>

    </body>
    </html>
    """)

# 🔹 Jalankan server
if __name__ == "__main__":
    app.run(debug=True)
