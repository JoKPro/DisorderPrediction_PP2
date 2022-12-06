import numpy as np
import h5py
import os
import ast

class Dataset:
    """
    Dataset class.
    The data is structured in dictionaries: {label: value}.
    Access a particular protein with index or protein ID (e.g. DATASET[0], DATASET["22331"].

    """


    def __init__(self, embeddings_path, scores_path, seq_ids_path, split={"train": 0.8, "val": 0.2}):

        self.raw_ids = None
        self.raw_seqs = None
        self.embeddings = None
        self.scores = None

        assert os.path.exists(embeddings_path), f"Embeddings file not found in path: {embeddings_path}"
        assert os.path.exists(scores_path), f"Scores file not found in path: {scores_path}"
        assert os.path.exists(scores_path), f"Scores file not found in path: {seq_ids_path}"
        assert sum(split.values()) == 1.0, "Invalid split"

        self.embeddings_path = embeddings_path
        self.scores_path = scores_path
        self.seq_ids_path = seq_ids_path

        self.split = split

        self.create_dataset()
        pass

    def __getitem__(self, idx):
        """
        Access a dataset element with index or label.
        :param idx: integer or string
        :returns: tuple, (embeddings_dict, scores_dict, raw_sequence_dict)
        """
        if isinstance(idx, slice):
            raise (Exception("Not yet implemented :(("))
        elif isinstance(idx, int):
            idx = self.raw_ids[idx]
            print(f"idx: {idx}")
        elif not isinstance(idx, str):
            raise (ValueError("Invalid index type"))

        return (self.embeddings[idx], self.scores[idx], self.raw_seqs[idx])

    def __len__(self):
        pass

    def create_dataset(self):

        with h5py.File(self.embeddings_path, "r") as embeddings_h5:
            self.embeddings = {id: np.array(embs) for id, embs in embeddings_h5.items()}

        with open(self.scores_path, "r") as scores_file:
            lines = scores_file.readlines()
            raw_scores = [np.array(ast.literal_eval(line)) for line in lines]
        with open(self.seq_ids_path, "r") as id_file:
            lines = id_file.readlines()
            self.raw_ids = [str(line.split(" ")[0]) for line in lines]
            raw_seqs = [line.split(" ")[1].strip() for line in lines]

        self.scores = dict(zip(self.raw_ids, raw_scores))
        self.raw_seqs = dict(zip(self.raw_ids, raw_seqs))

        pass
