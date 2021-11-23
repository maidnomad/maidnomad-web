from django.contrib import admin

# エクスポートしようとして間違って全部消してしまったら悲しいので
# 基本的に全て削除するボタンを非表示にすることにした
admin.site.disable_action("delete_selected")
