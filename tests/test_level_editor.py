import unittest
from unittest.mock import Mock, patch
import pygame
from src.level_editor import LevelEditor
from src.board import Board
from src.wall import Wall
from src.robot import Robot
from src.target import Target
from src.color import Color

class TestLevelEditor(unittest.TestCase):
    def setUp(self):
        self.screen = Mock(spec=pygame.Surface)
        self.level_editor = LevelEditor(self.screen)

    def test_init(self):
        self.assertIsInstance(self.level_editor.board, Board)
        self.assertEqual(self.level_editor.board.n_rows, 12)
        self.assertEqual(self.level_editor.board.n_cols, 12)
        self.assertIsNone(self.level_editor.current_tool)
        self.assertEqual(len(self.level_editor.tools), 8)
        self.assertEqual(self.level_editor.toolbar_height, 50)

    def test_tools_initialization(self):
        self.assertIsInstance(self.level_editor.tools['wall'], Wall)
        self.assertIsInstance(self.level_editor.tools['robot_red'], Robot)
        self.assertIsInstance(self.level_editor.tools['target_green'], Target)
        self.assertIsNone(self.level_editor.tools['eraser'])

    def test_robot_colors(self):
        self.assertEqual(self.level_editor.tools['robot_red'].color, Color.RED)
        self.assertEqual(self.level_editor.tools['robot_green'].color, Color.GREEN)
        self.assertEqual(self.level_editor.tools['robot_blue'].color, Color.BLUE)

    def test_target_colors(self):
        self.assertEqual(self.level_editor.tools['target_red'].color, Color.RED)
        self.assertEqual(self.level_editor.tools['target_green'].color, Color.GREEN)
        self.assertEqual(self.level_editor.tools['target_blue'].color, Color.BLUE)

    @patch('src.level_editor.Board')
    def test_custom_board_size(self, mock_board):
        custom_editor = LevelEditor(self.screen, n_rows=15, n_cols=20)
        mock_board.assert_called_once_with(n_rows=15, n_cols=20)

    def test_screen_assignment(self):
        self.assertEqual(self.level_editor.screen, self.screen)

