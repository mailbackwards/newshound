# Newshound

A sample app that demonstrates some simple, sustainable Django admin features
and packages around custom views and actions.

Created for [DjangoCon 2017](https://2017.djangocon.us/talks/saved-you-a-click-or-three-supercharging-the-django-admin-with-actions-and-views/). Slides can be found [here](https://docs.google.com/presentation/d/1lVgL3SEQUTUcSFs4sD6-nGFbFn15FOK310D6m7F_WuY/edit)

### Run

- put a `SECRET_KEY` in your env
- `pip install -r requirements.txt`
- `python manage.py migrate`
- `python manage.py runserver 0:5000`
- navigate to localhost:5000/admin/

### Packages

- [django-object-actions](https://github.com/crccheck/django-object-actions)
- [django-inline-actions](https://github.com/escaped/django-inline-actions/)
- [django-admin-row-actions](https://github.com/DjangoAdminHackers/django-admin-row-actions)
- [django-nested-admin](https://github.com/theatlantic/django-nested-admin)

See also `admin_site.py` and `admin_mixins.py` for some other customizations.

### Schema

Contains articles, as well as a database of dog breeds and their breed types.
The breeds/groups data is real! The dogs are not. A schema:

![Newshound schema](newshound/static/newshound-schema.png)

### Important!

#### Data sources:

- Breeds: [http://www.akc.org/dog-breeds/](http://www.akc.org/dog-breeds/)
- Sample dog names: [https://data.world/anchorage/dog-names/workspace/file?filename=dog-names_1.csv](https://data.world/anchorage/dog-names/workspace/file?filename=dog-names_1.csv)

For dogs, by dogs, about dogs.

![A cute dog](https://i.ytimg.com/vi/opKg3fyqWt4/hqdefault.jpg)
