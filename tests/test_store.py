from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from app.store import SQLiteMemoryStore, cosine_similarity


class MemoryStoreTests(unittest.TestCase):
    def test_cosine_similarity(self) -> None:
        self.assertAlmostEqual(cosine_similarity([1, 0], [1, 0]), 1.0)
        self.assertAlmostEqual(cosine_similarity([1, 0], [0, 1]), 0.0)

    def test_search_is_semantic_ranked_and_user_scoped(self) -> None:
        with TemporaryDirectory() as directory:
            store = SQLiteMemoryStore(str(Path(directory) / "memory.db"))
            store.add(user_id="a", conversation_id="c", role="user", content="민트초코를 좋아해", importance=0.8, embedding=[1.0, 0.0])
            store.add(user_id="a", conversation_id="c", role="user", content="자동차를 고쳤어", importance=0.5, embedding=[0.0, 1.0])
            store.add(user_id="b", conversation_id="c", role="user", content="다른 사용자 비밀", importance=1.0, embedding=[1.0, 0.0])

            found = store.search(
                user_id="a",
                query_embedding=[0.9, 0.1],
                top_k=2,
                candidate_limit=10,
                half_life_days=30,
                now=datetime.now(timezone.utc),
            )

            self.assertEqual(found[0].memory.content, "민트초코를 좋아해")
            self.assertTrue(all(item.memory.user_id == "a" for item in found))
            self.assertEqual(len(found), 2)

    def test_dimension_mismatch_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            cosine_similarity([1.0], [1.0, 0.0])


if __name__ == "__main__":
    unittest.main()

