import unittest
from unittest.mock import Mock, patch
import pygame
from src.game import Game
from src.board import Board
from src.solver import Solver
from src.robot import RobotColor

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.board = Mock(spec=Board)
        self.game.board.move_robot = Mock()

    @patch('src.game.Solver')
    @patch('src.game.time.sleep')
    @patch('src.game.pygame.event.pump')
    def test_solve_puzzle_with_solution(self, mock_pump, mock_sleep, mock_solver):
        mock_solver_instance = mock_solver.return_value
        mock_solver_instance.solve.return_value = [
            (RobotColor.RED, (0, 1)),
            (RobotColor.BLUE, (1, 0))
        ]

        with patch('builtins.print') as mock_print:
            self.game.solve_puzzle()

        mock_solver.assert_called_once_with(self.game.board)
        mock_solver_instance.solve.assert_called_once()
        
        self.assertEqual(self.game.board.move_robot.call_count, 2)
        self.game.board.move_robot.assert_any_call(RobotColor.RED, (0, 1))
        self.game.board.move_robot.assert_any_call(RobotColor.BLUE, (1, 0))
        
        self.assertEqual(mock_print.call_count, 5)
        mock_print.assert_any_call("\nSolution found!")
        mock_print.assert_any_call("==============")
        mock_print.assert_any_call("Step 1: Move RED robot DOWN")
        mock_print.assert_any_call("Step 2: Move BLUE robot RIGHT")
        mock_print.assert_any_call("\nPuzzle solved in 2 moves!")

        self.assertEqual(mock_sleep.call_count, 2)
        self.assertEqual(mock_pump.call_count, 2)

    @patch('src.game.Solver')
    def test_solve_puzzle_no_solution(self, mock_solver):
        mock_solver_instance = mock_solver.return_value
        mock_solver_instance.solve.return_value = None

        with patch('builtins.print') as mock_print:
            self.game.solve_puzzle()

        mock_solver.assert_called_once_with(self.game.board)
        mock_solver_instance.solve.assert_called_once()
        mock_print.assert_called_once_with("\nNo solution found")

    @patch('src.game.Solver')
    @patch('src.game.time.sleep')
    @patch('src.game.pygame.event.pump')
    def test_solve_puzzle_with_unknown_direction(self, mock_pump, mock_sleep, mock_solver):
        mock_solver_instance = mock_solver.return_value
        mock_solver_instance.solve.return_value = [
            (RobotColor.GREEN, (0, 0))
        ]

        with patch('builtins.print') as mock_print:
            self.game.solve_puzzle()

        mock_solver.assert_called_once_with(self.game.board)
        mock_solver_instance.solve.assert_called_once()
        
        self.assertEqual(self.game.board.move_robot.call_count, 1)
        self.game.board.move_robot.assert_called_once_with(RobotColor.GREEN, (0, 0))
        
        mock_print.assert_any_call("Step 1: Move GREEN robot UNKNOWN")

    def test_solve_puzzle_draw_called(self):
        self.game.draw = Mock()
        mock_solver = Mock()
        mock_solver.solve.return_value = [(RobotColor.RED, (0, 1))]
        
        with patch('src.game.Solver', return_value=mock_solver):
            with patch('src.game.time.sleep'):
                with patch('src.game.pygame.event.pump'):
                    self.game.solve_puzzle()
        
        self.game.draw.assert_called_once()

if __name__ == '__main__':
    unittest.main()
