import re
from chromadb import PersistentClient
from chromadb.utils import embedding_functions

# === Настройка ChromaDB ===
embedding_fn = embedding_functions.DefaultEmbeddingFunction()
client = PersistentClient(path="./chroma_storage")
collection_name = "khrustalnaia_tufelka"

collection = client.get_or_create_collection(
    name=collection_name,
    embedding_function=embedding_fn
)

# === Функции ===
def split_into_sentences(text: str):
    """
    Разбивает текст на предложения.
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]

def get_three_sentences_with_query(text: str, query: str):
    """
    Находит и возвращает до 3 предложений, где встречается слово или фраза.
    """
    sentences = split_into_sentences(text)
    query_lower = query.lower()
    found = [s for s in sentences if query_lower in s.lower()]
    return found[:3] if found else None

def search_top3_sentences(query: str):
    """
    Поиск трёх лучших документов с запросом
    и вывод до 3 предложений из каждого.
    """
    try:
        if collection.count() == 0:
            print(f"⚠️ Коллекция '{collection_name}' пуста.")
            return

        results = collection.query(
            query_texts=[query],
            n_results=3,  # берём три лучших совпадения
            include=['documents', 'distances']
        )

        documents = results.get("documents", [[]])[0]
        distances = results.get("distances", [[]])[0]

        if not documents:
            print("\n⚠️ Ничего не найдено.")
            return

        print(f"\n📖 Топ-3 совпадения по запросу: «{query}»")

        for i, doc in enumerate(documents):
            similarity = (1 - distances[i]) * 100
            found_sentences = get_three_sentences_with_query(doc, query)

            print(f"\n🔹 Совпадение {i+1} (похожесть: {similarity:.2f}%)")

            if found_sentences:
                for sent in found_sentences:
                    print(f"- {sent}")
            else:
                # если точного вхождения нет, показываем первые 3 предложения
                sentences = split_into_sentences(doc)
                for sent in sentences[:3]:
                    print(f"- {sent}")

    except Exception as e:
        print(f"\n[!] Ошибка: {e}")

# === Запуск программы ===
if __name__ == "__main__":
    print(f"\n📚 Поиск предложений в коллекции: '{collection_name}'")
    try:
        user_query = input("🔍 Введите слово или фразу: ").strip()
        if user_query:
            search_top3_sentences(user_query)
        else:
            print("⚠️ Пустой запрос.")
    except KeyboardInterrupt:
        print("\n❌ Поиск прерван пользователем.")
