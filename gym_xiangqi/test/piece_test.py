import unittest

from gym_xiangqi.piece import Piece, General, Advisor, Elephant
from gym_xiangqi.piece import Horse, Chariot, Cannon, Soldier
from gym_xiangqi.constants import RED, BLACK


class TestPieceClasses(unittest.TestCase):

    def setUp(self) -> None:
        self.classes = [Piece, General, Advisor, Elephant,
                        Horse, Chariot, Cannon, Soldier]

    def test_piece_initialization(self):
        for piece_class in self.classes:
            piece = piece_class(0, 0, 0)
            self.assertIsInstance(piece, piece_class)
            self.assertEqual(piece.color, RED)
            self.assertEqual(piece.row, 0)
            self.assertEqual(piece.col, 0)
            piece.color = 1
            self.assertEqual(piece.color, BLACK)


if __name__ == "__main__":
    unittest.main()