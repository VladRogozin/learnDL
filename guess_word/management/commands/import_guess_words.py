import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from guess_word.models import GuessWord


class Command(BaseCommand):
    help = 'Импорт слов для угадывания из JSON'

    def handle(self, *args, **options):
        # Ваши данные в формате JSON
        json_data = '''
            {
                "car": ["fast", "red"],
                "book": ["interesting", "thick"],
                "cat": ["fluffy", "playful"],
                "house": ["big", "modern"],
                "apple": ["red", "juicy"],
                "computer": ["powerful", "lightweight"],
                "planet": ["red", "small"],
                "guitar": ["acoustic", "ancient"],
                "flower": ["beautiful", "fragrant"],
                "human": ["smart", "friendly"],
                "banana": ["yellow", "sweet"],
                "mountain": ["tall", "snowy"],
                "sun": ["bright", "hot"],
                "window": ["large", "glass"],
                "ocean": ["blue", "vast"],
                "pen": ["blue", "plastic"],
                "star": ["bright", "distant"],
                "tree": ["tall", "green"],
                "milk": ["white", "nutritious"],
                "phone": ["modern", "smart"]
            }
        '''

        # Загрузка данных из JSON
        data = json.loads(json_data)

        for word, attributes in data.items():
            guess_word = GuessWord(
                guess_word=word,
                help_words=", ".join(attributes),
                level="A1",
                language="en",
            )

            # Строим путь к изображению в директории media/guess_word_image/
            image_path = os.path.join(settings.MEDIA_ROOT, 'guess_word_image', f"{word}.jpg")

            # Проверяем существование файла перед добавлением
            if os.path.exists(image_path):
                with open(image_path, 'rb') as img_file:
                    guess_word.photo.save(f"{word}.jpg", img_file, save=True)

            guess_word.save()

        self.stdout.write(self.style.SUCCESS('Успешно добавлены слова для угадывания'))