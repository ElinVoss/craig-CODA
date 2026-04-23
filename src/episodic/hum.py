"""
The hum does not start on import. Caller is responsible for instantiation and .start().

Example:
    from src.episodic.hum import Hum
    from src.episodic.store import EpisodicStore

    store = EpisodicStore(db_path)
    hum = Hum(store, decay_rate=0.995, crystallize_threshold=40, interval_minutes=60)
    hum.start()
    # hum.stop() when shutting down
"""
from __future__ import annotations
from apscheduler.schedulers.background import BackgroundScheduler
from .store import EpisodicStore


class Hum:
    def __init__(
        self,
        store: EpisodicStore,
        decay_rate: float,
        crystallize_threshold: int,
        interval_minutes: int,
    ):
        self.store = store
        self.decay_rate = decay_rate
        self.crystallize_threshold = crystallize_threshold
        self._scheduler = BackgroundScheduler()
        self._scheduler.add_job(
            self._cycle, "interval",
            minutes=interval_minutes,
            id="hum_cycle",
        )

    def start(self):
        self._scheduler.start()
        print("Hum started.")

    def stop(self):
        self._scheduler.shutdown()

    def _cycle(self):
        self.store.apply_decay(self.decay_rate, self.crystallize_threshold)
