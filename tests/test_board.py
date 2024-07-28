import unittest
from unittest.mock import Mock
from src.board import Board
from src.robot import RobotColor

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.board.robots = {
            RobotColor.RED: (0, 0),
            RobotColor.BLUE: (5, 5),
            RobotColor.GREEN: (10, 10),
            RobotColor.YELLOW: (15, 15)
        }

    def test_get_robot_position(self):
        self.assertEqual(self.board.robots[RobotColor.RED], (0, 0))
        self.assertEqual(self.board.robots[RobotColor.BLUE], (5, 5))
        self.assertEqual(self.board.robots[RobotColor.GREEN], (10, 10))
        self.assertEqual(self.board.robots[RobotColor.YELLOW], (15, 15))

    def test_get_nonexistent_robot_position(self):
        with self.assertRaises(KeyError):
            _ = self.board.robots[RobotColor.PURPLE]

    def test_update_robot_position(self):
        self.board.robots[RobotColor.RED] = (1, 1)
        self.assertEqual(self.board.robots[RobotColor.RED], (1, 1))

    def test_multiple_robots_different_positions(self):
        positions = set(self.board.robots.values())
        self.assertEqual(len(positions), 4)

if __name__ == '__main__':
    unittest.main()
