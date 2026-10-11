import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Retro Racing Game", page_icon="🏎️", layout="centered")

st.title("🏎️ Mini Retro Racing Game")
st.markdown("Sử dụng bàn phím trên máy tính hoặc bấm các nút **Trái / Phải** bên dưới nếu chơi trên điện thoại!")

game_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            margin: 0;
            background: #111;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-family: Arial, sans-serif;
            color: white;
            overflow: hidden;
        }
        canvas {
            border: 4px solid #fff;
            box-shadow: 0 0 20px rgba(255, 255, 255, 0.5);
            background: #333;
            max-width: 100%;
            height: auto;
        }
        #ui {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .controls {
            margin-top: 10px;
            display: flex;
            gap: 20px;
            justify-content: center;
        }
        button {
            padding: 15px 30px;
            font-size: 18px;
            font-weight: bold;
            background: #ff4757;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            user-select: none;
            -webkit-user-select: none;
        }
        button:active {
            background: #ff6b81;
        }
    </style>
</head>
<body>
    <div id="ui">Điểm: <span id="score">0</span></div>
    <canvas id="gameCanvas" width="400" height="500"></canvas>
    
    <div class="controls">
        <button id="leftBtn">◀ TRÁI</button>
        <button id="rightBtn">PHẢI ▶</button>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const scoreElement = document.getElementById("score");

        let score = 0;
        let gameOver = false;
        let gameSpeed = 5;

        let player = {
            x: 180,
            y: 380,
            width: 40,
            height: 70,
            color: "#ff4757",
            speed: 7
        };

        let enemies = [];
        let roadLinesOffset = 0;
        let keys = {};

        // Bắt sự kiện bàn phím máy tính
        window.addEventListener("keydown", (e) => { keys[e.key] = true; });
        window.addEventListener("keyup", (e) => { keys[e.key] = false; });

        // Bắt sự kiện cảm ứng / click cho nút mobile
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

        function spawnEnemy() {
            let lanes = [40, 120, 200, 280];
            let laneX = lanes[Math.floor(Math.random() * lanes.length)];
            enemies.push({
                x: laneX,
                y: -100,
                width: 40,
                height: 70,
                color: "#2ed573"
            });
        }

        let spawnTimer = 0;

        function update() {
            if (gameOver) return;

            // Xử lý di chuyển (bàn phím hoặc nút cảm ứng)
            if ((keys["ArrowLeft"] || keys["a"] || movingLeft) && player.x > 30) {
                player.x -= player.speed;
            }
            if ((keys["ArrowRight"] || keys["d"] || movingRight) && player.x < canvas.width - 70) {
                player.x += player.speed;
            }

            roadLinesOffset += gameSpeed;
            if (roadLinesOffset > 40) roadLinesOffset = 0;

            spawnTimer++;
            if (spawnTimer > 45) {
                spawnEnemy();
                spawnTimer = 0;
                score += 10;
                gameSpeed += 0.05;
            }

            for (let i = enemies.length - 1; i >= 0; i--) {
                enemies[i].y += gameSpeed;

                if (
                    player.x < enemies[i].x + enemies[i].width &&
                    player.x + player.width > enemies[i].x &&
                    player.y < enemies[i].y + enemies[i].height &&
                    player.y + player.height > enemies[i].y
                ) {
                    gameOver = true;
                }

                if (enemies[i].y > canvas.height) {
                    enemies.splice(i, 1);
                }
            }

            scoreElement.innerText = score;
        }

        function drawCar(x, y, width, height, color) {
            ctx.fillStyle = color;
            ctx.fillRect(x, y, width, height);
            ctx.fillStyle = "#000";
            ctx.fillRect(x - 6, y + 10, 6, 15);
            ctx.fillRect(x + width, y + 10, 6, 15);
            ctx.fillRect(x - 6, y + height - 25, 6, 15);
            ctx.fillRect(x + width, y + height - 25, 6, 15);
            ctx.fillStyle = "#fffa65";
            ctx.fillRect(x + 5, y, 8, 4);
            ctx.fillRect(x + width - 13, y, 8, 4);
        }

        function draw() {
            ctx.fillStyle = "#555";
            ctx.fillRect(20, 0, canvas.width - 40, canvas.height);

            ctx.fillStyle = "#ff4757";
            ctx.fillRect(0, 0, 20, canvas.height);
            ctx.fillRect(canvas.width - 20, 0, 20, canvas.height);

            ctx.strokeStyle = "#fff";
            ctx.lineWidth = 4;
            ctx.setLineDash([20, 20]);
            ctx.lineDashOffset = -roadLinesOffset;
            
            ctx.beginPath();
            ctx.moveTo(canvas.width / 2, 0);
            ctx.lineTo(canvas.width / 2, canvas.height);
            ctx.stroke();
            ctx.setLineDash([]);

            drawCar(player.x, player.y, player.width, player.height, player.color);

            for (let enemy of enemies) {
                drawCar(enemy.x, enemy.y, enemy.width, enemy.height, enemy.color);
            }

            if (gameOver) {
                ctx.fillStyle = "rgba(0, 0, 0, 0.8)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                ctx.fillStyle = "white";
                ctx.font = "26px Arial";
                ctx.textAlign = "center";
                ctx.fillText("GAME OVER", canvas.width / 2, canvas.height / 2 - 20);
                
                ctx.font = "16px Arial";
                ctx.fillText("Tải lại trang để chơi lại", canvas.width / 2, canvas.height / 2 + 20);
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

components.html(game_code, height=620, scrolling=False)
