from flask import Flask, jsonify, render_template_string
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

# 🔹 Fungsi Scraping Anime dari Donghub.vip
def scrape_donghub():
    url = "https://donghub.vip/"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {"anime_list": []}

    soup = BeautifulSoup(response.text, "html.parser")
    anime_list = []

    for anime in soup.select(".bsx"):
        title = anime.select_one(".tt").text.strip()
        link = anime.select_one("a")["href"]
        thumbnail = anime.select_one("img")["src"]

        # 🔹 Ambil Episode Pertama (Opsional)
        first_episode = scrape_episodes(link)

        anime_list.append({
            "title": title,
            "link": link,
            "thumbnail": thumbnail,
            "first_episode": first_episode
        })

    return {"anime_list": anime_list}

# 🔹 Fungsi Scraping Episode Pertama
def scrape_episodes(anime_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(anime_url, headers=headers)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    episode_link = soup.select_one(".eplister li a")["href"] if soup.select_one(".eplister li a") else anime_url
    return episode_link

# 🔹 API untuk mendapatkan daftar anime dari Donghub.vip
@app.route("/api/anime", methods=["GET"])
def anime_api():
    return jsonify(scrape_donghub())

# 🔹 Frontend (Tampilan HTML + CSS + JavaScript)
@app.route("/")
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Rief Anime</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #121212; color: white; text-align: center; }
            .anime-container { display: flex; flex-wrap: wrap; justify-content: center; }
            .anime-card { width: 200px; margin: 10px; background: #1e1e1e; padding: 10px; border-radius: 8px; }
            .anime-card img { width: 100%; border-radius: 5px; }
            .anime-card h3 { font-size: 16px; margin: 10px 0; }
            .anime-card a { text-decoration: none; color: white; background: #ff6600; padding: 5px; display: block; margin-top: 5px; border-radius: 5px; }
            .anime-card a:hover { background: #ff4500; }
        </style>
    </head>
    <body>

        <h1>Rief Anime Streaming</h1>
        <div class="anime-container" id="anime-list"></div>

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
                                <a href="${anime.first_episode}" target="_blank">Tonton Episode 1</a>
                            `;
                            animeList.appendChild(card);
                        });
                    })
                    .catch(error => console.error("Gagal mengambil data:", error));
            });
        </script>

    </body>
    </html>
    """)

# 🔹 Jalankan Server Flask
if __name__ == "__main__":
    app.run(debug=True)
