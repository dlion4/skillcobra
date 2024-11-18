# create_categories.py
from django.core.management.base import BaseCommand
from django.db import transaction

from skillcobra.school.models import Category
from skillcobra.school.models import SubCategory


class Command(BaseCommand):
    help = "Populate the database with categories and subcategories for LMS courses."

    def handle(self, *args, **kwargs):
        categories_with_subcategories = {
            "Technology": [
                "Programming & Development",
                "Web Development",
                "Mobile App Development",
                "Artificial Intelligence",
                "Cybersecurity",
                "Blockchain",
                "Game Development",
                "Cloud Computing",
                "DevOps",
                "Data Science & Analytics",
            ],
            "Business & Finance": [
                "Entrepreneurship",
                "Marketing",
                "Finance & Investment",
                "Accounting",
                "Business Analytics",
                "Human Resources",
                "Leadership & Management",
                "Sales Strategies",
                "Digital Marketing",
                "E-commerce",
            ],
            "Arts & Design": [
                "Graphic Design",
                "Video Production",
                "Photography",
                "Animation",
                "UX/UI Design",
                "Fashion Design",
                "Interior Design",
                "Fine Arts",
                "Music Production",
                "Creative Writing",
            ],
            # Add other categories and subcategories here
        }
        with transaction.atomic():
            for category_name, subcategories in categories_with_subcategories.items():
                category, created = Category.objects.get_or_create(name=category_name)
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f"Category '{category_name}' created.")
                    )
                else:
                    self.stdout.write(f"Category '{category_name}' already exists.")

                for subcategory_name in subcategories:
                    subcategory, sub_created = SubCategory.objects.get_or_create(
                        category=category, name=subcategory_name
                    )
                    if sub_created:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"  SubCategory '{subcategory_name}' created."
                            ),
                        )
                    else:
                        self.stdout.write(
                            f"  SubCategory '{subcategory_name}' already exists."
                        )

            self.stdout.write(
                self.style.SUCCESS("Categories and SubCategories populated successfully.")
            )
