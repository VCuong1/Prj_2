import pygame
import random
from queue import Queue

# Khởi tạo Pygame
pygame.init()

# Kích thước màn hình
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600  # Chiều rộng và chiều cao của màn hình (đơn vị pixel)
CELL_SIZE = 40  # Kích thước của mỗi ô lưới (được dùng để xác định kích thước của mê cung và nhân vật)

# Màu sắc cho việc vẽ
WHITE = (255, 255, 255)  # Màu trắng (dùng để vẽ đường đi trong mê cung)
BLACK = (0, 0, 0)        # Màu đen (dùng để vẽ các bức tường trong mê cung)
GREEN = (0, 255, 0)      # Màu xanh lá (dùng để vẽ thông báo chiến thắng)
RED = (255, 0, 0)        # Màu đỏ (dùng để vẽ thông báo "Game Over")
BLUE = (0, 0, 255)       # Màu xanh dương (dùng để vẽ con quái vật)
PINK = (255, 105, 180)   # Màu hồng (dùng để vẽ nhân vật người chơi)

# Tạo màn hình chơi game
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chase the Pink Dot")  # Đặt tên cửa sổ game

# Đặt đồng hồ để điều chỉnh tốc độ khung hình (FPS)
clock = pygame.time.Clock()

def generate_maze(rows, cols):
    """
    Hàm sinh mê cung sử dụng thuật toán tìm kiếm theo chiều sâu (DFS) với việc backtrack
    và tạo thêm các đường đi ngẫu nhiên.
    """
    maze = [[1 for _ in range(cols)] for _ in range(rows)]  # 1 là tường, 0 là đường đi

    # Các hướng di chuyển: (điều chỉnh theo hàng, điều chỉnh theo cột)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def in_bounds(r, c):
        """Kiểm tra xem tọa độ (r, c) có nằm trong phạm vi của mê cung không"""
        return 0 <= r < rows and 0 <= c < cols

    def carve_path(r, c):
        """Cắt đường đi trong mê cung"""
        maze[r][c] = 0  # Đánh dấu ô (r, c) là đường đi
        random.shuffle(directions)  # Xáo trộn các hướng để tạo sự ngẫu nhiên

        for dr, dc in directions:
            nr, nc = r + dr * 2, c + dc * 2  # Kiểm tra 2 bước xa
            if in_bounds(nr, nc) and maze[nr][nc] == 1:  # Nếu ô tiếp theo là tường
                maze[r + dr][c + dc] = 0  # Tạo đường đi giữa các ô
                carve_path(nr, nc)

    # Bắt đầu từ góc trên bên trái và tạo ra các đường đi
    carve_path(0, 0)

    # Thêm các đường mở ngẫu nhiên vào mê cung để có nhiều lối đi hơn
    for _ in range(int(rows * cols * 0.3)):  # Tạo ra 30% ô mở ngẫu nhiên
        r, c = random.randint(0, rows - 1), random.randint(0, cols - 1)
        if maze[r][c] == 1 and (r, c) != (0, 0) and (r, c) != (rows - 1, cols - 1):
            maze[r][c] = 0

    # Đảm bảo ô bắt đầu và ô kết thúc luôn là đường đi
    maze[0][0] = 0
    maze[rows - 1][cols - 1] = 0

    return maze

def bfs_path(maze, start, end):
    """
    Hàm tìm đường đi ngắn nhất trong mê cung bằng cách sử dụng tìm kiếm theo chiều rộng (BFS).
    """
    rows, cols = len(maze), len(maze[0])  # Lấy số hàng và số cột của mê cung
    queue = Queue()  # Tạo hàng đợi (queue) để xử lý BFS
    queue.put((start, [start]))  # Thêm điểm bắt đầu vào hàng đợi
    visited = set()  # Tập hợp các ô đã được thăm

    while not queue.empty():
        (r, c), path = queue.get()  # Lấy ô hiện tại và đường đi đến ô đó
        if (r, c) == end:  # Nếu ô hiện tại là ô kết thúc, trả về đường đi
            return path
        if (r, c) in visited:  # Nếu ô này đã được thăm, bỏ qua
            continue
        visited.add((r, c))  # Đánh dấu ô này đã thăm

        # Thêm các ô láng giềng vào hàng đợi
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0 and (nr, nc) not in visited:
                queue.put(((nr, nc), path + [(nr, nc)]))

    return []  # Nếu không có đường đi, trả về danh sách rỗng

