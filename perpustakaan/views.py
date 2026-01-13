from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from .models import Buku, Peminjaman, Favorit
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test # Tambahan untuk pengamanan admin
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from datetime import datetime
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.http import HttpResponse, HttpResponseRedirect

#--- Fitur Processing Form Data Peminjaman Buku ---
@login_required(login_url='login')
def cetak_bukti(request, id):
    # Ambil data peminjaman spesifik
    pinjaman = get_object_or_404(Peminjaman, id=id, user=request.user)
    
    context = {
        'pinjaman': pinjaman,
        'tanggal_cetak': datetime.now(),
    }
    return render(request, 'cetak_bukti.html', context)

def cetak_pdf_peminjaman(request, id):
    pinjaman = get_object_or_404(Peminjaman, id=id, user=request.user)
    
    template = get_template('cetak_bukti_pdf.html') # Kita buat template khusus PDF
    context = {
        'pinjaman': pinjaman,
        'tanggal_cetak': datetime.now(),
    }
    
    html = template.render(context)
    result = BytesIO()
    
    # Proses konversi HTML ke PDF
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse("Wah, ada error saat buat PDF nih.", status=400)


def admin_only(user):
    return user.is_superuser

# --- VIEW UTAMA ---

def index(request):
    return render(request, 'index.html')

# 1. Halaman Home
def home(request):
    # Mengambil 3 buku terbaru sebagai rekomendasi di halaman depan
    buku_rekomendasi = Buku.objects.all().order_by('-id')[:3]
    context = {
        'buku_rekomendasi': buku_rekomendasi,
    }
    return render(request, 'home.html', context)

# 2. Halaman Dashboard Admin
@user_passes_test(admin_only, login_url='home')
def admin_dashboard(request):
    context = {
        'total_buku': Buku.objects.count(),
        'total_user': User.objects.count(),
        'total_dipinjam': Peminjaman.objects.filter(status='Dipinjam').count(),
    }
    return render(request, 'admin_dashboard.html', context)

# 3. Halaman About
def about(request):
    return render(request, 'about.html')

# 4. Halaman Rekomendasi
def rekomendasi(request):
    # Mengambil semua buku atau bisa kamu filter berdasarkan kriteria tertentu
    daftar_rekomendasi = Buku.objects.all().order_by('?')[:6] # Mengambil 6 buku secara acak
    return render(request, 'rekomendasi.html', {'daftar_rekomendasi': daftar_rekomendasi})

@login_required(login_url='login')
def tambah_favorit(request, id):
    buku = get_object_or_404(Buku, id=id)
    favorit, created = Favorit.objects.get_or_create(user=request.user, buku=buku)
    
    if created:
        link_profil = f'<a href="/profile/" class="alert-link ms-2">Cek Favoritku <i class="bi bi-arrow-right"></i></a>'
        pesan = mark_safe(f"Buku <strong>{buku.judul}</strong> berhasil disukai! {link_profil}")
        messages.success(request, pesan)
    else:
        favorit.delete()
        messages.info(request, f"Buku {buku.judul} dihapus dari favorit.")
    
    return redirect(request.META.get('HTTP_REFERER', 'gallery'))

# 5. Halaman Gallery & Search
def gallery(request):
    query = request.GET.get('q')
    if query:
        daftar_buku = Buku.objects.filter(judul__icontains=query) | Buku.objects.filter(penulis__icontains=query)
    else:
        daftar_buku = Buku.objects.all()

    context = {
        'daftar_buku': daftar_buku,
        'query': query,
    }
    return render(request, 'gallery.html', context)

# 6. Detail Buku
def detail_buku(request, id):
    buku = get_object_or_404(Buku, id=id)
    return render(request, 'detail_buku.html', {'buku': buku})

# 7. Login
def login_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, f"Selamat datang, {u}!")
            return redirect('home')
        else:
            messages.error(request, "Username atau Password salah!")
    return render(request, 'login.html')

# 8. Logout
def logout_view(request):
    auth_logout(request)
    messages.info(request, "Kamu telah keluar.")
    return redirect('home')

# 9. Register
def register_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        pc = request.POST.get('password_confirm')

        if p != pc:
            messages.error(request, "Konfirmasi password tidak cocok!")
        elif len(p) < 8:
            messages.error(request, "Password minimal 8 karakter ya!")
        elif User.objects.filter(username=u).exists():
            messages.error(request, "Username sudah ada yang punya.")
        else:
            User.objects.create_user(username=u, password=p)
            messages.success(request, f"Akun {u} berhasil dibuat! Silakan login.")
            return redirect('login')
    return render(request, 'register.html')

