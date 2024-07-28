from collections import deque
import heapq
import itertools

class Solver():
    def __init__(self, board):
        self.board = board
        self.solutions = []
        self.bfs_cache = {}
        self.color_to_index = {color: index for index, color in enumerate(self.board.robots.keys())}

    def bfs(self, start, end):
        
        if start ==end:
            return 0
        
        if (start, end) in self.bfs_cache:
            return self.bfs_cache[(start, end)]

        # Initialize distances
        distances = [[float('inf')] * self.board.n_cols for _ in range(self.board.n_rows)]
        distances[start[0]][start[1]] = 0

        # BFS queue
        queue = deque([start])

        # Direction vectors for moving in 4-connected grid
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            x, y = queue.popleft()
            current_distance = distances[x][y]

            for dx, dy in directions:
                nx, ny = x + dx, y + dy

                if 0 <= nx < self.board.n_rows and 0 <= ny < self.board.n_cols  and (nx, ny) not in self.board.walls  and distances[nx][ny] == float('inf'):
                    distances[nx][ny] = current_distance + 1
                    if (nx, ny) == end:
                        self.bfs_cache[(start, end)] = distances[nx][ny]
                        return distances[nx][ny]
                    queue.append((nx, ny))

        # If no path is found
        self.bfs_cache[(start, end)] = float('inf')
        return float('inf')

    def _heuristic(self, robots, targets):
        
        tot = 0
        for t_col, t_pos in targets.items():
                r_pos = robots[t_col]
                tot += self.bfs(r_pos, t_pos)
        return tot
    
    def _state_to_tuple(self, robots):

        return tuple(robots.get(color, (-1, -1)) for color in self.color_to_index)

    def _get_next_states(self, robots):
                
        next_states = []
        for color, (x, y) in robots.items():
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_x, new_y = x, y
                while 0 <= new_x + dx < self.board.n_cols and 0 <= new_y + dy < self.board.n_rows:
                    if (new_x + dx, new_y + dy) in self.board.walls:
                        break
                    if (new_x + dx, new_y + dy) in robots.values():
                        break

                    new_x, new_y = new_x + dx, new_y + dy
                    if color in self.board.targets and (new_x, new_y) == self.board.targets[color]:
                        break

                if (new_x, new_y) != (x, y):
                    new_robots = robots.copy()
                    new_robots[color] = (new_x, new_y)
                    next_states.append((color, (dx, dy), new_robots))
        return next_states

    def solve(self, max_depth=20):
      
        # Use a counter to break ties and avoid comparing dictionaries
        counter = itertools.count()

        # 0. Initialize the priority queue with the start state
        start_robots = self.board.robots.copy()
        start_h = self._heuristic(start_robots, self.board.targets)
        pq = [(start_h, 0, next(counter), start_robots, [])]  # (priority, depth, counter, robots, path)
        visited = set()

        while pq:
            priority, depth, _, robots, path = heapq.heappop(pq)

            # 1. Check if the current state is the goal state and return the solution.
            print(self._heuristic(robots, self.board.targets))
            if self._heuristic(robots, self.board.targets) == 0:
                self.solutions = path
                return path

            if depth >= max_depth:
                continue

            # Keep track of visited states
            state_tuple = self._state_to_tuple(robots)
            if state_tuple in visited:
                continue
            visited.add(state_tuple)

            # 2. Generate all possible next states by moving each robot in each direction.
            for color, direction, new_robots in self._get_next_states(robots):
                # 3. Calculate priority (f = g + h) where g is the depth and h is the heuristic.
                new_depth = depth + 1
                h = self._heuristic(new_robots, self.board.targets)
                new_priority = new_depth + h

                # 4. Add new states to the priority queue if they haven't been visited.
                new_path = path + [(color, direction)]
                heapq.heappush(pq, (new_priority, new_depth, next(counter), new_robots, new_path))

        return None  # No solution found
