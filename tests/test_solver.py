import unittest
from src.solver import Solver
from src.board import Board

class TestSolver(unittest.TestCase):
    def setUp(self):
        self.board = Board(5, 5)
        self.solver = Solver(self.board)

    def test_bfs_start_equals_end(self):
        start = (0, 0)
        end = (0, 0)
        self.assertEqual(self.solver.bfs(start, end), 0)

    def test_bfs_adjacent_cells(self):
        start = (0, 0)
        end = (0, 1)
        self.assertEqual(self.solver.bfs(start, end), 1)

    def test_bfs_with_wall(self):
        self.board.walls.add((0, 1))
        start = (0, 0)
        end = (0, 2)
        self.assertEqual(self.solver.bfs(start, end), 3)

    def test_bfs_no_path(self):
        self.board.walls.add((1, 0))
        self.board.walls.add((0, 1))
        start = (0, 0)
        end = (1, 1)
        self.assertEqual(self.solver.bfs(start, end), float('inf'))

    def test_bfs_cache(self):
        start = (0, 0)
        end = (4, 4)
        first_result = self.solver.bfs(start, end)
        cached_result = self.solver.bfs(start, end)
        self.assertEqual(first_result, cached_result)
        self.assertIn((start, end), self.solver.bfs_cache)

    def test_bfs_out_of_bounds(self):
        start = (0, 0)
        end = (5, 5)
        self.assertEqual(self.solver.bfs(start, end), float('inf'))

if __name__ == '__main__':
    unittest.main()
