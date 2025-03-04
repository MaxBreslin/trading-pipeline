from pysrc.intern import DataClient  # type: ignore
from pysrc.prediction.lasso_model_predictor import LassoModelPredictor
from pysrc.utils.trade_types import Trade

import pandas as pd
import os


def run_iterations(timestamp: int, iters: int, out_file: str) -> None:
    out_file = "output/"
    os.makedirs(out_file, exist_ok=True)

    dc = DataClient(
        "https://api.gemini.com/v1", "/trades/btcusd", timestamp, 0, 50, timestamp
    )

    lmp = LassoModelPredictor()

    predictions_and_targets = []

    iter = 0

    while iter < lmp.TRAIN_LENGTH:
        data = dc.get_data()
        while len(data) == 0:
            dc.timestamp += 1
            dc.with_timestamp += 1
            data = dc.get_data()

        data = [Trade(float(d.price), float(d.volume), bool(d.side)) for d in data]
        lmp.on_tick(data)
        dc.timestamp += 1
        dc.with_timestamp += 1
        iter += 1

    iter = 0
    while iter < iters:
        data = dc.get_data()
        while len(data) == 0:
            dc.timestamp += 1
            dc.with_timestamp += 1
            data = dc.get_data()

        data = [Trade(float(d.price), float(d.volume), bool(d.side)) for d in data]
        expected_target = lmp.get_last_target()
        prediction = lmp.on_tick(data)

        predictions_and_targets.append(
            {
                "timestamp": dc.timestamp,
                "prediction": prediction,
                "target": expected_target,
            }
        )

        dc.timestamp += 1
        dc.with_timestamp += 1
        iter += 1

    df = pd.DataFrame(
        predictions_and_targets, columns=["timestamp", "prediction", "target"]
    )
    df.to_csv(f"{out_file}output.csv", index=False)


def calculate_corr(in_file: str) -> float:
    df = pd.read_csv(in_file)
    corr = df["prediction"].corr(df["target"])

    return float(corr)
