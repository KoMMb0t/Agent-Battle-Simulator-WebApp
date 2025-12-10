"""
Battle Storage Layer
Provides flexible storage backend for battles with support for:
- SQLite (persistent, production-ready)
- Redis (optional, high-performance)
- In-memory (fallback, development)
"""

import json
import os
import pickle
import sqlite3
import time
from typing import Optional, Tuple

try:
    from redis import Redis
    from redis.exceptions import RedisError
except ImportError:
    Redis = None
    RedisError = Exception


class BattleStorage:
    """
    Unified storage layer for battles with TTL support and automatic cleanup.
    
    Storage priority:
    1. Redis (if REDIS_URL is set and redis-py is installed)
    2. SQLite (if BATTLE_DB_PATH is set or USE_SQLITE=true)
    3. In-memory (fallback)
    """

    def __init__(self, ttl_seconds: Optional[int] = None):
        self.ttl_seconds = ttl_seconds or int(os.environ.get('BATTLE_TTL_SECONDS', 3600))
        self.redis_url = os.environ.get('REDIS_URL')
        self.db_path = os.environ.get('BATTLE_DB_PATH', 'battles.db')
        self.use_sqlite = os.environ.get('USE_SQLITE', 'false').lower() == 'true' or os.environ.get('BATTLE_DB_PATH')
        
        # Initialize storage backends
        self.redis_client = self._init_redis_client()
        self.sqlite_enabled = self.use_sqlite and self._init_sqlite_db()
        self._memory_store: dict[str, tuple[float, bytes]] = {}
        
        # Determine active backend
        self.backend = self._determine_backend()

    def _determine_backend(self) -> str:
        """Determine which storage backend to use"""
        if self.redis_client:
            return 'redis'
        elif self.sqlite_enabled:
            return 'sqlite'
        else:
            return 'memory'

    def _init_redis_client(self) -> Optional[Redis]:
        """Initialize Redis client if available"""
        if not self.redis_url or Redis is None:
            return None
        try:
            client = Redis.from_url(self.redis_url)
            client.ping()  # Validate connection
            return client
        except Exception:
            return None

    def _init_sqlite_db(self) -> bool:
        """Initialize SQLite database schema"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS battles (
                        battle_id TEXT PRIMARY KEY,
                        data BLOB NOT NULL,
                        created_at REAL NOT NULL,
                        updated_at REAL NOT NULL,
                        expires_at REAL NOT NULL
                    )
                    """
                )
                conn.execute(
                    """
                    CREATE INDEX IF NOT EXISTS idx_battles_expires_at 
                    ON battles(expires_at)
                    """
                )
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS agent_stats (
                        agent_name TEXT PRIMARY KEY,
                        wins INTEGER DEFAULT 0,
                        losses INTEGER DEFAULT 0,
                        total_battles INTEGER DEFAULT 0,
                        last_battle_at REAL
                    )
                    """
                )
            return True
        except Exception as e:
            print(f"SQLite initialization failed: {e}")
            return False

    def _get_db_connection(self):
        """Create a SQLite connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _key(self, battle_id: str) -> str:
        """Generate Redis key for battle"""
        return f"battle:{battle_id}"

    def save_battle(self, battle_id: str, battle) -> None:
        """Save battle to storage with TTL"""
        payload = pickle.dumps(battle)
        
        # Try Redis first
        if self.backend == 'redis' and self.redis_client:
            try:
                self.redis_client.setex(self._key(battle_id), self.ttl_seconds, payload)
                return
            except RedisError:
                # Fall through to next backend
                pass

        # Try SQLite
        if self.backend == 'sqlite' or self.sqlite_enabled:
            try:
                now = time.time()
                expires_at = now + self.ttl_seconds
                with self._get_db_connection() as conn:
                    conn.execute(
                        """
                        INSERT INTO battles (battle_id, data, created_at, updated_at, expires_at)
                        VALUES (?, ?, ?, ?, ?)
                        ON CONFLICT(battle_id) DO UPDATE SET
                            data = excluded.data,
                            updated_at = excluded.updated_at,
                            expires_at = excluded.expires_at
                        """,
                        (battle_id, payload, now, now, expires_at)
                    )
                return
            except Exception as e:
                print(f"SQLite save failed: {e}")
                # Fall through to memory

        # Fallback to memory
        expires_at = time.time() + self.ttl_seconds
        self._memory_store[battle_id] = (expires_at, payload)

    def get_battle(self, battle_id: str) -> Tuple[Optional[object], Optional[str]]:
        """
        Retrieve battle from storage.
        Returns: (battle_object, error_reason)
        error_reason can be: None (success), 'expired', 'not_found'
        """
        self.prune_expired()

        # Try Redis first
        if self.backend == 'redis' and self.redis_client:
            try:
                data = self.redis_client.get(self._key(battle_id))
                if data is None:
                    return None, 'not_found'
                # Extend TTL on access
                self.redis_client.expire(self._key(battle_id), self.ttl_seconds)
                return pickle.loads(data), None
            except RedisError:
                # Fall through to next backend
                pass

        # Try SQLite
        if self.backend == 'sqlite' or self.sqlite_enabled:
            try:
                with self._get_db_connection() as conn:
                    row = conn.execute(
                        "SELECT data, expires_at FROM battles WHERE battle_id = ?",
                        (battle_id,)
                    ).fetchone()
                    
                    if not row:
                        return None, 'not_found'
                    
                    # Check expiration
                    if row['expires_at'] < time.time():
                        conn.execute("DELETE FROM battles WHERE battle_id = ?", (battle_id,))
                        return None, 'expired'
                    
                    # Extend TTL on access
                    new_expires_at = time.time() + self.ttl_seconds
                    conn.execute(
                        "UPDATE battles SET updated_at = ?, expires_at = ? WHERE battle_id = ?",
                        (time.time(), new_expires_at, battle_id)
                    )
                    
                    return pickle.loads(row['data']), None
            except Exception as e:
                print(f"SQLite get failed: {e}")
                # Fall through to memory

        # Fallback to memory
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
        """Delete battle from storage"""
        # Redis
        if self.redis_client:
            try:
                self.redis_client.delete(self._key(battle_id))
            except RedisError:
                pass

        # SQLite
        if self.sqlite_enabled:
            try:
                with self._get_db_connection() as conn:
                    conn.execute("DELETE FROM battles WHERE battle_id = ?", (battle_id,))
            except Exception:
                pass

        # Memory
        self._memory_store.pop(battle_id, None)

    def prune_expired(self) -> None:
        """Remove expired battles from storage"""
        # Redis handles TTL automatically
        if self.backend == 'redis':
            return

        # SQLite cleanup
        if self.sqlite_enabled:
            try:
                with self._get_db_connection() as conn:
                    conn.execute("DELETE FROM battles WHERE expires_at < ?", (time.time(),))
            except Exception:
                pass

        # Memory cleanup
        now = time.time()
        expired_keys = [
            bid for bid, (expires_at, _) in self._memory_store.items()
            if expires_at < now
        ]
        for bid in expired_keys:
            del self._memory_store[bid]

    def record_agent_stats(self, agent_name: str, won: bool) -> None:
        """Record agent battle statistics (SQLite only)"""
        if not self.sqlite_enabled:
            return

        try:
            with self._get_db_connection() as conn:
                conn.execute(
                    """
                    INSERT INTO agent_stats (agent_name, wins, losses, total_battles, last_battle_at)
                    VALUES (?, ?, ?, 1, ?)
                    ON CONFLICT(agent_name) DO UPDATE SET
                        wins = wins + excluded.wins,
                        losses = losses + excluded.losses,
                        total_battles = total_battles + 1,
                        last_battle_at = excluded.last_battle_at
                    """,
                    (agent_name, 1 if won else 0, 0 if won else 1, time.time())
                )
        except Exception as e:
            print(f"Failed to record agent stats: {e}")

    def get_agent_stats(self, agent_name: str) -> Optional[dict]:
        """Get agent battle statistics (SQLite only)"""
        if not self.sqlite_enabled:
            return None

        try:
            with self._get_db_connection() as conn:
                row = conn.execute(
                    "SELECT * FROM agent_stats WHERE agent_name = ?",
                    (agent_name,)
                ).fetchone()
                
                if not row:
                    return None
                
                return {
                    'agent_name': row['agent_name'],
                    'wins': row['wins'],
                    'losses': row['losses'],
                    'total_battles': row['total_battles'],
                    'win_rate': row['wins'] / row['total_battles'] if row['total_battles'] > 0 else 0,
                    'last_battle_at': row['last_battle_at']
                }
        except Exception as e:
            print(f"Failed to get agent stats: {e}")
            return None

    def get_storage_info(self) -> dict:
        """Get information about the active storage backend"""
        info = {
            'backend': self.backend,
            'ttl_seconds': self.ttl_seconds,
        }
        
        if self.backend == 'sqlite':
            try:
                with self._get_db_connection() as conn:
                    battle_count = conn.execute("SELECT COUNT(*) FROM battles").fetchone()[0]
                    info['battle_count'] = battle_count
            except Exception:
                pass
        elif self.backend == 'memory':
            info['battle_count'] = len(self._memory_store)
        
        return info
