from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Post, Category, Comments


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('id','title','category', 'author', 'is_published', 'get_photo')
    search_fields = ('title', 'content')
    list_filter = ('is_published', 'category')
    save_on_top = True
    # Кастомизация формы заполнение админки через fields
    fields = ('title', 'content', 'photo', 'get_photo', 'category', 'author', 'is_published', 'create_date','update_date')
    readonly_fields = ('get_photo', 'create_date','update_date', )



    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        else:
            return '-'
    get_photo.short_description = 'Миниатюра'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','title')
    search_fields = ('title',)

class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'post_connected')
    search_fields = ('content',)


admin.site.register(Post,PostAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Comments,CommentsAdmin)