# 10. Profil User

@login_required(login_url='login')
def profile_view(request):
    # Ambil data peminjaman KHUSUS untuk user yang sedang login
    buku_saya = Peminjaman.objects.filter(user=request.user).order_by('-tanggal_pinjam')
    
    # Ambil data FAVORIT KHUSUS untuk user yang sedang login
    favorit_saya = Favorit.objects.filter(user=request.user)
    
    context = {
        'buku_saya': buku_saya,
        'favorit_saya': favorit_saya,
    }
    
    return render(request, 'profile.html', context)

# 11. Manajemen Dashboard Admin

@user_passes_test(admin_only, login_url='home')
def kelola_buku(request):
    semua_buku = Buku.objects.all()
    return render(request, 'kelola_buku.html', {'semua_buku': semua_buku})

@user_passes_test(admin_only, login_url='home')
def kelola_member(request):
    # Mengambil semua user kecuali akun admin itu sendiri agar tidak terhapus tidak sengaja
    daftar_user = User.objects.all().order_by('-date_joined')
    return render(request, 'kelola_member.html', {'daftar_user': daftar_user})

@user_passes_test(lambda u: u.is_superuser) # Hanya admin yang bisa akses
def rekap_admin_pdf(request):
    # Ambil semua data peminjaman
    semua_pinjaman = Peminjaman.objects.all().order_by('-tanggal_pinjam')
    
    template = get_template('rekap_admin_pdf.html')
    context = {
        'semua_pinjaman': semua_pinjaman,
        'tanggal_cetak': datetime.now(),
        'admin_name': request.user.username,
    }
    
    html = template.render(context)
    result = BytesIO()
    
    # Proses konversi ke PDF
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse("Terjadi kesalahan saat membuat laporan PDF.", status=400)

# 12. Logika Peminjaman
def tambah_peminjaman(request):
    if not request.user.is_authenticated:
        messages.error(request, "Silakan login terlebih dahulu!")
        return redirect('login')

    if request.method == "POST":
        user_id = request.POST.get('user')
        buku_id = request.POST.get('buku')
        peminjam = User.objects.get(id=user_id)
        buku_dipinjam = Buku.objects.get(id=buku_id)
        
        # --- LOGIKA STOK MULAI DISINI ---
        if buku_dipinjam.stok > 0:
            # 1. Kurangi stok buku
            buku_dipinjam.stok -= 1
            buku_dipinjam.save()

            # 2. Buat data peminjaman
            Peminjaman.objects.create(user=peminjam, buku=buku_dipinjam, status='Dipinjam')
            messages.success(request, f"Berhasil meminjam buku {buku_dipinjam.judul}.")
        else:
            # Jika stok habis
            messages.error(request, f"Maaf, stok buku '{buku_dipinjam.judul}' sedang habis!")
            return redirect('tambah_peminjaman') 
        # --- LOGIKA STOK SELESAI ---
        
        return redirect('daftar_peminjaman') if request.user.is_superuser else redirect('profile_view')

    users = User.objects.all()
    # Filter agar hanya buku yang stoknya > 0 yang muncul di pilihan (opsional tapi bagus)
    books = Buku.objects.filter(stok__gt=0) 
    return render(request, 'tambah_peminjaman.html', {'users': users, 'books': books})

def daftar_peminjaman(request):
    data_pinjam = Peminjaman.objects.all().order_by('-tanggal_pinjam')
    return render(request, 'daftar_peminjaman.html', {'data_pinjam': data_pinjam})

def kembalikan_buku(request, pk):
    # 1. Ambil data peminjaman tanpa filter user (agar Admin bisa proses semua)
    pinjaman = get_object_or_404(Peminjaman, pk=pk)
    
    # 2. Ambil objek buku
    buku = pinjaman.buku
    
    # 3. Tambah stok kembali
    buku.stok += 1
    buku.save()

    # 4. Update status dan catat waktu kembali (biar lengkap)
    pinjaman.status = 'Dikembalikan'
    pinjaman.tanggal_kembali = timezone.now() # Pastikan ada field ini di model
    pinjaman.save()
    
    messages.success(request, f"Buku '{pinjaman.buku.judul}' milik {pinjaman.user.username} berhasil dikembalikan!")
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))