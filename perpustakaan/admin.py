from django.contrib import admin
from .models import Buku, Peminjaman

admin.site.register(Buku)
admin.site.register(Peminjaman)

class PeminjamanAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'buku', 'status', 'tanggal_pinjam') # Kolom yang muncul
    list_filter = ('status', 'tanggal_pinjam') # Fitur filter di samping kanan
    search_fields = ('user__username', 'buku__judul') # Fitur pencarian