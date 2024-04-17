
from django.core.management import BaseCommand
from faker import Faker
from courses.models import Course, Category, Trainer
import random


class Command(BaseCommand):

    def __init__(self):
        super().__init__()
        self.faker = Faker()
        self.category = Category.objects.all()
        self.category_list = ["test1", "test2", "test3"]

    def handle(self, *args, **options):
        for item in self.category_list:
            Category.objects.get_or_create(name=item)



        for _ in range(10):
            course = Course.objects.create(
                title = self.faker.name(),
                content = self.faker.text(), 
                teacher = Trainer.objects.get(id=1),
                status = True,
            )
            cat = random.choices(list(self.category))

            course.category.set(cat)
        