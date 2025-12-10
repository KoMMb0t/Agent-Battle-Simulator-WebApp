import threading
import time
from typing import Dict, Optional, Tuple


class BattleStorage:
    """Thread-safe in-memory battle storage with TTL-based cleanup."""

    def __init__(self, ttl_seconds: int = 3600, cleanup_interval: int = 300):
        self.ttl_seconds = ttl_seconds
        self.cleanup_interval = cleanup_interval
        self._battles: Dict[str, Tuple[object, float]] = {}
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._cleanup_thread = threading.Thread(target=self._cleanup_loop, daemon=True)
        self._cleanup_thread.start()

    def _cleanup_loop(self) -> None:
        while not self._stop_event.wait(self.cleanup_interval):
            self.cleanup()

    def stop(self) -> None:
        self._stop_event.set()
        self._cleanup_thread.join(timeout=1)

    def set(self, battle_id: str, battle: object) -> None:
        with self._lock:
            self._battles[battle_id] = (battle, time.time())

    def get(self, battle_id: str) -> Optional[object]:
        with self._lock:
            entry = self._battles.get(battle_id)
            if not entry:
                return None

            battle, created_at = entry
            if time.time() - created_at > self.ttl_seconds:
                del self._battles[battle_id]
                return None
            return battle

    def has(self, battle_id: str) -> bool:
        return self.get(battle_id) is not None

    def cleanup(self) -> None:
        cutoff = time.time() - self.ttl_seconds
        with self._lock:
            expired = [battle_id for battle_id, (_, created_at) in self._battles.items()
                       if created_at < cutoff]
            for battle_id in expired:
                del self._battles[battle_id]

    def __contains__(self, battle_id: str) -> bool:
        return self.has(battle_id)

    def __len__(self) -> int:
        with self._lock:
            return len(self._battles)