def draw_maze(maze):
    """
    Hàm vẽ mê cung lên màn hình.
    """
    for row in range(len(maze)):  # Duyệt qua từng hàng trong mê cung
        for col in range(len(maze[0])):  # Duyệt qua từng cột trong mê cung
            color = WHITE if maze[row][col] == 0 else BLACK  # Nếu ô là đường đi, vẽ màu trắng, nếu là tường, vẽ màu đen
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def show_game_over(message):
    """
    Hàm hiển thị thông báo trò chơi kết thúc (Game Over hoặc You Win).
    """
    font = pygame.font.Font(None, 74)  # Tạo đối tượng font với kích thước 74
    text = font.render(message, True, RED if message == "Game Over" else GREEN)  # Tạo văn bản để hiển thị
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))  # Căn giữa văn bản
    screen.blit(text, text_rect)  # Vẽ văn bản lên màn hình

def main():
    while True:  # Vòng lặp vô hạn để khởi động lại game mỗi khi kết thúc
        rows = SCREEN_HEIGHT // CELL_SIZE  # Số hàng của mê cung
        cols = SCREEN_WIDTH // CELL_SIZE   # Số cột của mê cung

        # Tạo mê cung
        maze = generate_maze(rows, cols)

        # Vị trí bắt đầu của người chơi (hình tròn hồng) và con quái vật (hình tròn xanh dương)
        player_pos = [0, 0]  # Vị trí người chơi
        monster_pos = [rows - 1, cols - 1]  # Vị trí con quái vật

        # Di chuyển của người chơi (lên, xuống, trái, phải)
        player_move = [0, 0]

        # Tạo đường đi từ người chơi đến con quái vật (nếu có)
        start = tuple(player_pos)
        end = tuple(monster_pos)
        path = bfs_path(maze, start, end)

        # Vật thể theo đường đi (con quái vật sẽ đi theo người chơi)
        running = True
        while running:
            screen.fill(BLACK)  # Lấp đầy màn hình với màu đen

            # Xử lý các sự kiện (như di chuyển của người chơi)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return  # Thoát khỏi game khi đóng cửa sổ
                if event.type == pygame.KEYDOWN:
                    # Điều khiển người chơi di chuyển trong mê cung (chỉ khi không đụng tường)
                    if event.key == pygame.K_LEFT and player_pos[1] > 0 and maze[player_pos[0]][player_pos[1] - 1] == 0:
                        player_pos[1] -= 1
                    if event.key == pygame.K_RIGHT and player_pos[1] < cols - 1 and maze[player_pos[0]][player_pos[1] + 1] == 0:
                        player_pos[1] += 1
                    if event.key == pygame.K_UP and player_pos[0] > 0 and maze[player_pos[0] - 1][player_pos[1]] == 0:
                        player_pos[0] -= 1
                    if event.key == pygame.K_DOWN and player_pos[0] < rows - 1 and maze[player_pos[0] + 1][player_pos[1]] == 0:
                        player_pos[0] += 1

            # Tạo đường đi từ con quái vật đến người chơi
            path = bfs_path(maze, tuple(monster_pos), tuple(player_pos))
            if path:
                monster_pos = list(path[1])  # Con quái vật di chuyển về phía người chơi

            # Vẽ mê cung
            draw_maze(maze)

            # Vẽ người chơi (hình tròn màu hồng)
            pygame.draw.circle(
                screen,
                PINK,
                (player_pos[1] * CELL_SIZE + CELL_SIZE // 2, player_pos[0] * CELL_SIZE + CELL_SIZE // 2),
                CELL_SIZE // 4,
            )

            # Vẽ con quái vật (hình tròn màu xanh dương)
            pygame.draw.circle(
                screen,
                BLUE,
                (monster_pos[1] * CELL_SIZE + CELL_SIZE // 2, monster_pos[0] * CELL_SIZE + CELL_SIZE // 2),
                CELL_SIZE // 4,
            )

            # Kiểm tra nếu con quái vật bắt được người chơi
            if player_pos == monster_pos:
                show_game_over("Game Over")
                pygame.display.flip()
                pygame.time.wait(3000)  # Đợi 3 giây trước khi khởi động lại game
                break  # Thoát vòng lặp để khởi động lại game

            # Kiểm tra nếu người chơi đã đến được mục tiêu (góc dưới bên phải)
            if player_pos == [rows - 1, cols - 1]:
                show_game_over("You Win!")
                pygame.display.flip()
                pygame.time.wait(3000)  # Đợi 3 giây trước khi khởi động lại game
                break  # Thoát vòng lặp để khởi động lại game

            pygame.display.flip()  # Cập nhật màn hình
            clock.tick(5)  # Điều chỉnh tốc độ của trò chơi (khung hình mỗi giây)

if __name__ == "__main__":
    main()
