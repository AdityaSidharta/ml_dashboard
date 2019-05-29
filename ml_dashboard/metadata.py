import os
import pandas as pd

from ml_dashboard.io import read_yaml


class Metadata:
    def __init__(self, config=None):
        self.prediction_df = None
        self.prediction_key = None
        self.prediction_timestamp = None
        self.prediction_value = None

        self.groundtruth_df = None
        self.groundtruth_key = None
        self.groundtruth_value = None

        self.prediction_cards = {}
        self.groundtruth_cards = {}

        if config is not None:
            self.load_config(config)

    def assert_prediction(self):
        assert self.prediction_df is not None
        assert self.prediction_key is not None
        assert self.prediction_timestamp is not None
        assert self.prediction_value is not None

    def assert_groundtruth(self):
        assert self.groundtruth_df is not None
        assert self.groundtruth_key is not None
        assert self.groundtruth_value is not None

    def assert_prediction_cards(self):
        assert len(self.prediction_cards) > 0

    def assert_groundtruth_cards(self):
        assert len(self.groundtruth_cards) > 0

    def load_prediction(self, source, source_path, table_name, key, timestamp, value):
        if source == "csv":
            path = os.path.join(source_path, "{}.csv".format(table_name))
            self.prediction_df = pd.read_csv(path)
            self.prediction_key = key
            self.prediction_timestamp = timestamp
            self.prediction_value = value
        else:
            raise NotImplementedError("Other forms of sources is not supported yet")

    def load_groundtruth(self, source, source_path, table_name, key, value):
        if source == "csv":
            path = os.path.join(source_path, "{}.csv".format(table_name))
            self.groundtruth_df = pd.read_csv(path)
            self.groundtruth_key = key
            self.groundtruth_value = value
        else:
            raise NotImplementedError("Other form of sources is not supported yet")

    def insert_cards(self, card_type, row, name, col, plot_type, grouper, granularity, aggregation):
        if card_type == "prediction":
            cards = self.prediction_cards
        elif card_type == "groundtruth":
            cards = self.groundtruth_cards
        else:
            raise ValueError("Unrecognized card_type")

        if row not in cards.keys():
            cards[row] = []
        cards[row].append(
            {
                "name": name,
                "col": col,
                "plot_type": plot_type,
                "grouper": grouper,
                "granularity": granularity,
                "aggregation": aggregation,
            }
        )

    def delete_cards(self, card_type, row, idx):
        if card_type == "prediction":
            cards = self.prediction_cards
        elif card_type == "groundtruth":
            cards = self.groundtruth_cards
        else:
            raise ValueError("Unrecognized card_type")

        assert row in cards.keys()
        del cards[row][idx]

    def load_config(self, config):
        config_dict = read_yaml(config)
        prediction_dict = config_dict["prediction"]
        groundtruth_dict = config_dict["groundtruth"]
        prediction_cards_list = config_dict["prediction-cards"]
        groundtruth_cards_list = config_dict["groundtruth-cards"]
        self.load_prediction(
            prediction_dict["source"],
            prediction_dict["source_path"],
            prediction_dict["table_name"],
            prediction_dict["primary_key"],
            prediction_dict["timestamp"],
            prediction_dict["prediction_value"],
        )
        self.load_groundtruth(
            groundtruth_dict["source"],
            groundtruth_dict["source_path"],
            groundtruth_dict["table_name"],
            groundtruth_dict["primary_key"],
            groundtruth_dict["target_value"],
        )
        for idx, (value) in enumerate(prediction_cards_list):
            if "aggregation" in value.keys():
                aggregation = value["aggregation"]
            else:
                aggregation = None
            self.insert_cards(
                "prediction",
                value["row"],
                value["name"],
                value["col"],
                value["type"],
                value["grouper"],
                value["granularity"],
                aggregation,
            )
        for idx, (value) in enumerate(groundtruth_cards_list):
            if "aggregation" in value.keys():
                aggregation = value["aggregation"]
            else:
                aggregation = None
            self.insert_cards(
                "groundtruth",
                value["row"],
                value["name"],
                value["col"],
                value["type"],
                value["grouper"],
                value["granularity"],
                aggregation,
            )
