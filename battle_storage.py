import os
import pickle
import time
from typing import Optional, Tuple

try:
    from redis import Redis
    from redis.exceptions import RedisError
except ImportError:  # Redis optional
    Redis = None
    RedisError = Exception


class BattleStorage:
    """Lightweight storage layer for battles with TTL and pruning."""

    def __init__(self, ttl_seconds: Optional[int] = None):
        self.ttl_seconds = ttl_seconds or int(os.environ.get('BATTLE_TTL_SECONDS', 3600))
        self.redis_url = os.environ.get('REDIS_URL')
        self.redis_client = self._init_redis_client()
        self._memory_store: dict[str, tuple[float, bytes]] = {}

    def _init_redis_client(self) -> Optional[Redis]:
        if not self.redis_url or Redis is None:
            return None
        try:
            client = Redis.from_url(self.redis_url)
            # Validate connection lazily; will raise during first operation if unavailable
            return client
        except Exception:
            return None

    def _key(self, battle_id: str) -> str:
        return f"battle:{battle_id}"

    def save_battle(self, battle_id: str, battle) -> None:
        payload = pickle.dumps(battle)
        if self.redis_client:
            try:
                self.redis_client.setex(self._key(battle_id), self.ttl_seconds, payload)
                return
            except RedisError:
                # Fall back to memory if Redis is unavailable
                pass

        expires_at = time.time() + self.ttl_seconds
        self._memory_store[battle_id] = (expires_at, payload)

    def get_battle(self, battle_id: str) -> Tuple[Optional[object], Optional[str]]:
        """
        Return battle and reason. Reason is 'expired' or 'not_found'.
        """
        self.prune_expired()

        if self.redis_client:
            try:
                data = self.redis_client.get(self._key(battle_id))
                if data is None:
                    return None, 'not_found'
                # Extend TTL on access
                self.redis_client.expire(self._key(battle_id), self.ttl_seconds)
                return pickle.loads(data), None
            except RedisError:
                # Redis unreachable: treat as not found so client can recover
                return None, 'not_found'

        record = self._memory_store.get(battle_id)
        if not record:
            return None, 'not_found'

        expires_at, data = record
        if expires_at < time.time():
            del self._memory_store[battle_id]
            return None, 'expired'

        # Refresh TTL on access
        self._memory_store[battle_id] = (time.time() + self.ttl_seconds, data)
        return pickle.loads(data), None

    def delete_battle(self, battle_id: str) -> None:
        if self.redis_client:
            try:
                self.redis_client.delete(self._key(battle_id))
            except RedisError:
                pass
        self._memory_store.pop(battle_id, None)

    def prune_expired(self) -> None:
        if self.redis_client:
            # Redis handles TTL; nothing to prune
            return

        now = time.time()
        expired_keys = [bid for bid, (expires_at, _) in self._memory_store.items() if expires_at < now]
        for bid in expired_keys:
            del self._memory_store[bid]
