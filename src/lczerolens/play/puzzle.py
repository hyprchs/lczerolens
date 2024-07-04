"""Preproces functions for chess puzzles."""

from dataclasses import dataclass
from typing import Dict, List, Union, Tuple, Optional

import chess
import torch
from datasets import Features, Value

from lczerolens.encodings import move as move_encodings
from .sampling import Sampler


PUZZLE_DATASET_FEATURES = Features(
    {
        "PuzzleId": Value("string"),
        "FEN": Value("string"),
        "Moves": Value("string"),
        "Rating": Value("int64"),
        "RatingDeviation": Value("int64"),
        "Popularity": Value("int64"),
        "NbPlays": Value("int64"),
        "Themes": Value("string"),
        "GameUrl": Value("string"),
        "OpeningTags": Value("string"),
    }
)


@dataclass
class Puzzle:
    puzzle_id: str
    fen: str
    initial_move: chess.Move
    moves: List[chess.Move]
    rating: int
    rating_deviation: int
    popularity: int
    nb_plays: int
    themes: List[str]
    game_url: str
    opening_tags: List[str]

    @classmethod
    def from_dict(cls, obj: Dict[str, Union[str, int]]) -> "Puzzle":
        uci_moves = obj["Moves"].split()
        moves = [chess.Move.from_uci(uci_move) for uci_move in uci_moves]
        return cls(
            puzzle_id=obj["PuzzleId"],
            fen=obj["FEN"],
            initial_move=moves[0],
            moves=moves[1:],
            rating=obj["Rating"],
            rating_deviation=obj["RatingDeviation"],
            popularity=obj["Popularity"],
            nb_plays=obj["NbPlays"],
            themes=obj["Themes"].split(),
            game_url=obj["GameUrl"],
            opening_tags=obj["OpeningTags"].split(),
        )

    @property
    def initial_board(self) -> chess.Board:
        board = chess.Board(self.fen)
        board.push(self.initial_move)
        return board

    def evaluate(self, sampler: Sampler, use_perplexity: bool = False) -> Tuple[float, Optional[float]]:
        board = self.initial_board
        length = len(self.moves)
        score = 0.0
        perplexity = 1.0 if use_perplexity else 0.0
        for move in self.moves:
            utility, legal_indices, _ = sampler.get_utility(board)
            if use_perplexity:
                index = move_encodings.encode_move(move, board.turn)
                probs = torch.softmax(utility, dim=0)
                perplexity *= probs[legal_indices == index].item()
            predicted_move = sampler.choose_move(board, utility, legal_indices)
            if predicted_move == move:
                score += 1
            board.push(move)
        score /= length
        if not use_perplexity or perplexity == 0:
            perplexity = None
        else:
            perplexity = perplexity ** (-1 / length)
        return score, perplexity

    def __repr__(self) -> str:
        return self.initial_board.__repr__()

    def _repr_svg_(self) -> str:
        return self.initial_board._repr_svg_()