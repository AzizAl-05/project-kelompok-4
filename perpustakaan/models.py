from django.db import models
from django.contrib.auth.models import User # Import User bawaan Django

# 1. Model Buku
class Buku(models.Model):
    judul = models.CharField(max_length=200)
    penulis = models.CharField(max_length=100)
    deskripsi = models.TextField()
    cover = models.ImageField(upload_to='covers/', null=True, blank=True)
    tanggal_input = models.DateTimeField(auto_now_add=True)
    stok = models.IntegerField(default=1)

    def __str__(self):
        return self.judul

# 2. Model Peminjaman
class Peminjaman(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    buku = models.ForeignKey(Buku, on_delete=models.CASCADE)
    tanggal_pinjam = models.DateTimeField(auto_now_add=True)
    tanggal_kembali = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default='Dipinjam') # Dipinjam / Dikembalikan

    def __str__(self):
        return f"{self.user.username} meminjam {self.buku.judul}"

# 3. Model Favorit    
class Favorit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    buku = models.ForeignKey(Buku, on_delete=models.CASCADE)
    tanggal_ditambah = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'buku') # Agar satu user tidak bisa menyukai buku yang sama dua kali