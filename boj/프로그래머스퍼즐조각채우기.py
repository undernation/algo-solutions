"""
BOJ   프로그래머스 퍼즐조각 채우기

풀이일 : 2026-10-21   결과: 품
"""

from collections import deque
N = 0

def normalize(pos_list):
    
    new_list = []
    
    min_y = 52
    min_x = 52
    for a, b in pos_list:
        min_y = min(min_y, a)
        min_x = min(min_x, b)
        
    for a, b in pos_list:
        new_y = a - min_y
        new_x = b - min_x
        new_list.append((new_y, new_x))
        
    new_list.sort()
    return new_list


def rotate(pos_list):
    new_list = []
    
    for a, b in pos_list:
        new_y = 1 - b
        new_x = a
        new_list.append((new_y, new_x))
        
    return normalize(new_list)

visited = set()

def bfs(sy, sx, board, check_num):
    global visited
    cur_list = []
    q = deque()
    q.append((sy, sx))
    visited.add((sy, sx))
    cur_list.append((sy, sx))
    
    while q:
        cy, cx = q.popleft()
        
        for dy, dx in [[1, 0], [0, 1], [-1, 0], [0, -1]]:
            ny = cy + dy
            nx = cx + dx
            
            if not (0 <= ny < N and 0 <= nx < N):
                continue
            if board[ny][nx] != check_num:
                continue
            if (ny, nx) in visited:
                continue
                
            q.append((ny, nx))
            visited.add((ny, nx))
            cur_list.append((ny, nx))
            
    return cur_list
    
    
def solution(game_board, table):
    global N, visited
    answer = 0
    
    blocks = dict()
    block_id = 0
    N = len(game_board)
    
    # 조각 table 에서 추출하기
    
    for i in range(N):
        for j in range(N):
            if table[i][j] == 1 and (i, j) not in visited:
                cur_blocks = bfs(i, j, table, 1)
                
                blocks[block_id] = []
                normalized = normalize(cur_blocks)
                blocks[block_id].append(normalized)
                rotated = rotate(normalized)
                blocks[block_id].append(rotated)
                rotated = rotate(rotated)
                blocks[block_id].append(rotated)
                rotated = rotate(rotated)
                blocks[block_id].append(rotated)
                
                block_id += 1
    is_used = [False] * block_id
    
    
    # for key, value in blocks.items():
    #     print(key)
    #     print(value)
    
    
    # game_boar 에서 빈칸 추출하기
    # 빈칸 normalize 하기
    visited = set()
    
    # 조각 순회하면서 같은거 찾기
    blanks = []
    for i in range(N):
        for j in range(N):
            if game_board[i][j] == 0 and (i, j) not in visited:
                cur_blanks = bfs(i, j, game_board, 0)
                cur_blanks = normalize(cur_blanks)
                blanks.append(cur_blanks)
                
    # print(blanks)
    
    # 사용 시 해당 딕셔너리 False 처리 해주기
    # 사용시 해당 퍼즐 조각 갯수만큼 더해주기
    for blank in blanks:
        # print("blank", blank)
        for key, values in blocks.items():
            if is_used[key]:
                continue
            is_found = False
            for value in values:
                
                if blank == value:
                    answer += len(blank)
                    is_used[key] = True
                    is_found = True
                    break
            if is_found:
                break
        
    
    return answer
