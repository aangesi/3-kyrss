from chromadb import PersistentClient
from chromadb.utils import embedding_functions
import uuid
import xml.etree.ElementTree as ET


def extract_paragraphs(file_path):
    """
    Извлекает текст из <p> тегов в файле .fb2
    """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Получаем namespace, если есть
        namespaces = {'fb': root.tag.split('}')[0].strip('{')} if '}' in root.tag else {}

        paragraphs = []
        # Ищем все <p> теги
        for p in root.findall(".//fb:p", namespaces) if namespaces else root.findall(".//p"):
            text = ''.join(p.itertext()).strip()
            if text:
                paragraphs.append(text)

        return paragraphs

    except ET.ParseError as e:
        print(f"[!] Ошибка парсинга XML: {e}")
        return []
    except Exception as e:
        print(f"[!] Ошибка при извлечении абзацев: {e}")
        return []


def create_chroma_collection(collection_name="my_book"):
    """
    Создаёт коллекцию с эмбеддинг-функцией
    """
    embedding_fn = embedding_functions.DefaultEmbeddingFunction()
    client = PersistentClient(path="./chroma_storage")

    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_fn
    )

    return collection


def add_paragraphs_to_chroma(collection, paragraphs, metadata=None):
    """
    Добавляет абзацы в ChromaDB с уникальными ID
    """
    ids = [str(uuid.uuid4()) for _ in paragraphs]
    metadatas = [metadata or {}] * len(paragraphs)

    collection.add(
        documents=paragraphs,
        ids=ids,
        metadatas=metadatas
    )

    print(f"[+] Добавлено абзацев: {len(paragraphs)}")


if __name__ == "__main__":
    file_path = "khrustalnaia-tufielka-lp-k_-uebstier.fb2"
    collection_name = "khrustalnaia_tufelka"  # Имя только латиницей

    print("[*] Извлечение абзацев из FB2-файла...")
    paragraphs = extract_paragraphs(file_path)

    if paragraphs:
        print(f"[*] Найдено абзацев: {len(paragraphs)}")
        print("[*] Создание коллекции и добавление в ChromaDB...")
        collection = create_chroma_collection(collection_name)
        add_paragraphs_to_chroma(collection, paragraphs, metadata={"book": "khrustalnaia_tufelka"})
        print("[✅] Готово.")
    else:
        print("[!] Абзацы не найдены в файле.")
