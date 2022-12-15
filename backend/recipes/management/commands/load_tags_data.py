import json
from django.core.management import BaseCommand
from tqdm import tqdm
from typing import Any, Optional
from recipes.models import Tag


class Command(BaseCommand):
    """
    Класс команды для загрузки данных
    игнредиентов из json файла.
    """
    filename: str = 'tags'
    file: str = 'static/data/' + filename + '.json'

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        if Tag.objects.exists():
            self.stdout.write(
                'Initial data '
                '\033[0;33;48m{}\033[0;0m '
                'already exists.'.format(self.filename)
            )
            return

        with open(self.file, 'rb') as fin:
            data: list[dict[str, str]] = json.load(fin)

            for entry in tqdm(data):
                tag = Tag()
                tag.name = entry.get('name')
                tag.color = entry.get('color')
                tag.slug = entry.get('slug')
                tag.save()

        return self.stdout.write(
            'Loading \033[1m{}\033[0m data successfully done.'
            .format(self.filename)
        )
