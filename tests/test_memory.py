"""Tests para el módulo de memoria vectorial."""
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from ai_mastery.cli import cli
from ai_mastery import memory


def test_memory_manager_add_documents() -> None:
    """Test que verifica que MemoryManager.add_documents añade documentos."""
    mock_collection = MagicMock()
    mock_client = MagicMock()
    mock_client.get_or_create_collection.return_value = mock_collection
    with patch("chromadb.PersistentClient", return_value=mock_client):
        with patch("ai_mastery.memory.MemoryManager._get_embedding", return_value=[0.1, 0.2, 0.3]):
            manager = memory.MemoryManager(collection_name="test", persist_directory=":memory:")
            manager.client = mock_client
            manager.collection = mock_collection
            docs = ["Documento 1", "Documento 2"]
            count = manager.add_documents(docs)
            assert count == 2
            mock_collection.add.assert_called_once()


def test_memory_manager_query() -> None:
    """Test que verifica que MemoryManager.query devuelve resultados."""
    mock_collection = MagicMock()
    mock_collection.query.return_value = {
        "documents": [["Doc 1", "Doc 2"]],
        "metadatas": [[{}, {}]],
        "distances": [[0.1, 0.2]],
    }
    mock_client = MagicMock()
    mock_client.get_or_create_collection.return_value = mock_collection
    with patch("chromadb.PersistentClient", return_value=mock_client):
        with patch("ai_mastery.memory.MemoryManager._get_embedding", return_value=[0.1, 0.2, 0.3]):
            manager = memory.MemoryManager(collection_name="test", persist_directory=":memory:")
            manager.client = mock_client
            manager.collection = mock_collection
            results = manager.query("consulta")
            assert len(results) == 2
            assert results[0]["content"] == "Doc 1"


def test_ingest_command() -> None:
    """Test que verifica el comando ingest."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("docs.txt", "w", encoding="utf-8") as f:
            f.write("Línea 1\nLínea 2\n")
        # Mockear MemoryManager completo para evitar inicializar ChromaDB
        with patch("ai_mastery.memory.MemoryManager") as MockManager:
            mock_instance = MagicMock()
            mock_instance.add_documents.return_value = 2
            MockManager.return_value = mock_instance
            result = runner.invoke(cli, ["ingest", "docs.txt"])
            assert result.exit_code == 0
            assert "2 documentos ingeridos" in result.output


def test_query_command() -> None:
    """Test que verifica el comando query."""
    runner = CliRunner()
    mock_results = [
        {"content": "Resultado 1", "distance": 0.1, "metadata": {}},
        {"content": "Resultado 2", "distance": 0.2, "metadata": {}},
    ]
    # Mockear MemoryManager completo
    with patch("ai_mastery.memory.MemoryManager") as MockManager:
        mock_instance = MagicMock()
        mock_instance.query.return_value = mock_results
        MockManager.return_value = mock_instance
        result = runner.invoke(cli, ["query", "pregunta"])
        assert result.exit_code == 0
        assert "Resultado 1" in result.output
        assert "Resultado 2" in result.output