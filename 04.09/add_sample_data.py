from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_library_db import User, Post, Comment, Chat, Base

def add_sample_data():
    engine = create_engine('sqlite:///social_network.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Добавляем пользователей
    user1 = User(username='user1')
    user1.set_password('password1')
    user2 = User(username='user2')
    user2.set_password('password2')

    # Сохраняем пользователей
    session.add(user1)
    session.add(user2)
    session.commit()

    # Добавляем посты
    post1 = Post(content='Это мой первый пост!', user_id=user1.id)
    post2 = Post(content='Привет всем!', user_id=user2.id)
    
    session.add(post1)
    session.add(post2)
    session.commit()

    # Добавляем комментарии
    comment1 = Comment(content='Классный пост!', post_id=post1.id, user_id=user2.id)
    session.add(comment1)
    session.commit()

    # Добавляем чаты
    chat1 = Chat(owner_id=user1.id, content='Привет, как дела?')
    session.add(chat1)
    session.commit()

    print("Тестовые данные добавлены!")

if __name__ == '__main__':
    add_sample_data()