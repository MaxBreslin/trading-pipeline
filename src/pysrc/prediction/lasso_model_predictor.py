from pysrc import intern
from pysrc.utils.trade_types import Trade
from pysrc.utils.circular_buffer import CircularBuffer

import logging
from sklearn.linear_model import Lasso
from typing import Optional, Literal
import numpy as np


class LassoModelPredictor:
    def __init__(
        self,
        alpha: float = 1.0,
        fit_intercept: bool = True,
        copy_X: bool = True,
        max_iter: int = 1000,
        tol: float = 1e-4,
        warm_start: bool = True,
        positive: bool = False,
        random_state: Optional[int] = None,
        selection: Literal["cyclic", "random"] = "cyclic",
    ) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)

        self.TRAIN_LENGTH = 10

        self.model = Lasso(
            alpha=alpha,
            fit_intercept=fit_intercept,
            copy_X=copy_X,
            max_iter=max_iter,
            tol=tol,
            warm_start=warm_start,
            positive=positive,
            random_state=random_state,
            selection=selection,
        )

        self.n_trades_feature_gen = intern.NTradesFeature()
        self.percent_buy_feature_gen = intern.PercentBuyFeature()
        self.percent_sell_feature_gen = intern.PercentSellFeature()
        self.five_tick_volume_feature_gen = intern.FiveTickVolumeFeature()

        self.feature_gens = [
            self.n_trades_feature_gen,
            self.percent_buy_feature_gen,
            self.percent_sell_feature_gen,
            self.five_tick_volume_feature_gen,
        ]

        self.return_1s_gen = intern.ReturnOneS()

        self.features = CircularBuffer(self.TRAIN_LENGTH, len(self.feature_gens))
        self.targets = CircularBuffer(self.TRAIN_LENGTH)

    def _predict(self, features: list[float]) -> float:
        self.model.fit(np.asarray(self.features), np.asarray(self.targets))
        prediction = self.model.predict(
            np.asarray(features).reshape((1, len(self.feature_gens)))
        )
        assert prediction.shape[0] == 1
        return float(prediction[0])

    def _compute_features(self, data: list[Trade]) -> list[float]:
        return [feature_gen.compute_feature(data) for feature_gen in self.feature_gens]

    def _compute_target(self, data: list[Trade]) -> float:
        return float(self.return_1s_gen.compute_target(data))

    def on_tick(self, data: list[Trade]) -> Optional[float]:
        new_features = self._compute_features(data)
        new_target = self._compute_target(data)

        prediction = None
        if len(self.features) == self.TRAIN_LENGTH:
            prediction = self._predict(new_features)

        self.features.push(new_features)
        self.targets.push(new_target)

        return prediction

    def get_last_target(self) -> float:
        if len(self.targets) == 0:
            return 0.0
        return float(self.targets.get_buffer()[-1])
