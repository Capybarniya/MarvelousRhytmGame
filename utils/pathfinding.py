from utils.tools import heuristic

def a_star_search(start, goal, ver_func, max_depth=1e20):
    closed_set = []
    open_set = [start]
    
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    came_from = {}
    
    while open_set and len(closed_set) < max_depth:
        current = open_set[0]
        for node in open_set:
            if f_score.get(node, float('inf')) < f_score.get(current, float('inf')):
                current = node
        
        if current == goal:
            return reconstruct_path(came_from, current)
        
        open_set.remove(current)
        closed_set.append(current)
        
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor = (current[0] + dx, current[1] + dy)
            
            if neighbor in closed_set:
                continue
            
            if not ver_func(neighbor, check_for_enemies=False):
                continue
            
            tentative_g_score = g_score[current] + 1
            
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                
                if neighbor not in open_set:
                    open_set.append(neighbor)
    
    return None

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

def get_next_step(start, goal, ver_func, max_depth=1e20):
    path = a_star_search(start, goal, ver_func, max_depth)
    if path and len(path) > 1:
    
        return path[1]
    print(path)
    return None

def get_furthest_tile(start_pos, ver_func):
    queue = [] 
    queue.append((start_pos, 0))
    
    head_index = 0
    
    visited = {start_pos: True}
    
    farthest_pos = start_pos
    max_distance = 0
    
    while head_index < len(queue):
        current_pos, distance = queue[head_index]
        head_index += 1
        
        if distance > max_distance:
            max_distance = distance
            farthest_pos = current_pos
        
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor = (current_pos[0] + dx, current_pos[1] + dy)
            
            if ver_func(neighbor, check_for_enemies=False) and neighbor not in visited:
                visited[neighbor] = True
                queue.append((neighbor, distance + 1))
    
    return farthest_pos