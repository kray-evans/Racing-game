import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Retro Racing Game Pro", page_icon="🏎️", layout="centered")

st.title("🏎️ Mini Retro Racing Game - Deluxe Edition")
st.markdown("Chơi mượt mà trên **PC** (dùng phím `A`/`D` hoặc mũi tên) và **Mobile** (dùng các nút ảo bên dưới). Game có tích hợp nhạc nền và đồ họa nâng cấp!")

game_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            margin: 0;
            background: #1a1a2e;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: white;
            overflow: hidden;
        }
        #game-container {
            position: relative;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7);
            border-radius: 12px;
            overflow: hidden;
            border: 3px solid #0f3460;
        }
        canvas {
            background: #16213e;
            display: block;
        }
        #ui {
            position: absolute;
            top: 10px;
            left: 15px;
            right: 15px;
            display: flex;
            justify-content: space-between;
            font-size: 18px;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
            pointer-events: none;
        }
        .controls {
            margin-top: 12px;
            display: flex;
            gap: 20px;
            justify-content: center;
        }
        button {
            padding: 14px 28px;
            font-size: 16px;
            font-weight: bold;
            background: linear-gradient(135deg, #e94560, #ff6b6b);
            color: white;
            border: none;
            border-radius: 30px;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(233, 69, 96, 0.4);
            transition: 0.1s;
            user-select: none;
            -webkit-user-select: none;
        }
        button:active {
            transform: scale(0.95);
            background: linear-gradient(135deg, #c73852, #e94560);
        }
        .audio-control {
            margin-top: 8px;
            font-size: 13px;
            color: #a0a0a0;
        }
    </style>
</head>
<body>
    <div id="game-container">
        <div id="ui">
            <div>ĐIỂM: <span id="score" style="color: #4ecc6d;">0</span></div>
            <div>TỐC ĐỘ: <span id="speed">5</span>x</div>
        </div>
        <canvas id="gameCanvas" width="400" height="500"></canvas>
    </div>
    
    <div class="controls">
        <button id="leftBtn">◀ TRÁI</button>
        <button id="rightBtn">PHẢI ▶</button>
    </div>
    <div class="audio-control">🎵 Nhạc nền tự động phát (hoặc dùng phím A/D, Mũi tên trên PC)</div>

    <!-- Nhạc nền vui nhộn dạng chiptune từ nguồn công khai ổn định -->
    <audio id="bgMusic" loop autoplay>
        <source src="https://opengameart.org/sites/default/files/Preview_3_3.mp3" type="audio/mp3">
    </audio>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const scoreElement = document.getElementById("score");
        const speedElement = document.getElementById("speed");
        const bgMusic = document.getElementById("bgMusic");

        // Cố gắng phát nhạc khi người dùng tương tác lần đầu
        window.addEventListener('click', () => {
            if (bgMusic.paused) {
                bgMusic.play().catch(e => console.log("Audio play blocked"));
            }
        }, { once: true });

        let score = 0;
        let gameOver = false;
        let gameSpeed = 5;

        let player = {
            x: 180,
            y: 380,
            width: 40,
            height: 75,
            color: "#e94560",
            speed: 7
        };

        let enemies = [];
        let roadLinesOffset = 0;
        let particles = [];
        let keys = {};

        // Bắt sự kiện bàn phím PC
        window.addEventListener("keydown", (e) => { keys[e.key] = true; });
        window.addEventListener("keyup", (e) => { keys[e.key] = false; });

        // Bắt sự kiện nút cảm ứng mobile
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
            let lanes = [45, 125, 210, 295];
            let laneX = lanes[Math.floor(Math.random() * lanes.length)];
            let colors = ["#00adb5", "#ff5722", "#9c27b0", "#ffeb3b", "#00e676"];
            let randomColor = colors[Math.floor(Math.random() * colors.length)];
            
            enemies.push({
                x: laneX,
                y: -100,
                width: 40,
                height: 75,
                color: randomColor
            });
        }

        let spawnTimer = 0;

        function update() {
            if (gameOver) return;

            // Di chuyển người chơi
            if ((keys["ArrowLeft"] || keys["a"] || movingLeft) && player.x > 35) {
                player.x -= player.speed;
                // Tạo hiệu ứng khói/bụi khi chuyển động
                particles.push({x: player.x + 15, y: player.y + 70, size: Math.random() * 4 + 2, alpha: 1});
            }
            if ((keys["ArrowRight"] || keys["d"] || movingRight) && player.x < canvas.width - 75) {
                player.x += player.speed;
                particles.push({x: player.x + 25, y: player.y + 70, size: Math.random() * 4 + 2, alpha: 1});
            }

            // Hiệu ứng chuyển động khói
            for (let i = particles.length - 1; i >= 0; i--) {
                particles[i].y += gameSpeed;
                particles[i].alpha -= 0.05;
                if (particles[i].alpha <= 0) particles.splice(i, 1);
            }

            // Hiệu ứng đường chạy
            roadLinesOffset += gameSpeed;
            if (roadLinesOffset > 40) roadLinesOffset = 0;

            // Sinh xe địch
            spawnTimer++;
            if (spawnTimer > 45) {
                spawnEnemy();
                spawnTimer = 0;
                score += 10;
                gameSpeed += 0.04; // Tăng dần độ khó
            }

            // Cập nhật vị trí xe địch & kiểm tra va chạm
            for (let i = enemies.length - 1; i >= 0; i--) {
                enemies[i].y += gameSpeed;

                // Va chạm hình chữ nhật chuẩn xác
                if (
                    player.x < enemies[i].x + enemies[i].width - 5 &&
                    player.x + player.width - 5 > enemies[i].x &&
                    player.y < enemies[i].y + enemies[i].height - 5 &&
                    player.y + player.height - 5 > enemies[i].y
                ) {
                    gameOver = true;
                    bgMusic.pause();
                }

                // Xóa xe khi ra khỏi màn hình
                if (enemies[i].y > canvas.height) {
                    enemies.splice(i, 1);
                }
            }

            scoreElement.innerText = score;
            speedElement.innerText = gameSpeed.toFixed(1);
        }

        function drawCar(x, y, width, height, color, isPlayer = false) {
            ctx.save();
            
            // Thân xe chính với bo góc nhẹ
            ctx.fillStyle = color;
            ctx.beginPath();
            ctx.roundRect(x, y, width, height, 8);
            ctx.fill();

            // Kính chắn gió trước và sau
            ctx.fillStyle = "#111";
            ctx.fillRect(x + 6, y + 16, width - 12, 16); // Kính trước
            ctx.fillRect(x + 8, y + height - 22, width - 16, 12); // Kính sau

            // Nóc xe
            ctx.fillStyle = color;
            ctx.fillRect(x + 6, y + 28, width - 12, 22);

            // Bánh xe chi tiết
            ctx.fillStyle = "#111";
            ctx.fillRect(x - 5, y + 12, 5, 16); // Bánh trước trái
            ctx.fillRect(x + width, y + 12, 5, 16); // Bánh trước phải
            ctx.fillRect(x - 5, y + height - 22, 5, 16); // Bánh sau trái
            ctx.fillRect(x + width, y + height - 22, 5, 16); // Bánh sau phải

            // Đèn pha phía trước (Xe người chơi màu vàng sáng, xe địch màu đỏ/trắng)
            ctx.fillStyle = isPlayer ? "#ffe100" : "#ff4757";
            ctx.fillRect(x + 4, y, 6, 4);
            ctx.fillRect(x + width - 10, y, 6, 4);

            // Đèn hậu phía sau
            ctx.fillStyle = "#ff4757";
            ctx.fillRect(x + 5, y + height - 2, 6, 2);
            ctx.fillRect(x + width - 11, y + height - 2, 6, 2);

            ctx.restore();
        }

        function draw() {
            // Nền đường chính màu xám đậm hiện đại
            ctx.fillStyle = "#2b2b2b";
            ctx.fillRect(35, 0, canvas.width - 70, canvas.height);

            // Viền lề đường sọc đỏ trắng phong cách đường đua F1
            let stripeHeight = 30;
            let stripeOffset = (roadLinesOffset * 2) % (stripeHeight * 2);
            for (let y = -stripeHeight; y < canvas.height + stripeHeight; y += stripeHeight) {
                let isRed = Math.floor((y + stripeOffset) / stripeHeight) % 2 === 0;
                ctx.fillStyle = isRed ? "#e94560" : "#ffffff";
                ctx.fillRect(15, y - stripeOffset, 20, stripeHeight);
                ctx.fillRect(canvas.width - 35, y - stripeOffset, 20, stripeHeight);
            }

            // Dải phân cách làn đường đứt đoạn ở giữa
            ctx.strokeStyle = "#ffffff";
            ctx.lineWidth = 4;
            ctx.setLineDash([25, 25]);
            ctx.lineDashOffset = -roadLinesOffset;
            
            ctx.beginPath();
            ctx.moveTo(canvas.width / 2, 0);
            ctx.lineTo(canvas.width / 2, canvas.height);
            ctx.stroke();
            ctx.setLineDash([]); // Reset dash

            // Vẽ hiệu ứng khói bụi
            for (let p of particles) {
                ctx.fillStyle = `rgba(200, 200, 200, ${p.alpha})`;
                ctx.fillRect(p.x, p.y, p.size, p.size);
            }

            // Vẽ xe người chơi và xe địch
            drawCar(player.x, player.y, player.width, player.height, player.color, true);

            for (let enemy of enemies) {
                drawCar(enemy.x, enemy.y, enemy.width, enemy.height, enemy.color, false);
            }

            // Màn hình Game Over
            if (gameOver) {
                ctx.fillStyle = "rgba(15, 19, 42, 0.85)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                ctx.fillStyle = "#e94560";
                ctx.font = "bold 32px 'Segoe UI', sans-serif";
                ctx.textAlign = "center";
                ctx.fillText("THUA RỒI!", canvas.width / 2, canvas.height / 2 - 30);
                
                ctx.fillStyle = "#ffffff";
                ctx.font = "18px 'Segoe UI', sans-serif";
                ctx.fillText("Điểm đạt được: " + score, canvas.width / 2, canvas.height / 2 + 10);
                
                ctx.fillStyle = "#a0a0a0";
                ctx.font = "14px 'Segoe UI', sans-serif";
                ctx.fillText("Tải lại trang (F5) để chơi lại ván mới", canvas.width / 2, canvas.height / 2 + 50);
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
