from django.contrib import admin

from .models import Post, Dog, Breed, BreedGroup, DogBreedRelationship


class DogBreedInline(admin.TabularInline):
    model = DogBreedRelationship


class DogInline(admin.TabularInline):
    model = Post.dogs_mentioned.through


class PostAdmin(admin.ModelAdmin):
    model = Post
    inlines = [DogInline]


class DogAdmin(admin.ModelAdmin):
    model = Dog
    inlines = [DogBreedInline]


class BreedAdmin(admin.ModelAdmin):
    model = Breed


class BreedGroupAdmin(admin.ModelAdmin):
    model = BreedGroup


admin.site.register(Post, PostAdmin)
admin.site.register(Dog, DogAdmin)
admin.site.register(Breed, BreedAdmin)
admin.site.register(BreedGroup, BreedGroupAdmin)
