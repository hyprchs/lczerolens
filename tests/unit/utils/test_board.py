"""
Tests for the board utils.
"""

from lczero.backends import GameState

from lczerolens import board_utils
from lczerolens.utils import lczero as lczero_utils


class TestWithBackend:
    def test_board_to_tensor13x8x8(
        self, random_move_board_list, tiny_lczero_backend
    ):
        """
        Test that the board to tensor function works.
        """
        move_list, board_list = random_move_board_list
        for i, board in enumerate(board_list):
            board_tensor = board_utils.board_to_tensor13x8x8(board)
            uci_moves = [move.uci() for move in move_list[:i]]
            lczero_game = GameState(moves=uci_moves)
            lczero_input_tensor = lczero_utils.board_from_backend(
                tiny_lczero_backend, lczero_game, planes=13
            )
            assert (board_tensor == lczero_input_tensor[:13]).all()

    def test_board_to_tensor112x8x8(
        self, random_move_board_list, tiny_lczero_backend
    ):
        """
        Test that the board to tensor function works.
        """
        move_list, board_list = random_move_board_list
        for i, board in enumerate(board_list):
            board_tensor = board_utils.board_to_tensor112x8x8(board)
            uci_moves = [move.uci() for move in move_list[:i]]
            lczero_game = GameState(moves=uci_moves)
            lczero_input_tensor = lczero_utils.board_from_backend(
                tiny_lczero_backend, lczero_game
            )
            # assert (board_tensor == lczero_input_tensor).all()
            for plane in range(112):
                assert (
                    board_tensor[plane] == lczero_input_tensor[plane]
                ).all()


class TestRepetition:
    def test_board_to_tensor13x8x8(
        self, repetition_move_board_list, tiny_lczero_backend
    ):
        """
        Test that the board to tensor function works.
        """
        move_list, board_list = repetition_move_board_list
        for i, board in enumerate(board_list):
            uci_moves = [move.uci() for move in move_list[:i]]
            board_tensor = board_utils.board_to_tensor13x8x8(board)
            lczero_game = GameState(moves=uci_moves)
            lczero_input_tensor = lczero_utils.board_from_backend(
                tiny_lczero_backend, lczero_game, planes=13
            )
            assert (board_tensor == lczero_input_tensor[:13]).all()

    def test_board_to_tensor112x8x8(
        self, repetition_move_board_list, tiny_lczero_backend
    ):
        """
        Test that the board to tensor function works.
        """
        move_list, board_list = repetition_move_board_list
        for i, board in enumerate(board_list):
            uci_moves = [move.uci() for move in move_list[:i]]
            board_tensor = board_utils.board_to_tensor112x8x8(board)
            lczero_game = GameState(moves=uci_moves)
            lczero_input_tensor = lczero_utils.board_from_backend(
                tiny_lczero_backend, lczero_game
            )
            assert (board_tensor == lczero_input_tensor).all()


class TestLong:
    def test_board_to_tensor13x8x8(
        self, long_move_board_list, tiny_lczero_backend
    ):
        """
        Test that the board to tensor function works.
        """
        move_list, board_list = long_move_board_list
        for i, board in enumerate(board_list):
            uci_moves = [move.uci() for move in move_list[:i]]
            board_tensor = board_utils.board_to_tensor13x8x8(board)
            lczero_game = GameState(moves=uci_moves)
            lczero_input_tensor = lczero_utils.board_from_backend(
                tiny_lczero_backend, lczero_game, planes=13
            )
            assert (board_tensor == lczero_input_tensor[:13]).all()

    def test_board_to_tensor112x8x8(
        self, long_move_board_list, tiny_lczero_backend
    ):
        """
        Test that the board to tensor function works.
        """
        move_list, board_list = long_move_board_list
        for i, board in enumerate(board_list):
            uci_moves = [move.uci() for move in move_list[:i]]
            board_tensor = board_utils.board_to_tensor112x8x8(board)
            lczero_game = GameState(moves=uci_moves)
            lczero_input_tensor = lczero_utils.board_from_backend(
                tiny_lczero_backend, lczero_game
            )
            assert (board_tensor == lczero_input_tensor).all()
