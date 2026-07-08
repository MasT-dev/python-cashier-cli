import os
import json


class System:
    def __init__(self):
        self.rapi = 5 * "====="
    def question_teks(self, teks):
        return input(teks)
    def question_angka(self, teks):
        while True:
            try:
                return int(input(teks))
            except ValueError:
                print("[System]: Only Angka !!!")
    def template_teks(self, judul, isi):
        print(f"{self.rapi:^26}")
        print(f"{judul:^26}")
        print(f"{self.rapi:^26}\n")
        print(isi)

class Database:
    def __init__(self, nama_file="data.json"):
        self.nama_file = nama_file
    def loads(self):
        # Ambil data dari database
        try:
            with open(self.nama_file, "r") as file:
                return json.load(file)

        except FileNotFoundError:
            with open(self.nama_file, "w") as file:
                json.dump({}, file)
                return {}

        except json.JSONDecodeError:
            print("[SYSTEM]: data.json rusak, database diinisialisasi ulang.\n")

            with open(self.nama_file, "w") as file:
                json.dump({}, file, indent=4)
                return {}
    def save(self, data):
        # Simpan data ke database
        with open(self.nama_file, "w") as file:
            json.dump(data, file, indent=4)

class Login:
    def __init__(self, system, database):
        self.system = system
        self.database = database
        self.MAX_LOGIN = 3
    def login(self):
        print("\n")

        # Load data dari database
        data = self.database.loads()

        # Batas percobaan login username
        kesalahan_user = 0

        while True:
            if kesalahan_user < self.MAX_LOGIN:
                self.system.template_teks("LOGIN 🔐", "MASUKKAN USERNAME ANDA")

                # Input user
                cek_user = self.system.question_teks(": ").lower().strip()

                # Cek user dalam data
                if cek_user in data:

                    # User ditemukan & cek status akun
                    if data[cek_user]["status"] == "banned":
                        print(f"{5 * '======='}")
                        print("AKUN ANDA TERBLOKIR")
                        return

                    # Akun aman
                    kesalahan_user = 0
                    kesalahan_password = 0

                    while True:
                        if kesalahan_password < self.MAX_LOGIN:

                            # Input password
                            cek_password = self.system.question_teks(
                                "MASUKKAN PASSWORD ANDA\n: "
                            ).strip()

                            # Cek password dalam data
                            if cek_password == data[cek_user]["password"]:
                                print("\n")
                                print("password benar")
                                return

                            else:
                                # Password salah
                                kesalahan_password += 1
                                sisa = self.MAX_LOGIN - kesalahan_password

                                print(
                                    f"PASSWORD ANDA SALAH\n"
                                    f"SISA KESEMPATAN: {sisa}"
                                )
                                print("SILAHKAN MASUKKAN ULANG PASSWORD ANDA\n")
                                continue

                        # Limit cek password tercapai
                        print(f"{5 * '====='}")
                        print("AKUN ANDA TERBLOKIR")

                        data[cek_user]["status"] = "banned"

                        # Simpan data akun yang terbanned
                        self.database.save(data)

                        return

                else:
                    # Username tidak ditemukan
                    print(
                        "USERNAME ANDA TIDAK DITEMUKAN\n"
                        "SILAHKAN MASUKKAN ULANG USERNAME\n"
                    )

                    kesalahan_user += 1
                    continue

            # Limit cek username tercapai
            print(5 * "=======")
            print("SILAHKAN BUAT AKUN ANDA TERLEBIH DAHULU")

            return

class Daftar:
    def __init__(self, system, database):
        self.system = system
        self.database = database
    def daftar(self):
        print("\n")

        # Load data
        data = self.database.loads()

        while True:
            self.system.template_teks("DAFTAR 📝", "BUAT USERNAME ANDA")

            # Buat username
            create_username = self.system.question_teks(": ").lower().strip()

            # Cek user dipakai pengguna lain atau tidak
            if create_username in data:
                print(
                    "USERNAME TELAH DIGUNAKAN\n"
                    "SILAHKAN GUNAKAN USERNAME LAIN.\n"
                )
                continue
            # Cek username kosong
            elif not create_username:
                print("USERNAME TIDAK BOLEH KOSONG\n")
                continue

            # User belum dipakai & buat password
            while True:
                create_password = self.system.question_teks(
                    "MASUKKAN PASSWORD BARU ANDA\n: "
                ).strip()

                cek_simbol = create_password.isalnum()
                cek_angka = create_password.isdecimal()
                cek_huruf = create_password.isalpha()
                cek = cek_angka or cek_huruf

                # Cek password kosong atau tidak
                if not create_password:
                    print(
                        25 * "="
                        + "\n"
                        + "PASSWORD TIDAK BOLEH KOSONG\n"
                        + 25 * "="
                        + "\n"
                    )
                    continue

                # Cek password ada simbol atau tidak
                elif cek_simbol == False:
                    print(
                        25 * "="
                        + "\n"
                        + "TIDAK BOLEH ADA SIMBOL !!!\n"
                        + 25 * "="
                        + "\n"
                    )
                    continue

                # Cek password menyertakan alfabet dan angka atau tidak
                if cek == True:
                    print(
                        25 * "="
                        + "\n"
                        + "PEMBUATAN PASSWORD HARUS MENYERTAKAN\n"
                        + "ALFABET DAN ANGKA !!!\n"
                        + 25 * "="
                        + "\n"
                    )
                    continue

                # Pembuatan akun
                print(f"{self.system.rapi:^26}")

                data[create_username] = {
                    "uang": 0,
                    "status": "aman",
                    "password": create_password,
                }

                # Simpan akun ke database
                self.database.save(data)

                print("CREATED AKUN SUKSES ✓")
                return

class Run:
    def __init__(self):
        self.system = System()
        self.database = Database()

        self.login_fitur = Login(self.system, self.database)
        self.daftar_fitur = Daftar(self.system, self.database)

        # Opsi pilihan
        self.opsi = {
            1: self.login_fitur.login,
            2: self.daftar_fitur.daftar,
        }
    def apk(self):
        while True:
            # Menu awal
            self.system.template_teks(
                "SELAMAT DATANG",
                "1. LOGIN\n2. DAFTAR\n3. EXIT\n"
            )

            # Input pilihan
            pilih = self.system.question_angka("PILIH: ")

            # Cek pilihan user
            if pilih in self.opsi:
                self.opsi[pilih]()
                print("\n")

            # Exit
            elif pilih == 3:
                print("\n")
                print("EXIT ⌛︎")
                break

            else:
                print("[SYSTEM]: MENU TIDAK TERSEDIA")

os.system("cls" if os.name == "nt" else "clear")
run = Run()
run.apk()
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
