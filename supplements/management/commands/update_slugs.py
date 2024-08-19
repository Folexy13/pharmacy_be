from django.core.management.base import BaseCommand
from supplements.models import Category, SubCategory

class Command(BaseCommand):
    help = 'Update slugs for all existing categories and subcategories.'

    def handle(self, *args, **kwargs):
        self.update_category_slugs()
        self.update_subcategory_slugs()

    def update_category_slugs(self):
        categories = Category.objects.all()
        for category in categories:
            if not category.slug:
                category.save()  # This will trigger the save method logic
                self.stdout.write(f"Updated slug for category {category.name}: {category.slug}")

    def update_subcategory_slugs(self):
        subcategories = SubCategory.objects.all()
        for subcategory in subcategories:
            if not subcategory.slug:
                subcategory.save()  # This will trigger the save method logic
                self.stdout.write(f"Updated slug for subcategory {subcategory.name}: {subcategory.slug}")
