from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.urlresolvers import reverse
from .models import Menu, Item, Ingredient
from .forms import MenuForm


class ModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='DavidGilmour',
            password='SeeEmilyPlay'
        )

        self.salt = Ingredient.objects.create(name='salt')
        self.cp = Ingredient.objects.create(name='chickpeas')
        self.th = Ingredient.objects.create(name='tahini')
        self.lj = Ingredient.objects.create(name='lemon juice')
        self.parsley = Ingredient.objects.create(name='parsley')
        self.tomato = Ingredient.objects.create(name='tomato')

    def test_item_creation(self):

        hummus_ingredients = Ingredient.objects.all()
        self.assertIn(self.salt, hummus_ingredients)
        self.assertIn(self.cp, hummus_ingredients)
        self.assertIn(self.th, hummus_ingredients)
        self.assertIn(self.lj, hummus_ingredients)
        self.assertEqual(6, Ingredient.objects.count())

    def test_menu_creation(self):

        hummus = Item.objects.create(
            name='Hummus',
            description='Tasty chickpea dip from the Middle East',
            chef=self.user
        )

        hummus.ingredients.add(self.salt, self.cp, self.th, self.lj)
        hummus.save()

        tabbouleh = Item.objects.create(
            name="Tabbouleh",
            description="Delicious citrusy salad",
            chef=self.user
        )

        tabbouleh.ingredients.add(self.parsley, self.tomato)
        tabbouleh.save()

        self.new_menu = Menu.objects.create(season='spring')
        self.new_menu.items.add(hummus, tabbouleh)
        self.new_menu.save()

        self.assertEqual(1, Menu.objects.count())
        self.assertEqual(2, self.new_menu.items.count())


class ViewTests(TestCase):

    def setUp(self):

        # A test user

        self.user = User.objects.create_user(
            username='DavidGilmour',
            password='SeeEmilyPlay')

        # A test falafel

        self.falafel = Item.objects.create(
            name='falafel',
            description='tasty vegan staple',
            chef=self.user
        )

        # Two test menus

        self.my_menu = Menu.objects.create(season='spring')
        self.my_other_menu = Menu.objects.create(season='summer')

    def test_menu_list(self):
        resp = self.client.get(reverse('menu_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/all_menus.html')
        self.assertContains(resp, 'spring')
        self.assertContains(resp, 'summer')

    def test_view_menu_detail(self):
        resp = self.client.get(reverse(
            'menu_detail',
            kwargs={'pk': self.my_menu.id}
        ))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/menu_detail.html')
        self.assertContains(resp, 'spring')

    def test_view_item_detail(self):
        resp = self.client.get(reverse(
            'item_detail',
            kwargs={'pk': self.falafel.pk}
        ))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/item_detail.html')
        self.assertContains(resp, 'falafel')

    def test_view_edit_menu(self):
        resp = self.client.get(
            reverse('menu_edit', kwargs={'pk': self.my_menu.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/edit_menu.html')
        self.assertContains(resp, 'spring')

    def test_view_new_menu(self):
        resp = self.client.get(reverse('menu_new'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/new_menu.html')

    def test_create_new_menu_invalid(self):
        resp = self.client.post(reverse('menu_new'),
                                {'created_date': timezone.now(),
                                 'season': '',
                                 'items': '',
                                 'expiration_date': 'two years'})
        self.assertEqual(200, resp.status_code)
        self.assertFormError(resp, 'form', 'season',
                             ['This field is required.'])
        self.assertFormError(resp, 'form', 'items',
                             ['"" is not a valid value for a primary key.'])
        self.assertFormError(resp, 'form', 'expiration_date',
                             ['Enter a valid date.'])


class FormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='DavidGilmour',
            password='SeeEmilyPlay'
        )

        self.falafel = Item.objects.create(
            name='falafel',
            description='tasty vegan staple',
            chef=self.user
        )

        self.hummus = Item.objects.create(
            name='hummus',
            description='chickpea goodness',
            chef=self.user
        )

    def test_menuform_valid(self):
        form = MenuForm(data={
            'season': 'Spring 2018',
            'created_date': timezone.now(),
            'items': ['1', '2']
        })
        self.assertTrue(form.is_valid())
