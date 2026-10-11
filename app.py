import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Retro Racing Game", page_icon="🏎️", layout="centered")

st.title("🏎️ Mini Retro Racing Game")
st.markdown("Sử dụng các phím mũi tên **Trái / Phải** hoặc các nút điều khiển bên dưới để né xe địch và ghi điểm!")

# Mã HTML/JS cho game đua xe
game_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            margin: 0;
            background: #111;
            display: flex;
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
        }
        #ui {
            position: absolute;
            top: 20px;
            font-size: 20px;
            font-weight: bold;
        }
        .controls {
            margin-top: 10px;
            display: flex;
            gap: 10px;
            justify-content: center;
        }
        button {
            padding: 10px 20px;
            font-size: 16px;
            background: #ff4757;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button:active {
            background: #ff6b81;
        }
    </style>
</head>
<body>
    <div id="ui">Điểm: <span id="score">0</span></div>
    <canvas id="gameCanvas" width="400" height="600"></canvas>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const scoreElement = document.getElementById("score");

        let score = 0;
        let gameOver = false;
        let gameSpeed = 5;

        // Xe người chơi
        let player = {
            x: 180,
            y: 480,
            width: 40,
            height: 70,
            color: "#ff4757",
            speed: 6
        };

        // Danh sách xe chướng ngại vật
        let enemies = [];
        let roadLinesOffset = 0;

        let keys = {};

        window.addEventListener("keydown", (e) => { keys[e.key] = true; });
        window.addEventListener("keyup", (e) => { keys[e.key] = false; });

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

            // Di chuyển người chơi
            if ((keys["ArrowLeft"] || keys["a"]) && player.x > 30) {
                player.x -= player.speed;
            }
            if ((keys["ArrowRight"] || keys["d"]) && player.x < canvas.width - 70) {
                player.x += player.speed;
            }

            // Hiệu ứng đường chạy
            roadLinesOffset += gameSpeed;
            if (roadLinesOffset > 40) roadLinesOffset = 0;

            // Sinh xe địch
            spawnTimer++;
            if (spawnTimer > 50) {
                spawnEnemy();
                spawnTimer = 0;
                score += 10;
                gameSpeed += 0.05; // Tăng dần độ khó
            }

            // Cập nhật vị trí xe địch
            for (let i = enemies.length - 1; i >= 0; i--) {
                enemies[i].y += gameSpeed;

                // Kiểm tra va chạm
                if (
                    player.x < enemies[i].x + enemies[i].width &&
                    player.x + player.width > enemies[i].x &&
                    player.y < enemies[i].y + enemies[i].height &&
                    player.y + player.height > enemies[i].y
                ) {
                    gameOver = true;
                }

                // Xóa xe qua màn hình
                if (enemies[i].y > canvas.height) {
                    enemies.splice(i, 1);
                }
            }

            scoreElement.innerText = score;
        }

        function drawCar(x, y, width, height, color) {
            ctx.fillStyle = color;
            ctx.fillRect(x, y, width, height);
            // Bánh xe
            ctx.fillStyle = "#000";
            ctx.fillRect(x - 6, y + 10, 6, 15);
            ctx.fillRect(x + width, y + 10, 6, 15);
            ctx.fillRect(x - 6, y + height - 25, 6, 15);
            ctx.fillRect(x + width, y + height - 25, 6, 15);
            // Đèn trước
            ctx.fillStyle = "#fffa65";
            ctx.fillRect(x + 5, y, 8, 4);
            ctx.fillRect(x + width - 13, y, 8, 4);
        }

        function draw() {
            // Vẽ nền đường
            ctx.fillStyle = "#555";
            ctx.fillRect(20, 0, canvas.width - 40, canvas.height);

            // Lề đường
            ctx.fillStyle = "#ff4757";
            ctx.fillRect(0, 0, 20, canvas.height);
            ctx.fillRect(canvas.width - 20, 0, 20, canvas.height);

            // Vạch kẻ đường giữa
            ctx.strokeStyle = "#fff";
            ctx.lineWidth = 4;
            ctx.setLineDash([20, 20]);
            ctx.lineDashOffset = -roadLinesOffset;
            
            ctx.beginPath();
            ctx.moveTo(canvas.width / 2, 0);
            ctx.lineTo(canvas.width / 2, canvas.height);
            ctx.stroke();
            ctx.setLineDash([]); // Reset dash

            // Vẽ xe người chơi
            drawCar(player.x, player.y, player.width, player.height, player.color);

            // Vẽ xe địch
            for (let enemy of enemies) {
                drawCar(enemy.x, enemy.y, enemy.width, enemy.height, enemy.color);
            }

            if (gameOver) {
                ctx.fillStyle = "rgba(0, 0, 0, 0.8)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                ctx.fillStyle = "white";
                ctx.font = "30px Arial";
                ctx.textAlign = "center";
                ctx.fillText("GAME OVER", canvas.width / 2, canvas.height / 2 - 20);
                
                ctx.font = "18px Arial";
                ctx.fillText("Nhấn F5 hoặc tải lại trang để chơi lại", canvas.width / 2, canvas.height / 2 + 20);
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

# Hiển thị game trong ứng dụng Streamlit
components.html(game_code, height=650, scrolling=False)
