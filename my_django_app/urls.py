"""
URL configuration for my_django_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from perpustakaan import views

urlpatterns = [
    # Admin Panel Django
    path('admin/', admin.site.urls),
    
    # Halaman Utama
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    
    # Dashboard Khusus Admin
    path('dashboard-admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard-admin/kelola-buku/', views.kelola_buku, name='kelola_buku'),
    path('dashboard-admin/kelola-member/', views.kelola_member, name='kelola_member'),
    path('admin-rekap-pdf/', views.rekap_admin_pdf, name='rekap_admin_pdf'),
    
    # Informasi & Galeri
    path('about/', views.about, name='about'), 
    path('rekomendasi/', views.rekomendasi, name='rekomendasi'),
    path('gallery/', views.gallery, name='gallery'),
    path('buku/<int:id>/', views.detail_buku, name='detail_buku'),
    path('favorit/<int:id>/', views.tambah_favorit, name='tambah_favorit'),
    
    # Autentikasi
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('cetak-bukti/<int:id>/', views.cetak_bukti, name='cetak_bukti'),
    path('cetak-pdf/<int:id>/', views.cetak_pdf_peminjaman, name='cetak_pdf'),
    path('profile/view/', views.profile_view, name='profile_view'),
    
    # Manajemen Peminjaman
    path('peminjaman/', views.daftar_peminjaman, name='daftar_peminjaman'),
    path('peminjaman/tambah/', views.tambah_peminjaman, name='tambah_peminjaman'),
    path('peminjaman/kembali/<int:pk>/', views.kembalikan_buku, name='kembalikan_buku'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
