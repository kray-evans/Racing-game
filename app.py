import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Cartoon Racing Game", page_icon="🚗", layout="centered")

st.title("🚗 Cartoon Racing - Phiên bản Hoạt Hình Vui Nhộn")
st.markdown("Đồ họa hoạt hình tươi sáng! Chơi mượt mà trên **PC** (`A`/`D`, mũi tên) và **Mobile** (nút ảo).")

game_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            margin: 0;
            background: #2b1055;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-family: 'Comic Sans MS', 'Bubblegum Sans', 'Segoe UI', cursive, sans-serif;
            color: white;
            overflow: hidden;
        }
        #game-container {
            position: relative;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5);
            border-radius: 20px;
            overflow: hidden;
            border: 4px solid #ff758c;
        }
        canvas {
            background: #512b58;
            display: block;
        }
        #ui {
            position: absolute;
            top: 12px;
            left: 20px;
            right: 20px;
            display: flex;
            justify-content: space-between;
            font-size: 20px;
            font-weight: bold;
            text-shadow: 2px 2px 0px #000;
            pointer-events: none;
            color: #ffeb3b;
        }
        .controls {
            margin-top: 15px;
            display: flex;
            gap: 20px;
            justify-content: center;
        }
        button {
            padding: 14px 32px;
            font-size: 16px;
            font-family: 'Comic Sans MS', cursive, sans-serif;
            font-weight: bold;
            background: linear-gradient(135deg, #ff758c, #ff7eb3);
            color: white;
            border: none;
            border-radius: 40px;
            cursor: pointer;
            box-shadow: 0 6px 20px rgba(255, 117, 140, 0.5);
            transition: 0.1s;
            user-select: none;
            -webkit-user-select: none;
        }
        button:active {
            transform: scale(0.92);
        }
        .audio-control {
            margin-top: 8px;
            font-size: 13px;
            color: #d8b4fe;
        }
    </style>
</head>
<body>
    <div id="game-container">
        <div id="ui">
            <div>⭐ ĐIỂM: <span id="score">0</span></div>
            <div>🚀 TỐC ĐỘ: <span id="speed">5</span>x</div>
        </div>
        <canvas id="gameCanvas" width="400" height="500"></canvas>
    </div>
    
    <div class="controls">
        <button id="leftBtn">👈 TRÁI</button>
        <button id="rightBtn">PHẢI 👉</button>
    </div>
    <div class="audio-control">🎵 Nhạc nền hoạt hình (Click màn hình để bật nhạc)</div>

    <audio id="bgMusic" loop>
        <source src="https://opengameart.org/sites/default/files/Preview_3_3.mp3" type="audio/mp3">
    </audio>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const scoreElement = document.getElementById("score");
        const speedElement = document.getElementById("speed");
        const bgMusic = document.getElementById("bgMusic");

        window.addEventListener('click', () => {
            if (bgMusic.paused && !gameOver) {
                bgMusic.play().catch(e => console.log("Audio play blocked"));
            }
        }, { once: true });

        let score = 0;
        let gameOver = false;
        let gameSpeed = 5;

        let player = {
            x: 180,
            y: 380,
            width: 44,
            height: 75,
            color: "#ff6b6b",
            speed: 7
        };

        let enemies = [];
        let roadOffset = 0;
        let particles = [];
        let keys = {};

        window.addEventListener("keydown", (e) => { keys[e.key] = true; });
        window.addEventListener("keyup", (e) => { keys[e.key] = false; });

        const leftBtn = document.getElementById("leftBtn");
        const rightBtn = document.getElementById("rightBtn");

        let movingLeft = false;
        let movingRight = false;

        leftBtn.addEventListener("mousedown", () => { movingLeft = true; });
        leftBtn.addEventListener("mouseup", () => { movingLeft = false; });
        leftBtn.addEventListener("touchstart", (e) => { e.preventDefault(); movingLeft = true; });
        leftBtn.addEventListener("touchend", (e) => { e.preventDefault(); movingLeft = false; });

        rightBtn.addEventListener("mousedown", () => { movingRight = true; });
        rightBtn.addEventListener("mouseup", () => { movingRight = false; });
        rightBtn.addEventListener("touchstart", (e) => { e.preventDefault(); movingRight = true; });
        rightBtn.addEventListener("touchend", (e) => { e.preventDefault(); movingRight = false; });

        canvas.addEventListener("click", (e) => {
            if (gameOver) {
                const rect = canvas.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                if (x >= canvas.width / 2 - 80 && x <= canvas.width / 2 + 80 &&
                    y >= canvas.height / 2 + 35 && y <= canvas.height / 2 + 80) {
                    resetGame();
                }
            }
        });

        function resetGame() {
            score = 0;
            gameSpeed = 5;
            enemies = [];
            particles = [];
            player.x = 180;
            gameOver = false;
            bgMusic.currentTime = 0;
            bgMusic.play().catch(e => console.log("Audio play blocked"));
        }

        function spawnEnemy() {
            let lanes = [45, 125, 210, 295];
            let laneX = lanes[Math.floor(Math.random() * lanes.length)];
            let colors = ["#4ecdc4", "#ffe66d", "#ff6b6b", "#a8dadc", "#ff9f43", "#a55eea"];
            let randomColor = colors[Math.floor(Math.random() * colors.length)];
            
            enemies.push({
                x: laneX,
                y: -100,
                width: 44,
                height: 75,
                color: randomColor
            });
        }

        let spawnTimer = 0;

        function update() {
            if (gameOver) return;

            if ((keys["ArrowLeft"] || keys["a"] || movingLeft) && player.x > 35) {
                player.x -= player.speed;
                particles.push({x: player.x + 15, y: player.y + 70, size: Math.random() * 6 + 3, alpha: 1});
            }
            if ((keys["ArrowRight"] || keys["d"] || movingRight) && player.x < canvas.width - 75) {
                player.x += player.speed;
                particles.push({x: player.x + 25, y: player.y + 70, size: Math.random() * 6 + 3, alpha: 1});
            }

            for (let i = particles.length - 1; i >= 0; i--) {
                particles[i].y += gameSpeed;
                particles[i].alpha -= 0.04;
                if (particles[i].alpha <= 0) particles.splice(i, 1);
            }

            roadOffset += gameSpeed;
            if (roadOffset > 40) roadOffset = 0;

            spawnTimer++;
            if (spawnTimer > 45) {
                spawnEnemy();
                spawnTimer = 0;
                score += 10;
                gameSpeed += 0.04;
            }

            for (let i = enemies.length - 1; i >= 0; i--) {
                enemies[i].y += gameSpeed;

                if (
                    player.x < enemies[i].x + enemies[i].width - 6 &&
                    player.x + player.width - 6 > enemies[i].x &&
                    player.y < enemies[i].y + enemies[i].height - 6 &&
                    player.y + player.height - 6 > enemies[i].y
                ) {
                    gameOver = true;
                    bgMusic.pause();
                }

                if (enemies[i].y > canvas.height) {
                    enemies.splice(i, 1);
                }
            }

            scoreElement.innerText = score;
            speedElement.innerText = gameSpeed.toFixed(1);
        }

        function drawCar(x, y, width, height, color, isPlayer = false) {
            ctx.save();
            
            ctx.fillStyle = color;
            ctx.beginPath();
            ctx.roundRect(x, y, width, height, 16);
            ctx.fill();

            ctx.fillStyle = "rgba(255, 255, 255, 0.35)";
            ctx.beginPath();
            ctx.roundRect(x + 4, y + 4, width - 8, height / 3, 10);
            ctx.fill();

            ctx.fillStyle = "#2d3436";
            ctx.beginPath();
            ctx.roundRect(x + 6, y + 16, width - 12, 18, 6);
            ctx.fill();

            ctx.beginPath();
            ctx.roundRect(x + 8, y + height - 20, width - 16, 10, 4);
            ctx.fill();

            ctx.fillStyle = "#2d3436";
            ctx.beginPath();
            ctx.roundRect(x - 6, y + 12, 6, 18, 3);
            ctx.roundRect(x + width, y + 12, 6, 18, 3);
            ctx.roundRect(x - 6, y + height - 24, 6, 18, 3);
            ctx.roundRect(x + width, y + height - 24, 6, 18, 3);
            ctx.fill();

            ctx.fillStyle = isPlayer ? "#ffeaa7" : "#fab1a0";
            ctx.beginPath();
            ctx.arc(x + 9, y + 4, 5, 0, Math.PI * 2);
            ctx.arc(x + width - 9, y + 4, 5, 0, Math.PI * 2);
            ctx.fill();

            if (isPlayer) {
                ctx.fillStyle = "#ff7675";
                ctx.beginPath();
                ctx.arc(x + 5, y + 32, 4, 0, Math.PI * 2);
                ctx.arc(x + width - 5, y + 32, 4, 0, Math.PI * 2);
                ctx.fill();
            }

            ctx.restore();
        }

        function draw() {
            ctx.fillStyle = "#3a1c71";
            ctx.fillRect(35, 0, canvas.width - 70, canvas.height);

            ctx.fillStyle = "#26de81";
            ctx.fillRect(0, 0, 35, canvas.height);
            ctx.fillRect(canvas.width - 35, 0, 35, canvas.height);

            let decHeight = 40;
            let decOffset = roadOffset % decHeight;
            for (let y = -decHeight; y < canvas.height + decHeight; y += decHeight) {
                ctx.fillStyle = "#20bf6b";
                ctx.fillRect(8, y + decOffset, 18, 12);
                ctx.fillRect(canvas.width - 26, y + decOffset, 18, 12);
            }

            ctx.strokeStyle = "#fff";
            ctx.lineWidth = 6;
            ctx.setLineDash([20, 20]);
            ctx.lineDashOffset = -roadOffset;
            
            ctx.beginPath();
            ctx.moveTo(canvas.width / 2, 0);
            ctx.lineTo(canvas.width / 2, canvas.height);
            ctx.stroke();
            ctx.setLineDash([]);

            for (let p of particles) {
                ctx.fillStyle = `rgba(255, 235, 59, ${p.alpha})`;
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
                ctx.fill();
            }

            drawCar(player.x, player.y, player.width, player.height, player.color, true);

            for (let enemy of enemies) {
                drawCar(enemy.x, enemy.y, enemy.width, enemy.height, enemy.color, false);
            }

            if (gameOver) {
                ctx.fillStyle = "rgba(43, 16, 85, 0.92)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                ctx.fillStyle = "#ff6b6b";
                ctx.font = "bold 34px 'Comic Sans MS', cursive, sans-serif";
                ctx.textAlign = "center";
                ctx.fillText("💥 ÔI KHÔNG! 💥", canvas.width / 2, canvas.height / 2 - 45);
                
                ctx.fillStyle = "#ffe66d";
                ctx.font = "bold 20px 'Comic Sans MS', cursive, sans-serif";
                ctx.fillText("Điểm của bạn: " + score, canvas.width / 2, canvas.height / 2 - 5);
                
                ctx.fillStyle = "#ff758c";
                ctx.beginPath();
                ctx.roundRect(canvas.width / 2 - 80, canvas.height / 2 + 30, 160, 48, 24);
                ctx.fill();

                ctx.fillStyle = "#ffffff";
                ctx.font = "bold 18px 'Comic Sans MS', cursive, sans-serif";
                ctx.fillText("CHƠI LẠI 🚗", canvas.width / 2, canvas.height / 2 + 60);
            }
        }

        function loop() {
            update();
            draw();
            requestAnimationFrame(loop);
        }

        loop();
    </script>
</body>
</html>
"""

components.html(game_code, height=630, scrolling=False)

