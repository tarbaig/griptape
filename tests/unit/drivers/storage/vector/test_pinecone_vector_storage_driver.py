import pytest

from griptape.artifacts import TextArtifact
from griptape.drivers import PineconeVectorStorageDriver
from tests.mocks.mock_embedding_driver import MockEmbeddingDriver


class TestOpenAiEmbeddingDriver:
    @pytest.fixture(autouse=True)
    def mock_openai_embedding_create(self, mocker):
        # Create a fake response
        fake_query_response = {
            "matches": [
                {
                    "values": [0, 1, 0],
                    "score": 42,
                    "metadata": {
                        "foo": "bar"
                    }
                }
            ],
            "namespace": "foobar"
        }

        mocker.patch('pinecone.Index.upsert', return_value=None)
        mocker.patch('pinecone.Index.query', return_value=fake_query_response)
        mocker.patch('pinecone.create_index', return_value=None)

    @pytest.fixture
    def driver(self):
        return PineconeVectorStorageDriver(
            api_key="foobar",
            index_name="test"
        )

    def test_insert_test_artifact(self, driver):
        assert driver.insert_text_artifact(
            TextArtifact("foo"),
            vector_id="foo"
        ) == "foo"

    def test_insert_vector(self, driver):
        assert driver.insert_vector([0, 1, 2], vector_id="foo") == "foo"
        assert isinstance(driver.insert_vector([0, 1, 2]), str)

    def test_insert_text(self, driver):
        assert driver.insert_text("foo", vector_id="foo") == "foo"
        assert isinstance(driver.insert_text("foo"), str)

    def test_query(self, driver):
        assert driver.query("test")[0].vector == [0, 1, 0]

    def test_create_index(self, driver):
        assert driver.create_index("test") is None
