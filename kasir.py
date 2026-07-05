import os
import json

class System:
  data = {
    
  }
  barang = {
    
  }
  def __init__(self):
    # opsi pilihan
    self.opsi={
      1: self.login,
      2: self.daftar,
    }
    self.rapi=5*"====="
  def question_teks(self,teks):
    return input(teks)
  def question_angka(self,teks):
    while True:
      try:
        return int(input(teks))
      except ValueError:
        print('[System]: Only Angka !!!')
  def template_teks(self,judul,isi):
    print(f'{self.rapi:^26}')
    print(f'{judul:^26}')
    print(f'{self.rapi:^26}\n')
    print(isi)
  def loads(self):
    # Ambil data dari database
    try:
      with open('data.json','r') as file:
        return json.load(file)
    except FileNotFoundError:
      with open('data.json','w') as file:
        json.dump({},file)
        return {}
    except json.JSONDecodeError:
      print("[SYSTEM]: data.json rusak, database diinisialisasi ulang.\n")
      with open("data.json", "w") as file:
        json.dump({}, file, indent=4)
        return {}
  def save(self):
    # Simpan data ke database
    with open('data.json','w') as file:
      json.dump(self.data,file,indent=4)
  def login(self):
    print('\n')
    # Load data dari database
    self.data = self.loads()
    # Batas percobaan Login
    MAX_LOGIN= 3
    kesalahan_user= 0
    # ==================
    while True:
      if kesalahan_user < MAX_LOGIN:
        self.template_teks('LOGIN 🔐','MASUKKAN USERNAME ANDA')
        # Input User
        cek_user=self.question_teks(': ').lower().strip()
        # Cek user dalam data
        if cek_user in self.data:
          # User ditemukan & Cek status akun
          if self.data[cek_user]['status'] == 'banned':
            # Akun terbanned  
            print(f'{5*"======="}')
            print(f'AKUN ANDA TERBLOKIR')
            return
          # Akun Aman
          # Batas percobaan Login
          kesalahan_user=0
          kesalahan_password=0
          # ================°°°°°°
          while True:
            if kesalahan_password< MAX_LOGIN:
              # input pw
              cek_password=self.question_teks('MASUKKAN PASSWORD ANDA\n: ').strip()
              # Cek pw dalam Data
              if cek_password == self.data[cek_user]['password']:
                # Pw Benar
                cek_password=0
                print('\n')
                print('password benar')
                return
              else:
                # Pw salah
                # Add salah pw
                kesalahan_password+=1
                sisa = 3 - kesalahan_password
                # Sisa percobaan
                print(f'PASSWORD ANDA SALAH\nSISA KESEMPATAN: {sisa}')
                print('SILAHKAN MASUKKAN ULANG PASSWORD ANDA\n')
                continue
            # Limit Cek password Tercapai 
            print(f'{5*"====="}')
            print(f'AKUN ANDA TERBLOKIR')
            self.data[cek_user]['status']= 'banned'
            # Simpan Data akun yg terbanned
            self.save()
            kesalahan_password=0
            return
        else:
          # username tidak ditemukan
          print('USERNAME ANDA TIDAK DITEMUKAN\nSILAHKAN MASUKKAN ULANG USERNAME\n')
          # add salah user
          kesalahan_user+=1
          continue
      # Limit Cek username Tercapai 
      print(5*'=======')
      print(f'SILAHKAN BUAT AKUN ANDA TERLEBIH DAHULU')
      kesalahan_user=0
      return
  def daftar(self):
    print('\n')
    #Load data
    self.data=self.loads()
    while True:
      self.template_teks('DAFTAR 📝','BUAT USERNAME ANDA')
      # Buat username
      create_username=self.question_teks(': ').lower().strip()
      # Cek user dipakai pengguna lain apa tidak
      if create_username in self.data:
        # User Sudah dipakai
        print('USERNAME TELAH DIGUNAKAN\nSILAHKAN GUNAKAN USERNAME LAIN.\n')
        continue
      elif not create_username:
        print('USERNAME TIDAK BOLEH KOSONG\n')
        continue
      # User belum dipakai & Buat pw
      while True:
        create_password=self.question_teks("MASUKKAN PASSWORD BARU ANDA\n: ").strip()
        if not create_password:
          print('PASSWORD TIDAK BOLEH KOSONG\n')
          continue
        print(f'{self.rapi:^26}')
        self.data[create_username]= {
          'uang': 0,
          'status': 'aman',
          'password': create_password,
        }
        # Simpan akun ke database
        self.save()
        print('CREATED AKUN SUKSES ✓')
        return
        
class Run(System):
  def apk(self):
    while True:
      # Menu Awal
      self.template_teks("SELAMAT DATANG","1. LOGIN\n2. DAFTAR\n3. EXIT\n")
      # Input pilihan 
      pilih=self.question_angka("PILIH: ")
      # Cek pilihan user
      if pilih in self.opsi:
        self.opsi[pilih]()
        print('\n')
      # Exit
      elif pilih == 3:
        print('\n')
        print('EXIT ⌛︎')
        break
      else:
        print("[SYSTEM]: MENU TIDAK TERSEDIA")

os.system("cls" if os.name == "nt" else "clear")
run=Run()
run.apk()