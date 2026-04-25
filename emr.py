import pdfplumber  
import pyautogui
import pyperclip
import re  
import time 
import tkinter as tk    
from datetime import datetime, timedelta
from tkinter import messagebox, ttk
 
def checkPassword():
    password_set = "asdasd"
    if password_entry.get() == password_set: 
        root.destroy() 
        main()
    else:
        messagebox.showinfo('?', 'invalid passcode')

def main():  
 
    def scan(opt):     
        if opt == 'i': 
            pdf_path = "C:/download/print_asperawat_gd.pdf" 
        else:
            pdf_path = "C:/download/print_transfer.pdf"  

        # scan identitas berbasis teks 
        try:
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for page in pdf.pages: 
                    text += page.extract_text() + "\n"
 
                if opt == 'i': 
                    pindahan_entry.delete(0, tk.END) 
                    pindahan_entry.insert(0, 'IGD')  
    
                mr = re.search(r'\s(\d{8})\s' , text)
                if mr: 
                    mr_entry.delete(0, tk.END) 
                    mr_entry.insert(0, mr.group(1)) 
                 
                tn = re.search(r'\btn\.?\s+([^\s(]+(?:\s+[^\s(]+)*)' , text, re.IGNORECASE)
                if tn: 
                    nama_entry.delete(0, tk.END) 
                    nama_entry.insert(0, tn.group(1).strip())  
 
                ny = re.search(r'\bny\.?\s+([^\s(]+(?:\s+[^\s(]+)*)', text, re.IGNORECASE)
                if ny: 
                    nama_entry.delete(0, tk.END) 
                    nama_entry.insert(0, ny.group(1).strip()) 
  
                sdr = re.search(r'\bsdr\.?\s+([^\s(]+(?:\s+[^\s(]+)*)', text, re.IGNORECASE)
                if sdr: 
                    nama_entry.delete(0, tk.END) 
                    nama_entry.insert(0, sdr.group(1).strip()) 
 
                sdri = re.search(r'\bsdri\.?\s+([^\s(]+(?:\s+[^\s(]+)*)', text, re.IGNORECASE)
                if sdri: 
                    nama_entry.delete(0, tk.END) 
                    nama_entry.insert(0, sdri.group(1).strip()) 
         
                age = re.search(r"\((\d+)\s+th", text) 
                if age:  
                    usia_entry.delete(0, tk.END) 
                    usia_entry.insert(0, age.group(1) )  
        
        except Exception as e: 
            messagebox.showinfo('?', e)

        # scan based on [table]
        try:
            with pdfplumber.open(pdf_path) as pdf:
                text = ''

                # Iterasi setiap halaman
                for halaman in pdf.pages:
                    tables = halaman.extract_tables()
                    if tables: 
                        for t in tables:
                            for baris in t:
                                # remove [None] and empty string, gabungkan dengan spasi
                                bersih_baris = [str(elemen) for elemen in baris if elemen not in [None, ""]]
                                text += " ".join(bersih_baris) + "\n" 
                        text += "\n"
 
                # print(text)

                if opt == 'i' : 
                    
                    keluhan = re.search(r"Keluhan Utama\s*(.*?)\s*Riwayat Penyakit", text, re.DOTALL)
                    if keluhan:  
                        keluhan_entry.delete(0, tk.END) 
                        keluhan_entry.insert(0, ' '.join(keluhan.group(1).split())) 
                         
                    rps = re.search(r"dahulu dan keluarga \)\s*(.*?)\s*Riwayat Pengobatan", text, re.DOTALL) 
                    if rps:   
                        rps_entry.delete(0, tk.END) 
                        rps_entry.insert(0, ' '.join(rps.group(1).split())) 
                    else:
                        # jika RPS tidak terdeteksi, isi dengan keluhan utama
                        rps_entry.insert(0, ' '.join(keluhan.group(1).split())) 
 
                    rpd = re.search(r"konsumsi obat saat ini \)\s*(.*?)\s*Riwayat Kelahiran", text, re.DOTALL)
                    rpd_entry.delete(0, tk.END) 
                    if rpd:    
                        rpd_entry.insert(0, ' '.join(rpd.group(1).split())) 
                    else: 
                        rpd_entry.insert(0, '-') 
 
                    diagnosa = re.search(r"DIAGNOSIS SESUAI ICD-10\s*(.*?)\s*Permasalahan Medis", text, re.DOTALL)
                    if diagnosa:   
                        remove_numbering = re.sub(r"\d+\s*\.\s*", "", diagnosa.group(1))  
                        diagnosa_entry.delete(0, tk.END) 
                        diagnosa_entry.insert(0, ' + '.join(remove_numbering.split('\n')))  
             
                    sistole = re.search(r"Sistole\s*:\s*(.*?)\s*mmHg", text, re.IGNORECASE) 
                    if sistole:   
                        sistole_entry.delete(0, tk.END) 
                        sistole_entry.insert(0, sistole.group(1)) 
             
                    diastole = re.search(r"Diastole\s*:\s*(.*?)\s*mmHg", text, re.IGNORECASE) 
                    if diastole:   
                        diastole_entry.delete(0, tk.END) 
                        diastole_entry.insert(0, diastole.group(1)) 
  
                    nadi = re.search(r"nadi\s*(.*?)\s*x/menit", text, re.IGNORECASE)
                    if nadi: 
                        nadi_entry.delete(0, tk.END) 
                        nadi_entry.insert(0, nadi.group(1)) 
 
                    suhu = re.search(r"(?i)suhu\s+(\S+)", text, re.IGNORECASE)
                    if suhu: 
                        comaToPeriod = suhu.group(1).strip().replace(',', '.')
                        suhu_entry.delete(0, tk.END) 
                        suhu_entry.insert(0, comaToPeriod) 
 
                    rr_match = re.search(r"(?i)rr\s+(\d+)\s+x/menit", text, re.IGNORECASE)
                    if rr_match: 
                        rr_entry.delete(0, tk.END) 
                        rr_entry.insert(0, rr_match.group(1).strip()) 
             
                    spo2 = re.search(r"(?i)\bspo2\b\s*(\d+)%", text, re.IGNORECASE)
                    if spo2: 
                        spo2_entry.delete(0, tk.END) 
                        spo2_entry.insert(0, spo2.group(1).strip())  
             
                    alergi = re.search(r'Alergi\s+([^\n]+)', text, re.IGNORECASE)  
                    if alergi: 
                        if alergi.group(1).strip().lower() != "tidak": 
                            alergi_removeYa = alergi.group(1).replace('Ya : ', '')
                            alergi_entry.delete(0, tk.END) 
                            alergi_entry.insert(0, alergi_removeYa.strip()) 
                        else:
                            alergi_entry.delete(0, tk.END) 
                            alergi_entry.insert(0, '-') # isi dengan [-] jika tidak ada alergi, agar placeholder tidak muncul sebagai string
                               
                    dr = re.findall(r"dr\.\s+([\w\s]+?)\s+Sp\.", text, re.IGNORECASE | re.DOTALL)  
                    dr_unique = set(match.strip().replace("\n", " ") for match in dr)  
                    if dr: 
                        dr_EN.delete("1.0", tk.END)    
                        for doctor in dr_unique:
                            dr_EN.insert(tk.END, doctor + "\n")
  
                    # khusus untuk menemukan nama dr. aji
                    aji = re.search(r"\s*Satriyo\s*Aji\s*", text, re.IGNORECASE | re.DOTALL)  
                    if aji:   
                        dr_EN.insert(tk.END, aji.group().strip().replace("\n", " "))
                    
                    tx = re.search(r"PLAN OF\s*CARE\s*\)\s*(.*?)\s*Konsultasi Dokter", text, re.DOTALL) 
                    if tx:
                        # beri bulleting
                        tx_bulleting = "\n".join(f"- {baris}" for baris in tx.group(1).strip().split("\n")) 

                        # rapikan buleting yang double (- -) menjadi (-)
                        removeExtraBullet = re.sub(r'^\s*[-\s]+', '- ', tx_bulleting, flags=re.MULTILINE)

                        # Filter baris yang tidak mengandung 'mrs' (ignorecase)
                        removeMRS = [line for line in removeExtraBullet.splitlines() if not re.search(r'mrs', line, re.IGNORECASE)]

                        # Gabungkan kembali menjadi string
                        result = '\n'.join(removeMRS)
 
                        terapi_entry.delete("1.0", tk.END)   
                        terapi_entry.insert(tk.END, result)
  
                    report() 
                    rx()
                
                else: 
                    # new line menyebabkan regex tidak bisa mencari kata tertentu
                    allTextWithoutNewLine = text.replace('\n', '. ')   

                    keluhan_pattern = r"Keluhan Utama(.*?)Riwayat Penyakit"
                    keluhan_match = re.search(keluhan_pattern, allTextWithoutNewLine)
                    if keluhan_match: 
                        keluhan_entry.delete(0, tk.END) 
                        keluhan_entry.insert(0, keluhan_match.group(1).strip()) 
                    
                    rps_entry.delete(0, tk.END) 
                    rps_entry.insert(0, '-') 
                    rpd_entry.delete(0, tk.END) 
                    rpd_entry.insert(0, '-') 

                    diagnosa_pattern = r"Diagnosa(.*?)Alasan Admisi"
                    diagnosa_match = re.search(diagnosa_pattern, allTextWithoutNewLine) 
                    if diagnosa_match:   
                        diagnosa_entry.delete(0, tk.END) 
                        diagnosa_entry.insert(0, diagnosa_match.group(1).strip()) 
        
                    sistole_pattern = r'Sistole\s*:\s*(\d+)\s*mmhg'
                    sistole_match = re.search(sistole_pattern, text, flags=re.IGNORECASE)
                    if sistole_match:   
                        sistole_entry.delete(0, tk.END) 
                        sistole_entry.insert(0, sistole_match.group(1)) 

                    diastole_pattern = r'Diastole\s*:\s*(\d+)\s*mmhg'
                    diastole_match = re.search(diastole_pattern, text, flags=re.IGNORECASE)
                    if diastole_match:    
                        diastole_entry.delete(0, tk.END) 
                        diastole_entry.insert(0, diastole_match.group(1)) 
        
                    nadi_pattern = r"(?i)nadi\s+(\d+)\s+x/menit"
                    nadi_match = re.search(nadi_pattern, text, flags=re.IGNORECASE)
                    if nadi_match: 
                        nadi_entry.delete(0, tk.END) 
                        nadi_entry.insert(0, nadi_match.group(1).strip()) 

                    suhu_pattern = r"Suhu(.*?)GCS"
                    suhu_match = re.search(suhu_pattern, text, flags=re.IGNORECASE)
                    if suhu_match: 
                        comaToPeriod = suhu_match.group(1).strip().replace(',', '.')
                        suhu_entry.delete(0, tk.END) 
                        suhu_entry.insert(0, comaToPeriod) 

                    rr_pattern = r"Pernafasan(.*?)Tensi"
                    rr_match = re.search(rr_pattern, text, flags=re.IGNORECASE)
                    if rr_match: 
                        rr_entry.delete(0, tk.END) 
                        rr_entry.insert(0, rr_match.group(1).strip()) 
        
                    spo2_pattern = r"SPO2(.*?)Suhu"
                    spo2_match = re.search(spo2_pattern, text, flags=re.IGNORECASE)
                    if spo2_match: 
                        spo2_entry.delete(0, tk.END) 
                        spo2_entry.insert(0, spo2_match.group(1).strip())  
        
                    alergi_pattern = r'Alergi\s+([^\n]+)'
                    alergi_match = re.search(alergi_pattern, text, flags=re.IGNORECASE) 

                    if alergi_match : 
                        if alergi_match.group(1).strip().lower() != "tidak": 
                            alergi_removeYa = alergi_match.group(1).replace('Ya, ', '')
                            alergi_removeAlergen = alergi_removeYa.replace('Bahan Alergen :', '')
                            alergi_entry.delete(0, tk.END) 
                            alergi_entry.insert(0, alergi_removeAlergen.strip()) 
                        else:
                            alergi_entry.delete(0, tk.END) 

                    
                    diet_pattern = r"Diet(.*?)Makan"
                    diet_match = re.search(diet_pattern, text)
                    if diet_match: 
                        diet_entry.delete(0, tk.END) 
                        diet_entry.insert(0, diet_match.group(1).strip()) 

                    inf_pattern = r"Infus \(dalam 24 jam\)(.*?)Obat Injeksi"
                    inf_match = re.search(inf_pattern, allTextWithoutNewLine, re.DOTALL)
                    
                    inj_pattern = r"Obat Injeksi(.*?)Obat Oral"
                    inj_match = re.search(inj_pattern, allTextWithoutNewLine, re.DOTALL)
                    
                    po_pattern = r"Obat Oral(.*?)Prosedur Medis"
                    po_match = re.search(po_pattern, allTextWithoutNewLine, re.DOTALL)

                    res = inf_match.group(1) +'\n'+ inj_match.group(1) +'\n'+ po_match.group(1)

                    # ganti koma dengan newline
                    res = res.replace(',', '\n')
                    
                    # Hilangkan baris kosong
                    res = re.sub(r'\n\s*\n', '\n', res) 

                    # Tambahkan bullet (-) pada setiap baris 
                    res = "\n".join(f"- {line}" for line in res.splitlines() if line.strip())
        
                    # reset entry, masukkan hasil 
                    terapi_entry.delete("1.0", tk.END)
                    terapi_entry.insert("1.0", res)
                    
        except Exception as e: 
            messagebox.showinfo('?', e) 

    def ttv():  
        time.sleep(2)   
        pyautogui.write(rr_entry.get())
        pyautogui.press('tab')  
        pyautogui.write(spo2_entry.get())
        pyautogui.press('tab')  
        pyautogui.press('tab')  
        pyautogui.write(suhu_entry.get())
        pyautogui.press('tab')  
        pyautogui.write(sistole_entry.get())
        pyautogui.press('tab')  
        pyautogui.write(diastole_entry.get())
        pyautogui.press('tab')  
        pyautogui.write(nadi_entry.get())
        pyautogui.press('enter') 


    def terima_transfer():   
        time.sleep(2)   
        pyautogui.write(rr_entry.get())
        pyautogui.press('tab')  
        pyautogui.write(sistole_entry.get())
        pyautogui.press('tab')  
        pyautogui.write(diastole_entry.get())
        pyautogui.press('tab')  
        pyautogui.write(nadi_entry.get())
        pyautogui.press('tab')  
        pyautogui.press('tab')  
        pyautogui.write(spo2_entry.get())
        pyautogui.press('tab')   
        pyautogui.write(suhu_entry.get())
        pyautogui.press('tab')  
        pyautogui.write('456')
        pyautogui.press('tab')  
        pyautogui.write('isokor')
        pyautogui.press('tab')  
        pyautogui.write('positif')   
        pyautogui.press('tab')  
        pyautogui.press('tab')  
        pyautogui.press('tab')   
        pyautogui.press('enter')
        messagebox.showinfo("?", "Terima transfer selesai") 
  
    def cppt(opt):  
        time.sleep(2) 
        currentDate = datetime.now().strftime("%Y-%m-%d")
        currentHour = datetime.now().hour 
        cpptTime = ''
        if currentHour > 6 and currentHour < 14:
            cpptTime = currentDate + ' 12:00:00'
            handOverTime = currentDate + ' 14:00:00' 
        elif currentHour > 13 and currentHour < 21:
            cpptTime = currentDate + ' 19:00:00'
            handOverTime = currentDate + ' 21:00:00' 
        else:
            # Shif malam
            if currentHour > 20 and currentHour < 24 :
                # ganti ke tanggal berikutnya jika sebelum jam 24
                today = datetime.today()  
                next_day = today + timedelta(days=1) 
                tomorrow = next_day.strftime("%Y-%m-%d")

                cpptTime = tomorrow + ' 05:00:00'
                handOverTime = tomorrow + ' 07:00:00'  
            else : 
                # jika diatas jam 24, gunakan tanggal yang sama
                cpptTime = currentDate + ' 05:00:00'
                handOverTime = currentDate + ' 07:00:00' 
 
        pyautogui.write(cpptTime)
        pyautogui.press('tab')
        pyautogui.press('tab')
        
        if opt == 'c': 
            # Subyektif

            pyautogui.hotkey('ctrl', 'a')  
            pyautogui.hotkey('ctrl', 'c')  
            s = pyperclip.paste()  
            s_res = re.sub(r'pasien mengatakan\s*', '', s, flags=re.IGNORECASE)   
            pyperclip.copy(s_res)  
            pyautogui.hotkey('ctrl', 'v')   

            pyautogui.press('tab') 
            pyautogui.press('tab') 
            pyautogui.press('tab') 

            # Asesmen
 
            pyautogui.hotkey('ctrl', 'a')  
            pyautogui.hotkey('ctrl', 'c')  
            asesmen = pyperclip.paste()  

            asesmen_new = []
            implementasi = [] # sekalian bikin implementasi lah
            intervensi = [] # sekalian bikin intervensi dari asesmen yang didapat 
 
            if re.search(r'nyeri', asesmen, re.IGNORECASE):
                asesmen_new.append("nyeri akut") 
                implementasi.append('skala nyeri menurun')
                implementasi.append('grimace berkurang')
                intervensi.append("kaji keluhan nyeri") 
 
            if re.search(r'pola napas', asesmen, re.IGNORECASE):
                asesmen_new.append("pola napas tidak efektif")
                implementasi.append('frekuensi napas membaik')  
                implementasi.append('dipsnea menurun')  
                intervensi.append("pantau kepatenan jalan napas")  
                intervensi.append("monitor saturasi secara berkala") 

            if re.search(r'pola nafas', asesmen, re.IGNORECASE):
                asesmen_new.append("pola napas tidak efektif")  
                implementasi.append('frekuensi napas membaik')  
                implementasi.append('dipsnea menurun')   
                intervensi.append("pantau kepatenan jalan napas") 
                intervensi.append("monitor saturasi secara berkala") 

            if re.search(r'bersihan', asesmen, re.IGNORECASE):
                asesmen_new.append("bersihan jalan napas tidak efektif") 
                implementasi.append('produksi sputum menurun')   
                implementasi.append('wheezing/ronchi menurun')   
                intervensi.append("kaji keluhan batuk") 
                intervensi.append("monitor suara nafas") 

            if re.search(r'curah jantung', asesmen, re.IGNORECASE):
                asesmen_new.append("penurunan curah jantung")
                implementasi.append('status hemodinamik membaik')   
                intervensi.append("monitor status hemodinamik") 
            
            if re.search(r'hipertermi', asesmen, re.IGNORECASE):
                asesmen_new.append("hipertermia")
                implementasi.append('suhu tubuh dalam batas normal')   
                intervensi.append("monitor suhu tubuh bila perlu") 

            if re.search(r'hipervolemi', asesmen, re.IGNORECASE):
                asesmen_new.append("hipervolemia")
                implementasi.append('intake dan output seimbang')   
                implementasi.append('edema berkurang')   
                intervensi.append("batasi asupan cairan") 
                intervensi.append("monitor keseimbangan cairan") 

            if re.search(r'nausea', asesmen, re.IGNORECASE):
                asesmen_new.append("nausea")
                implementasi.append('keluhan mual berkurang')   
                intervensi.append("monitor keluhan muntah") 
                intervensi.append("pantau isyarat nonverbal ketidaknyamanan") 

            if re.search(r'adaptif', asesmen, re.IGNORECASE):
                asesmen_new.append("penurunan kapasitas adaptif intrakranial")
                implementasi.append('tingkat kesadaran membaik')   
                implementasi.append('irama napas membaik')   
                intervensi.append("monitor peningkatan tekanan darah") 
                intervensi.append("monitor irreguleritas irama napas") 
                intervensi.append("monitor penurunan tingkat kesadaran") 

            if re.search(r'ketidakstabilan', asesmen, re.IGNORECASE):
                asesmen_new.append("resiko ketidakstabilan kadar gula darah")
                implementasi.append('kadar gula darah dalam batas normal')   
                intervensi.append("pantau kadar gula darah secara berkala") 

            if re.search(r'infeksi', asesmen, re.IGNORECASE):
                asesmen_new.append("resiko infeksi")
                implementasi.append('tidak ada tanda infeksi') 
                intervensi.append("pantau tanda tanda infeksi") 

            if re.search(r'jatuh', asesmen, re.IGNORECASE):
                asesmen_new.append("resiko jatuh")
                implementasi.append('tidak ada kejadian jatuh')  
                intervensi.append("pasang kunci bed dan siderail") 
 
            # Convert asesmen_new to a numbered string with new lines
            asesmen_numbering = '\n'.join(f"{i+1}. {item}" for i, item in enumerate(asesmen_new))  
            pyperclip.copy(asesmen_numbering)  
            pyautogui.hotkey('ctrl', 'v')   
            pyautogui.press('tab') 
            pyautogui.press('tab') 

            # Planning

            pyautogui.hotkey('ctrl', 'a')  
            implementasi.insert(0, 'ttv dalam batas normal') 
            implementasi_numbering = '\n'.join(f"{i+1}. {item}" for i, item in enumerate(implementasi))  
            pyperclip.copy(implementasi_numbering)  
            pyautogui.hotkey('ctrl', 'v')   
            pyautogui.press('tab') 
            pyautogui.press('tab')  
              
            # Intervensi 

            intervensi.insert(0, "monitor tanda vital") # Add to beginning list
            intervensi.append("kolaborasi dengan tim medis") # Add to end of list 
            intervensi_numbering = '\n'.join(f"{i+1}. {item}" for i, item in enumerate(intervensi)) 
            pyperclip.copy(intervensi_numbering)  
            pyautogui.hotkey('ctrl', 'v')   

            pyautogui.press('tab') 
            pyautogui.press('right') 
            pyautogui.press('left') 
            pyautogui.press('tab')  
            pyautogui.write(handOverTime) 
            pyautogui.press('tab')  

            if currentHour > 6 and currentHour < 14:
                pyautogui.write('p')  
            elif currentHour > 13 and currentHour < 21:
                pyautogui.write('s')  
            else:
                pyautogui.write('m') 
            pyautogui.press('tab')   

        else: 
            # Subyektif 
            pyautogui.write(keluhan_entry.get() ) 
            if nyeriAkut_VAR.get() :
                pyautogui.write(', nyeri hilang timbul, tidak menjalar')
            
            # Obyektif
            pyautogui.press('tab')
            pyautogui.write('akral hangat, kesadaran composmentis, GCS E4V5M6,') 
            if bersihanJalanNapas_VAR.get() :
                pyautogui.write(' ronchi (+)')

            pyautogui.press('enter')
            pyautogui.write('TD : ' + sistole_entry.get()  + '/' + diastole_entry.get()  + ' mmHg')
            pyautogui.press('enter')
            pyautogui.write('Nadi : ' + nadi_entry.get()  + ' x/menit')
            pyautogui.press('enter')
            pyautogui.write('Suhu : ' + suhu_entry.get() +' C')
            pyautogui.press('enter')
            pyautogui.write('Respirasi : ' + rr_entry.get() +'x')
            pyautogui.press('enter')
            pyautogui.write('SpO2 : ' + spo2_entry.get() +'%') 
            pyautogui.press('tab') 
            pyautogui.press('tab') 
            
            # DIAGNOSA 
            if bersihanJalanNapas_VAR.get() :
                pyautogui.write('- Bersihan jalan napas tidak efektif')
                pyautogui.press('enter') 
            if hipertermia_VAR.get() :
                pyautogui.write('- Hipertermia')
                pyautogui.press('enter') 
            if hipervolemia_VAR.get() :
                pyautogui.write('- Hipervolemia')
                pyautogui.press('enter') 
            if nausea_VAR.get() :
                pyautogui.write('- Nausea')
                pyautogui.press('enter') 
            if nyeriAkut_VAR.get() :
                pyautogui.write('- Nyeri akut')
                pyautogui.press('enter') 
            if penurunanCurahJantung_VAR.get() :
                pyautogui.write('- Penurunan Curah Jantung')
                pyautogui.press('enter') 
            if penurunanKapasitasAdaptif_VAR.get() :
                pyautogui.write('- Penurunan Kapasitas Adaptif Intrakranial')
                pyautogui.press('enter') 
            if polaNapas_VAR.get() :
                pyautogui.write('- Pola napas tidak efektif')
                pyautogui.press('enter') 
            if resikoInfeksi_VAR.get() :
                pyautogui.write('- Resiko infeksi')
                pyautogui.press('enter') 
            if resikoJatuh_VAR.get() :
                pyautogui.write('- Resiko jatuh')
                pyautogui.press('enter')  
            pyautogui.press('tab') 
            pyautogui.press('tab') 

            # IMPLEMENTASI

            if opt == 'p': 
                pyautogui.write('- ttv dalam batas normal')
                pyautogui.press('enter') 

                if bersihanJalanNapas_VAR.get() :
                    pyautogui.write('- produksi sputum menurun')
                    pyautogui.press('enter') 
                    pyautogui.write('- wheezing/ronchi menurun')
                    pyautogui.press('enter') 
                if hipertermia_VAR.get() :
                    pyautogui.write('- suhu tubuh dalam batas normal')
                    pyautogui.press('enter') 
                if hipervolemia_VAR.get() :
                    pyautogui.write('- intake dan output seimbang')
                    pyautogui.press('enter') 
                    pyautogui.write('- edema menurun')
                    pyautogui.press('enter') 
                if nausea_VAR.get() :
                    pyautogui.write('- Keluhan mual menurun')
                    pyautogui.press('enter') 
                if nyeriAkut_VAR.get() :
                    pyautogui.write('- skala nyeri menurun')
                    pyautogui.press('enter') 
                    pyautogui.write('- grimace berkurang')
                    pyautogui.press('enter') 
                if penurunanCurahJantung_VAR.get() :
                    pyautogui.write('- status hemodinamik membaik')
                    pyautogui.press('enter')  
                if penurunanKapasitasAdaptif_VAR.get() :
                    pyautogui.write('- tingkat kesadaran membaik')
                    pyautogui.press('enter')  
                    pyautogui.write('- irama napas reguler')
                    pyautogui.press('enter')  
                if polaNapas_VAR.get() :
                    pyautogui.write('- frekuensi napas membaik')
                    pyautogui.press('enter') 
                    pyautogui.write('- dispnea menurun')
                    pyautogui.press('enter') 
                if resikoInfeksi_VAR.get() :
                    pyautogui.write('- tidak ada tanda tanda infeksi')
                    pyautogui.press('enter') 
                if resikoJatuh_VAR.get() :
                    pyautogui.write('- tidak ada kejadian jatuh')
                    pyautogui.press('enter')  
            else: 
                lines = dr_EN.get("1.0", tk.END).strip().split("\n")  # Memecah teks menjadi daftar baris
                formatted_lines = [f"lapor dr. {line.strip()}" for line in lines]  # Menambahkan "lapor dr."
                res = "\n".join(formatted_lines)  # Menggabungkan kembali menjadi string 
                pyautogui.write(res)
            
            pyautogui.press('tab')
            pyautogui.press('tab')

            # INTERVENSI

            if opt == 'p': 
                pyautogui.write('- monitor ttv')
                pyautogui.press('enter') 
                if bersihanJalanNapas_VAR.get() :
                    pyautogui.write('- kaji keluhan batuk')
                    pyautogui.press('enter') 
                if hipertermia_VAR.get() :
                    pyautogui.write('- monitor suhu tubuh secara berkala')
                    pyautogui.press('enter') 
                if hipervolemia_VAR.get() :
                    pyautogui.write('- batasi asupan cairan')
                    pyautogui.press('enter') 
                    pyautogui.write('- monitor keseimbangan cairan')
                    pyautogui.press('enter') 
                if nausea_VAR.get() :
                    pyautogui.write('- monitor keluhan muntah')
                    pyautogui.press('enter') 
                if nyeriAkut_VAR.get() :
                    pyautogui.write('- kaji keluhan nyeri')
                    pyautogui.press('enter') 
                if penurunanCurahJantung_VAR.get() :
                    pyautogui.write('- monitor status hemodinamik')
                    pyautogui.press('enter')  
                if penurunanKapasitasAdaptif_VAR.get() :
                    pyautogui.write('- monitor peningkatan tekanan darah')
                    pyautogui.press('enter')  
                    pyautogui.write('- monitor irreguleritas irama napas')
                    pyautogui.press('enter')  
                    pyautogui.write('- monitor penurunan tingkat kesadaran')
                    pyautogui.press('enter')  
                if polaNapas_VAR.get() :
                    pyautogui.write('- pantau kepatenan jalan napas')
                    pyautogui.press('enter') 
                    pyautogui.write('- monitor saturasi secara berkala')
                    pyautogui.press('enter') 
                if resikoInfeksi_VAR.get() :
                    pyautogui.write('- pantau adanya tanda tanda infeksi')
                    pyautogui.press('enter') 
                if resikoJatuh_VAR.get() :
                    pyautogui.write('- pasang kunci bed dan siderail')
                    pyautogui.press('enter') 
                pyautogui.write('- kolaborasi dengan tim medis') 

                pyautogui.press('tab') 
                pyautogui.press('right') 
                pyautogui.press('left') 
                pyautogui.press('tab')  
                pyautogui.write(handOverTime) 
                pyautogui.press('tab')  

                if currentHour > 6 and currentHour < 14:
                    pyautogui.write('p')  
                elif currentHour > 13 and currentHour < 21:
                    pyautogui.write('s')  
                else:
                    pyautogui.write('m') 
                pyautogui.press('tab')   
    
            else:
                pyautogui.write('advis belum terhubung') 
                pyautogui.press('tab') 
                pyautogui.press('right')  
 
    def dp():  
        time.sleep(2) 
        pyautogui.write("KIE minum obat sesuai anjuran")
        pyautogui.press('enter') 
        pyautogui.write("KIE kontrol sesuai jadwal")
        pyautogui.press('tab')
        pyautogui.press('tab') 
        pyautogui.press('enter') 

    def akrid(): 
        time.sleep(2)

        keluhan = keluhan_entry.get()
        rps = rps_entry.get()
        rpd = rpd_entry.get()
        sistole = sistole_entry.get()
        diastole = diastole_entry.get()
        nadi = nadi_entry.get()
        suhu = suhu_entry.get()
        rr = rr_entry.get()
        spo2 = spo2_entry.get()
        diet = diet_entry.get()
        alergi = alergi_entry.get()

        # -- anamnesis
        pyautogui.write(keluhan) 
        pyautogui.press('tab')
        pyautogui.write(rps) 
        pyautogui.press('tab')
        pyautogui.write(rpd)  
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('left') 
        pyautogui.press('tab')
        pyautogui.press('tab')

        if alergi == '' or alergi == '-':
            pyautogui.press('right')
            pyautogui.press('left') 
            pyautogui.press('tab')
        else:
            pyautogui.press('right')
            pyautogui.press('tab')
            pyautogui.write(alergi)

        # -- psiko
        pyautogui.press('tab') 
        pyautogui.press('space')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('left')
        pyautogui.press('tab')
        pyautogui.press('space')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('space')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('left')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('left')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('left')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.write('tidak ada')

        # -- sosial
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('left') 
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('tab')
        pyautogui.write('tidak ada')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.write('tidak ada')

        # -- ekonomi
        for i in range(11):
            pyautogui.press('tab')   
        pyautogui.press('right') 
        pyautogui.press('left') 
        
        # -- nilai budaya
        pyautogui.press('tab') 
        pyautogui.write('tidak ada') 
        pyautogui.press('tab') 
        pyautogui.write('tidak ada') 
        
        # -- ttv
        pyautogui.press('tab')   
        pyautogui.write(sistole)   
        pyautogui.press('tab')   
        pyautogui.write(diastole)   
        pyautogui.press('tab')   
        pyautogui.write(nadi)   
        pyautogui.press('tab')   
        pyautogui.press('right')   
        pyautogui.press('left')   
        pyautogui.press('tab')   
        pyautogui.write(rr) 
        for i in range(4):   
            pyautogui.press('tab')    
        pyautogui.write(suhu)   
        pyautogui.press('tab')   
        pyautogui.write(spo2)   
        pyautogui.press('tab')   
        
        # -- B1
        pyautogui.press('tab') 
        pyautogui.press('space') 
        for i in range(9):
            pyautogui.press('tab')  
        pyautogui.press('space') 
        for i in range(6):
            pyautogui.press('tab')  
        pyautogui.press('right') 
        pyautogui.press('left') 
        pyautogui.press('tab') 
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('left') 
        pyautogui.press('tab') 
        pyautogui.press('tab') 
        pyautogui.press('space') 
        for i in range(8):
            pyautogui.press('tab')  
        pyautogui.press('right') 
        pyautogui.press('left') 
        pyautogui.press('tab') 
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('left') 
        pyautogui.press('tab') 
        pyautogui.press('tab') 
        pyautogui.press('right') 

        # -- B2 
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('left')  
        pyautogui.press('tab') 
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('left') 
        pyautogui.press('tab') 
        pyautogui.press('right')  
        pyautogui.press('left') 
        pyautogui.press('tab') 
        pyautogui.press('right')  
        pyautogui.press('left') 
        pyautogui.press('tab') 
        pyautogui.press('right')  
        pyautogui.press('tab') 
        pyautogui.press('right')  
        pyautogui.press('tab') 
        pyautogui.press('right')  
        pyautogui.press('left')  
        pyautogui.press('tab') 
        pyautogui.press('right')  
        pyautogui.press('tab') 
        pyautogui.press('right')  
        pyautogui.press('tab') 
        pyautogui.press('right')  
        pyautogui.press('tab') 
        pyautogui.press('right')  
        pyautogui.press('left')  
        pyautogui.press('tab') 

        # -- B3 
        pyautogui.press('tab')
        pyautogui.write('E4V5M6') 
        pyautogui.press('tab')
        pyautogui.press('space')
        for i in range(14):
            pyautogui.press('tab') 
        pyautogui.press('space') 
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('left') 
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('left') 
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('left') 
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('left') 
        pyautogui.press('tab') 
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('left') 
        pyautogui.press('tab')
        pyautogui.press('space')
        for i in range(6): 
            pyautogui.press('tab') 
        pyautogui.press('right')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('left')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('left')
        pyautogui.press('tab')
        
        # -- B4 
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('left') 
        pyautogui.press('tab') 
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('left') 
        pyautogui.press('tab') 
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('left') 
        pyautogui.press('tab')  
        pyautogui.write('-+ 500') 
        pyautogui.press('tab') 
        pyautogui.write('kuning') 
        
        # -- B5
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('left') 
        pyautogui.press('tab')  
        pyautogui.press('tab') 
        pyautogui.write('> 2x') 
        pyautogui.press('tab') 
        pyautogui.write('-+ 500 cc') 
        for i in range(5): 
            pyautogui.press('tab') 
        pyautogui.press('space') 
        for i in range(3): 
            pyautogui.press('tab') 
        pyautogui.write(diet) 
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('left')
        for i in range(7): 
            pyautogui.press('tab') 
        pyautogui.press('space') 
        pyautogui.press('tab')
        for i in range(4): 
            pyautogui.press('tab') 
        pyautogui.press('space')  
        for i in range(14): 
            pyautogui.press('tab') 
        pyautogui.press('right')
        pyautogui.press('left')  
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.write('kuning')  
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('left') 
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('left') 
        pyautogui.press('tab')
        
        # -- B6
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('left')  
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('right')  
        pyautogui.press('tab') 
        pyautogui.write('5') 
        pyautogui.press('tab') 
        pyautogui.write('5') 
        pyautogui.press('tab') 
        pyautogui.write('5') 
        pyautogui.press('tab') 
        pyautogui.write('5')  
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('right') 
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('left') 
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('left') 
        pyautogui.press('tab') 
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('left')  
        pyautogui.press('tab') 
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('left')  
        pyautogui.press('tab') 
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('left')  
        pyautogui.press('tab') 
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('left')  
        
        # -- endokrin 
        pyautogui.press('tab') 
        pyautogui.press('right')  
        pyautogui.press('tab') 
        pyautogui.press('right')  
        pyautogui.press('tab') 
        pyautogui.press('right')  
        pyautogui.press('tab') 
        pyautogui.press('right')   
        for i in range(6): 
            pyautogui.press('tab') 

        # -- asesmen nyeri 
        if nyeriAkut_VAR.get() :
            pyautogui.press('tab') 
            pyautogui.press('right') 
            pyautogui.press('tab') 
            pyautogui.press('enter')
            pyautogui.press('down') 
            pyautogui.press('down') 
            pyautogui.press('down') 
            pyautogui.press('enter') 
            pyautogui.press('tab') 
            pyautogui.press('right') 
            pyautogui.press('left') 
            pyautogui.press('tab') 
            pyautogui.press('right') 
            pyautogui.press('tab') 
            pyautogui.press('tab') 
            pyautogui.press('right') 
            pyautogui.press('left') 
            for i in range(5): 
                pyautogui.press('tab') 
            pyautogui.press('tab') 
        else:
            pyautogui.press('tab') 
            pyautogui.press('right') 
            pyautogui.press('left') 
            pyautogui.press('tab') 
     
        # -- nutrisi
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('left')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('tab')
        pyautogui.press('right')

        # -- FUNGSIONAL INDEX
        for i in range(10): 
            pyautogui.press('tab')
        
        # -- MORSE FALL SCALE
        for i in range(2): 
            pyautogui.press('tab')
            pyautogui.press('right')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('right')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('left')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('right')
        pyautogui.press('tab')
        pyautogui.press('right') 

        # -- DEKUBITUS 
        for i in range(5): 
            pyautogui.press('tab')
            pyautogui.press('right')
            pyautogui.press('right')
            pyautogui.press('right')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('right')

        # -- RESIKO PENYAKIT MENULAR
        pyautogui.press('tab')
        pyautogui.press('right')
        
        # -- RESTRAIN
        for i in range(6):
            pyautogui.press('tab') 
        pyautogui.press('right')
        pyautogui.press('left')
        pyautogui.press('tab') 
        pyautogui.press('tab') 
        pyautogui.press('right')
        pyautogui.press('left')
        pyautogui.press('tab') 

        # -- EWS
        pyautogui.press('tab') 
        pyautogui.write(rr)  
        pyautogui.press('tab') 
        pyautogui.write(spo2)  
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('left') 
        pyautogui.press('tab') 
        pyautogui.write(suhu) 
        pyautogui.press('tab') 
        pyautogui.write(sistole) 
        pyautogui.press('tab') 
        pyautogui.write(nadi)
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('left')  

        # -- DISCARD PLANNING
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('left') 
        for i in range(3):
            pyautogui.press('tab') 
            pyautogui.press('right')  
        for i in range(30):
            pyautogui.press('tab') 
        pyautogui.press('space')  
        for i in range(11):
            pyautogui.press('tab') 
        pyautogui.press('space')  
        for i in range(20):
            pyautogui.press('tab') 
        pyautogui.write('-')    

    def akrig():  
        time.sleep(2)

        keluhan = keluhan_entry.get()
        rps = rps_entry.get()
        rpd = rpd_entry.get()
        sistole = sistole_entry.get()
        diastole = diastole_entry.get()
        nadi = nadi_entry.get()
        suhu = suhu_entry.get()
        rr = rr_entry.get()
        spo2 = spo2_entry.get()
        diet = diet_entry.get()
        alergi = alergi_entry.get()

        # -- anamnesis
        pyautogui.write(keluhan) 
        pyautogui.press('tab')
        pyautogui.write(rps) 
        pyautogui.press('tab')
        pyautogui.write(rpd)  
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('left') 
        pyautogui.press('tab')
        pyautogui.press('tab')

        if alergi == '' or alergi == '-':
            pyautogui.press('right')
            pyautogui.press('left') 
            pyautogui.press('tab')
        else:
            pyautogui.press('right')
            pyautogui.press('tab')
            pyautogui.write(alergi)

        # -- psiko
        pyautogui.press('tab') 
        pyautogui.press('space')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('left')
        pyautogui.press('tab')
        pyautogui.press('space')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('space')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('left')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('left')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('left')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.write('tidak ada')

        # -- sosial
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('left') 
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('tab')
        pyautogui.write('tidak ada')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.write('tidak ada')

        # -- ekonomi
        for i in range(11):
            pyautogui.press('tab')   
        pyautogui.press('right') 
        pyautogui.press('left') 
        
        # -- nilai budaya
        pyautogui.press('tab') 
        pyautogui.write('tidak ada') 
        pyautogui.press('tab') 
        pyautogui.write('tidak ada') 
        
        # -- ttv
        pyautogui.press('tab')   
        pyautogui.write(sistole)   
        pyautogui.press('tab')   
        pyautogui.write(diastole)   
        pyautogui.press('tab')   
        pyautogui.write(nadi)   
        pyautogui.press('tab')   
        pyautogui.press('right')   
        pyautogui.press('left')   
        pyautogui.press('tab')   
        pyautogui.write(rr) 
        for i in range(4):   
            pyautogui.press('tab')    
        pyautogui.write(suhu)   
        pyautogui.press('tab')   
        pyautogui.write(spo2)   
        pyautogui.press('tab')   
        
        # -- B1
        pyautogui.press('tab') 
        pyautogui.press('space') 
        for i in range(9):
            pyautogui.press('tab')  
        pyautogui.press('space') 
        for i in range(6):
            pyautogui.press('tab')  
        pyautogui.press('right') 
        pyautogui.press('left') 
        pyautogui.press('tab') 
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('left') 
        pyautogui.press('tab') 
        pyautogui.press('tab') 
        pyautogui.press('space') 
        for i in range(8):
            pyautogui.press('tab')  
        pyautogui.press('right') 
        pyautogui.press('left') 
        pyautogui.press('tab') 
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('left') 
        pyautogui.press('tab') 
        pyautogui.press('tab') 
        pyautogui.press('right') 

        # -- B2 
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('left')  
        pyautogui.press('tab') 
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('left') 
        pyautogui.press('tab') 
        pyautogui.press('right')  
        pyautogui.press('left') 
        pyautogui.press('tab') 
        pyautogui.press('right')  
        pyautogui.press('left') 
        pyautogui.press('tab') 
        pyautogui.press('right')  
        pyautogui.press('tab') 
        pyautogui.press('right')  
        pyautogui.press('tab') 
        pyautogui.press('right')  
        pyautogui.press('left')  
        pyautogui.press('tab') 
        pyautogui.press('right')  
        pyautogui.press('tab') 
        pyautogui.press('right')  
        pyautogui.press('tab') 
        pyautogui.press('right')  
        pyautogui.press('tab') 
        pyautogui.press('right')  
        pyautogui.press('left')  
        pyautogui.press('tab') 

        # -- B3 
        pyautogui.press('tab')
        pyautogui.write('E4V5M6') 
        pyautogui.press('tab')
        pyautogui.press('space')
        for i in range(14):
            pyautogui.press('tab') 
        pyautogui.press('space') 
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('left') 
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('left') 
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('left') 
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('left') 
        pyautogui.press('tab') 
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('left') 
        pyautogui.press('tab')
        pyautogui.press('space')
        for i in range(6): 
            pyautogui.press('tab') 
        pyautogui.press('right')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('left')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('left')
        pyautogui.press('tab')
        
        # -- B4 
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('left') 
        pyautogui.press('tab') 
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('left') 
        pyautogui.press('tab') 
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('left') 
        pyautogui.press('tab')  
        pyautogui.write('-+ 500') 
        pyautogui.press('tab') 
        pyautogui.write('kuning') 
        
        # -- B5
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('left') 
        pyautogui.press('tab')  
        pyautogui.press('tab') 
        pyautogui.write('> 2x') 
        pyautogui.press('tab') 
        pyautogui.write('-+ 500 cc') 
        for i in range(5): 
            pyautogui.press('tab') 
        pyautogui.press('space') 
        for i in range(3): 
            pyautogui.press('tab') 
        pyautogui.write(diet) 
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('left')
        for i in range(7): 
            pyautogui.press('tab') 
        pyautogui.press('space') 
        pyautogui.press('tab')
        for i in range(4): 
            pyautogui.press('tab') 
        pyautogui.press('space')  
        for i in range(14): 
            pyautogui.press('tab') 
        pyautogui.press('right')
        pyautogui.press('left')  
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.write('kuning')  
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('left') 
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('left') 
        pyautogui.press('tab')
        
        # -- B6
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('left')  
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('right')  
        pyautogui.press('tab') 
        pyautogui.write('5') 
        pyautogui.press('tab') 
        pyautogui.write('5') 
        pyautogui.press('tab') 
        pyautogui.write('5') 
        pyautogui.press('tab') 
        pyautogui.write('5')  
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('right') 
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('left') 
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('left') 
        pyautogui.press('tab') 
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('left')  
        pyautogui.press('tab') 
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('left')  
        pyautogui.press('tab') 
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('left')  
        pyautogui.press('tab') 
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('left')  
        
        # -- endokrin 
        pyautogui.press('tab') 
        pyautogui.press('right')  
        pyautogui.press('tab') 
        pyautogui.press('right')  
        pyautogui.press('tab') 
        pyautogui.press('right')  
        pyautogui.press('tab') 
        pyautogui.press('right')   
        for i in range(6): 
            pyautogui.press('tab') 
 
        # -- asesmen nyeri 
        if nyeriAkut_VAR.get() :
            pyautogui.press('tab') 
            pyautogui.press('right') 
            pyautogui.press('tab') 
            pyautogui.press('enter')
            pyautogui.press('down') 
            pyautogui.press('down') 
            pyautogui.press('down') 
            pyautogui.press('enter') 
            pyautogui.press('tab') 
            pyautogui.press('right') 
            pyautogui.press('left') 
            pyautogui.press('tab') 
            pyautogui.press('right') 
            pyautogui.press('tab') 
            pyautogui.press('tab') 
            pyautogui.press('right') 
            pyautogui.press('left') 
            for i in range(5): 
                pyautogui.press('tab') 
            pyautogui.press('tab') 
        else:
            pyautogui.press('tab') 
            pyautogui.press('right') 
            pyautogui.press('left') 
            pyautogui.press('tab') 

        # -- nutrisi
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('left')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('tab')
        pyautogui.press('right')

        # -- FUNGSIONAL INDEX
        for i in range(10): 
            pyautogui.press('tab')

        # -- ONTARIO FALL SCALE
        for i in range(9): 
            pyautogui.press('tab')
            pyautogui.press('right')
        for i in range(2): 
            pyautogui.press('tab')
            pyautogui.press('right')
            pyautogui.press('left')

        # -- DEKUBITUS 
        for i in range(5): 
            pyautogui.press('tab')
            pyautogui.press('right')
            pyautogui.press('right')
            pyautogui.press('right')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('right')

        # -- RESIKO PENYAKIT MENULAR
        pyautogui.press('tab')
        pyautogui.press('right')

        # -- FUNGSI KOGNITIF
        for i in range(10):
            pyautogui.press('tab')
            pyautogui.press('right')
            pyautogui.press('left')

        # -- PENGKAJIAN DEPRESI
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('left')
        for i in range(3):
            pyautogui.press('tab')
            pyautogui.press('right')
        for i in range(2):
            pyautogui.press('tab')
            pyautogui.press('right')
            pyautogui.press('left')
        for i in range(4):
            pyautogui.press('tab')
            pyautogui.press('right')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('left')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('tab')
        pyautogui.press('right')
        pyautogui.press('left')
        for i in range(2):
            pyautogui.press('tab')
            pyautogui.press('right')

        # -- RESTRAIN
        for i in range(6):
            pyautogui.press('tab') 
        pyautogui.press('right')
        pyautogui.press('left')
        pyautogui.press('tab') 
        pyautogui.press('tab') 
        pyautogui.press('right')
        pyautogui.press('left')
        pyautogui.press('tab') 

        # -- EWS
        pyautogui.press('tab') 
        pyautogui.write(rr)  
        pyautogui.press('tab') 
        pyautogui.write(spo2)  
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('left') 
        pyautogui.press('tab') 
        pyautogui.write(suhu) 
        pyautogui.press('tab') 
        pyautogui.write(sistole) 
        pyautogui.press('tab') 
        pyautogui.write(nadi)
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('left')  

        # -- DISCARD PLANNING
        pyautogui.press('tab') 
        pyautogui.press('right') 
        pyautogui.press('left') 
        for i in range(3):
            pyautogui.press('tab') 
            pyautogui.press('right')  
        for i in range(30):
            pyautogui.press('tab') 
        pyautogui.press('space')  
        for i in range(11):
            pyautogui.press('tab') 
        pyautogui.press('space')  
        for i in range(20):
            pyautogui.press('tab') 
        pyautogui.write('-')    
 
    def report():   
        # reset preview field
        report_EN.delete("1.0", tk.END)

        h = datetime.now().hour
        sapaan = '-' 
        if h < 10 :
            sapaan = 'pagi'
        elif 10 <= h < 15 :
            sapaan = 'siang'
        elif 14 <= h < 19 :
            sapaan = 'sore'
        else :
            sapaan = 'malam'

        text = 'Selamat ' + sapaan +' dokter,\n'
        text += 'Melaporkan pasien baru pindahan dari '+ pindahan_entry.get() +',\n\n'
        text += '*a/n '+ nama_entry.get().upper() +' / '+ usia_entry.get() +'th*\n'
        text += 'dengan '+ diagnosa_entry.get() + '\n\n'
        text += 'Keluhan : '+ keluhan_entry.get() + '\n\n'
        text += "```GCS  : 456\n"
        text += 'TD   : '+ sistole_entry.get() +'/'+ diastole_entry.get() +' mmHg\n'
        text += 'Nadi : '+ nadi_entry.get() +' x/menit\n'
        text += 'Suhu : '+ suhu_entry.get() +' C\n'
        text += 'RR   : '+ rr_entry.get() +' x/menit\n'
        text += 'SpO2 : '+ spo2_entry.get() +"%```\n\n"
        text += "`Terapi`\n"
        text += terapi_entry.get("1.0", tk.END) + '\n\n' 

        if tindakan_entry.get() != '':
            text += "`Rencana Tindakan`\n"
            text += tindakan_entry.get() + '\n\n'

        text += 'Apakah ada advis tambahan dokter? \nTerimakasih ...'  
        
        report_EN.insert(tk.END, text)  

    def rx():   
        try:
            # Reset preview field
            rx_EN.delete("1.0", tk.END)

            h = datetime.now().hour
            sapaan = '-' 
            if 3 <= h < 10 :
                sapaan = 'pagi'
            elif 10 <= h < 15 :
                sapaan = 'siang'
            elif 14 <= h < 19 :
                sapaan = 'sore'
            else :
                sapaan = 'malam' 

            text = 'Selamat ' + sapaan +' dokter, RID minta tolong eresep nggih.\n\n'
            text += '```Nama :``` *' + nama_entry.get().upper() + '*\n'
            text += '```RM   :``` *' + mr_entry.get() + '*\n\n'

            # split kalimat per baris baru
            lines = terapi_entry.get("1.0", tk.END).splitlines() 

            for line in lines:
                # jika obat syrup
                if 'syr' in line:
                    text += line + ' (1)\n'
                else: 
                    # temukan aturan pakai
                    res = re.search(r'(\d+)x', line, re.IGNORECASE)
                    if res: 
                        total = int(res.group(1)) * 3
                        text += line + ' (' + str(total) + ')\n' 
                    else:
                        text += line + ' (3)\n'
                        
            text += '\nTerimakasih ...'
            
            rx_EN.insert(tk.END, text)
  
        except Exception as e: 
            messagebox.showinfo("Error", e)  
    
    def copy_report(): 
        t = report_EN.get("1.0", tk.END) 
        app.clipboard_clear() 
        app.clipboard_append(t)
    
    def copy_rx(): 
        t = rx_EN.get("1.0", tk.END) 
        app.clipboard_clear() 
        app.clipboard_append(t)

    # TAB 3 | Diagnose

    def reset(): 
        bersihanJalanNapas_VAR.set(False)  
        diare_VAR.set(False)  
        hipertermia_VAR.set(False)  
        hipervolemia_VAR.set(False)  
        ketidakstabilanGD_VAR.set(False)   
        nausea_VAR.set(False)   
        nyeriAkut_VAR.set(False)
        penurunanCurahJantung_VAR.set(False)
        penurunanKapasitasAdaptif_VAR.set(False)
        polaNapas_VAR.set(False)
        resikoInfeksi_VAR.set(False)
        resikoJatuh_VAR.set(False)

    def diagnose():
        # Kumpulan variabel dengan nama dan nilainya
        variables = [
            ("bersihanJalanNapas_VAR", bersihanJalanNapas_VAR.get()),
            ("diare_VAR", diare_VAR.get()),
            ("hipertermia_VAR", hipertermia_VAR.get()),
            ("hipervolemia_VAR", hipervolemia_VAR.get()),
            ("ketidakstabilanGD_VAR", ketidakstabilanGD_VAR.get()),
            ("nausea_VAR", nausea_VAR.get()),
            ("nyeriAkut_VAR", nyeriAkut_VAR.get()),
            ("penurunanCurahJantung_VAR", penurunanCurahJantung_VAR.get()),
            ("penurunanKapasitasAdaptif_VAR", penurunanKapasitasAdaptif_VAR.get()),
            ("polaNapas_VAR", polaNapas_VAR.get()),
            ("resikoInfeksi_VAR", resikoInfeksi_VAR.get()),
            ("resikoJatuh_VAR", resikoJatuh_VAR.get())
        ]
  
        # Cari variabel terakhir yang bernilai True
        last_true = None
        for name, value in variables:
            if value:
                last_true = name
  
        time.sleep(2) 
        for _ in range(5):
            pyautogui.press('tab')
        if bersihanJalanNapas_VAR.get():
                pyautogui.press('space')
                if last_true == 'bersihanJalanNapas_VAR' :
                    implement()
                    return
        for _ in range(8):
            pyautogui.press('tab')
        if diare_VAR.get():
                pyautogui.press('space')    
                if last_true == 'diare_VAR' :
                    implement()
                    return 
        for _ in range(32):
            pyautogui.press('tab')
        if hipertermia_VAR.get():
                pyautogui.press('space')   
                if last_true == 'hipertermia_VAR' :
                    implement()
                    return  
        for _ in range(2):
            pyautogui.press('tab')
        if hipervolemia_VAR.get():
                pyautogui.press('space')  
                if last_true == 'hipervolemia_VAR' :
                    implement()
                    return  
        for _ in range(24):
            pyautogui.press('tab')
        if ketidakstabilanGD_VAR.get():
                pyautogui.press('space')    
                if last_true == 'ketidakstabilanGD_VAR' :
                    implement()
                    return
        for _ in range(10):
            pyautogui.press('tab')
        if nausea_VAR.get():
                pyautogui.press('space')    
                if last_true == 'nausea_VAR' :
                    implement()
                    return
        for _ in range(2):
            pyautogui.press('tab')
        if nyeriAkut_VAR.get():
                pyautogui.press('space')    
                if last_true == 'nyeriAkut_VAR' :
                    implement()
                    return
        for _ in range(6):
            pyautogui.press('tab')
        if penurunanCurahJantung_VAR.get():
                pyautogui.press('space')    
                if last_true == 'penurunanCurahJantung_VAR' :
                    implement()
                    return
        for _ in range(2):
            pyautogui.press('tab')
        if penurunanKapasitasAdaptif_VAR.get():
                pyautogui.press('space')    
                if last_true == 'penurunanKapasitasAdaptif_VAR' :
                    implement()
                    return
        for _ in range(8):
            pyautogui.press('tab')
        if polaNapas_VAR.get():
                pyautogui.press('space')    
                if last_true == 'polaNapas_VAR' :
                    implement()
                    return
        for _ in range(28):
            pyautogui.press('tab')
        if resikoInfeksi_VAR.get():
                pyautogui.press('space')    
                if last_true == 'resikoInfeksi_VAR' :
                    implement()
                    return
        for _ in range(4):
            pyautogui.press('tab')
        if resikoJatuh_VAR.get():
                pyautogui.press('space')   
                if last_true == 'resikoJatuh_VAR' :
                    implement()
                    return  
   
    def implement():
        messagebox.showinfo("?", "implementasi sudah dimuat?") 
        time.sleep(2)
        
        # PENYEBAB 
        if bersihanJalanNapas_VAR.get():
            for _ in range(12):
                pyautogui.press('tab')
            pyautogui.press('space')   
            pyautogui.press('tab') 
        if diare_VAR.get():
            for _ in range(9):
                pyautogui.press('tab')
            pyautogui.press('space')   
            for _ in range(4):
                pyautogui.press('tab')   
        if hipertermia_VAR.get():
            for _ in range(5):
                pyautogui.press('tab')
            pyautogui.press('space')  
            for _ in range(3):
                pyautogui.press('tab')  
        if hipervolemia_VAR.get():
            pyautogui.press('tab')
            pyautogui.press('space')   
            for _ in range(3):
                pyautogui.press('tab') 
        if ketidakstabilanGD_VAR.get():
            pyautogui.press('tab')
            pyautogui.press('space')    
            for _ in range(11):
                pyautogui.press('tab') 
        if nausea_VAR.get():
            pyautogui.press('tab')
            pyautogui.press('space')
            for _ in range(17):
                pyautogui.press('tab') 
        if nyeriAkut_VAR.get():
            pyautogui.press('tab')
            pyautogui.press('space') 
            for _ in range(2):
                pyautogui.press('tab') 
        if penurunanCurahJantung_VAR.get():
            for _ in range(3):
                pyautogui.press('tab')
            pyautogui.press('space') 
            for _ in range(2):
                pyautogui.press('tab')    
        if penurunanKapasitasAdaptif_VAR.get():
            for _ in range(3):
                pyautogui.press('tab')
            pyautogui.press('space') 
            for _ in range(3):
                pyautogui.press('tab')   
        if polaNapas_VAR.get():
            for _ in range(8):
                pyautogui.press('tab')
            pyautogui.press('space')  
            for _ in range(7):
                pyautogui.press('tab')  
        if resikoInfeksi_VAR.get():
            for _ in range(13):
                pyautogui.press('tab')
            pyautogui.press('space')   
            for _ in range(20):
                pyautogui.press('tab')  
        if resikoJatuh_VAR.get():
            for _ in range(4):
                pyautogui.press('tab')
            pyautogui.press('space')   
            for _ in range(23):
                pyautogui.press('tab') 

        # GEJALA
        
        if bersihanJalanNapas_VAR.get():
            pyautogui.press('tab') 
            pyautogui.press('space')   
            for _ in range(11):
                pyautogui.press('tab')
        if diare_VAR.get():
            for _ in range(4):
                pyautogui.press('tab')
            pyautogui.press('space')   
            for _ in range(2):
                pyautogui.press('tab')   
        if hipertermia_VAR.get():
            for _ in range(6):
                pyautogui.press('tab')
            pyautogui.press('space')   
        if hipervolemia_VAR.get():
            for _ in range(9):
                pyautogui.press('tab')  
            pyautogui.press('space')   
            for _ in range(6):
                pyautogui.press('tab')  
        if ketidakstabilanGD_VAR.get():
            for _ in range(3):
                pyautogui.press('tab')
            pyautogui.press('space')    
            for _ in range(13):
                pyautogui.press('tab')  
        if nausea_VAR.get():
            pyautogui.press('tab')
            pyautogui.press('space')
            for _ in range(10):
                pyautogui.press('tab')  
        if nyeriAkut_VAR.get():
            pyautogui.press('tab')
            pyautogui.press('space') 
            for _ in range(12):
                pyautogui.press('tab')  
        if penurunanCurahJantung_VAR.get():
            for _ in range(16):
                pyautogui.press('tab')
            pyautogui.press('space')  
            for _ in range(3):
                pyautogui.press('tab')   
        if penurunanKapasitasAdaptif_VAR.get():
            for _ in range(3):
                pyautogui.press('tab')
            pyautogui.press('space') 
            for _ in range(13):
                pyautogui.press('tab')  
        if polaNapas_VAR.get(): 
            pyautogui.press('tab')
            pyautogui.press('space')  
            for _ in range(12):
                pyautogui.press('tab')   

        # LUARAN
        
        if bersihanJalanNapas_VAR.get():
            pyautogui.press('tab')  
        if diare_VAR.get(): 
            pyautogui.press('tab') 
        if hipertermia_VAR.get():
            pyautogui.press('tab')
        if hipervolemia_VAR.get():
            pyautogui.press('tab')  
        if ketidakstabilanGD_VAR.get():
            pyautogui.press('tab') 
        if nausea_VAR.get():
            pyautogui.press('tab') 
        if nyeriAkut_VAR.get():
            pyautogui.press('tab')
        if penurunanCurahJantung_VAR.get():
            pyautogui.press('tab')  
        if penurunanKapasitasAdaptif_VAR.get():
            pyautogui.press('tab') 
        if polaNapas_VAR.get(): 
            pyautogui.press('tab') 
        if resikoInfeksi_VAR.get():
            pyautogui.press('tab') 
        if resikoJatuh_VAR.get(): 
            pyautogui.press('tab') 
    
        # KRITERIA HASIL
        
        if bersihanJalanNapas_VAR.get():
            for _ in range(3):
                pyautogui.press('tab') 
            pyautogui.press('space') 
            pyautogui.press('tab')   
            pyautogui.press('space') 
            for _ in range(5):
                pyautogui.press('tab')  
            pyautogui.press('space') 
            for _ in range(3):
                pyautogui.press('tab')  
        if diare_VAR.get():
            pyautogui.press('tab')   
            pyautogui.press('space') 
            for _ in range(3):
                pyautogui.press('tab')
            pyautogui.press('space')   
            for _ in range(2):
                pyautogui.press('tab')
            pyautogui.press('space')   
            for _ in range(3):
                pyautogui.press('tab')
            pyautogui.press('space')  
        if hipertermia_VAR.get():
            pyautogui.press('tab')   
            pyautogui.press('space')  
            for _ in range(6):
                pyautogui.press('tab')
            pyautogui.press('space')
            for _ in range(3):
                pyautogui.press('tab')   
        if hipervolemia_VAR.get():
            for _ in range(3):
                pyautogui.press('tab')  
            pyautogui.press('space')  
            for _ in range(2):
                pyautogui.press('tab')  
            pyautogui.press('space')  
            for _ in range(2):
                pyautogui.press('tab')  
            pyautogui.press('space') 
            for _ in range(3):
                pyautogui.press('tab')  
            pyautogui.press('space')  
            for _ in range(4):
                pyautogui.press('tab')  
        if ketidakstabilanGD_VAR.get():
            for _ in range(4):
                pyautogui.press('tab')
            pyautogui.press('space')  
            for _ in range(7):
                pyautogui.press('tab')
            pyautogui.press('space')  
            for _ in range(5):
                pyautogui.press('tab') 
        if nausea_VAR.get():
            pyautogui.press('tab')
            pyautogui.press('space')
            for _ in range(4):
                pyautogui.press('tab') 
            pyautogui.press('space')
            for _ in range(7):
                pyautogui.press('tab')  
        if nyeriAkut_VAR.get():
            for _ in range(12):
                pyautogui.press('tab') 
            pyautogui.press('space') 
            for _ in range(7):
                pyautogui.press('tab') 
            pyautogui.press('space')  
            for _ in range(6):
                pyautogui.press('tab')   
        if penurunanCurahJantung_VAR.get():
            for _ in range(4):
                pyautogui.press('tab')
            pyautogui.press('space')  
            pyautogui.press('tab') 
        if penurunanKapasitasAdaptif_VAR.get():
            pyautogui.press('tab')
            pyautogui.press('space')  
            for _ in range(5):
                pyautogui.press('tab')
            pyautogui.press('space')  
            for _ in range(9):
                pyautogui.press('tab')  
        if polaNapas_VAR.get(): 
            for _ in range(3):
                pyautogui.press('tab')   
            pyautogui.press('space')  
            pyautogui.press('tab')   
            pyautogui.press('space')
            for _ in range(6):
                pyautogui.press('tab')   
            pyautogui.press('space')    
            for _ in range(3):
                pyautogui.press('tab')  
        if resikoInfeksi_VAR.get(): 
            for _ in range(3):
                pyautogui.press('tab')   
            pyautogui.press('space')   
            for _ in range(2):
                pyautogui.press('tab')   
            pyautogui.press('space')    
        if resikoJatuh_VAR.get(): 
            pyautogui.press('tab')   
            pyautogui.press('space')     
            for _ in range(3):
                pyautogui.press('tab') 

        # INTERVENSI | OBSERVASI
        
        if bersihanJalanNapas_VAR.get():
            pyautogui.press('tab')   
            pyautogui.press('space') 
            for _ in range(3):
                pyautogui.press('tab') 
            pyautogui.press('space') 
            for _ in range(7):
                pyautogui.press('tab') 
            pyautogui.press('space') 
            pyautogui.press('tab')  
        if diare_VAR.get():
            for _ in range(5):
                pyautogui.press('tab')
            pyautogui.press('space')  
            pyautogui.press('tab')   
            pyautogui.press('space')  
            for _ in range(2):
                pyautogui.press('tab')
            pyautogui.press('space')    
            pyautogui.press('tab')   
        if hipertermia_VAR.get():
            for _ in range(2):
                pyautogui.press('tab')
            pyautogui.press('space') 
            for _ in range(3):
                pyautogui.press('tab')    
        if hipervolemia_VAR.get():
            for _ in range(3):
                pyautogui.press('tab')  
            pyautogui.press('space')  
            pyautogui.press('tab')  
            pyautogui.press('space')    
            for _ in range(4):
                pyautogui.press('tab')   
        if ketidakstabilanGD_VAR.get():
            for _ in range(2):
                pyautogui.press('tab')
            pyautogui.press('space')  
            for _ in range(3):
                pyautogui.press('tab')
            pyautogui.press('space')  
            pyautogui.press('tab')
            pyautogui.press('space')   
            for _ in range(2):
                pyautogui.press('tab')  
        if nausea_VAR.get():
            for _ in range(6):
                pyautogui.press('tab') 
            pyautogui.press('space') 
            for _ in range(4):
                pyautogui.press('tab')  
            pyautogui.press('space') 
            for _ in range(3):
                pyautogui.press('tab')  
        if nyeriAkut_VAR.get():
            for _ in range(4):
                pyautogui.press('tab') 
            pyautogui.press('space') 
            for _ in range(2):
                pyautogui.press('tab') 
            pyautogui.press('space')  
            for _ in range(6):
                pyautogui.press('tab')   
        if penurunanCurahJantung_VAR.get():
            for _ in range(2):
                pyautogui.press('tab')
            pyautogui.press('space')  
            for _ in range(3):
                pyautogui.press('tab')
        if penurunanKapasitasAdaptif_VAR.get():
            for _ in range(3):
                pyautogui.press('tab')
            pyautogui.press('space')
            for _ in range(3):
                pyautogui.press('tab')
            pyautogui.press('space')
            for _ in range(6):
                pyautogui.press('tab')
            pyautogui.press('space')  
            for _ in range(7):
                pyautogui.press('tab')   
        if polaNapas_VAR.get(): 
            for _ in range(3):
                pyautogui.press('tab')   
            pyautogui.press('space')   
            for _ in range(6):
                pyautogui.press('tab')   
            pyautogui.press('space')  
            pyautogui.press('tab')
        if resikoInfeksi_VAR.get(): 
            pyautogui.press('tab')   
            pyautogui.press('space')    
            pyautogui.press('tab')   
        if resikoJatuh_VAR.get(): 
            pyautogui.press('tab')   
            pyautogui.press('space')     
            for _ in range(2):
                pyautogui.press('tab') 
            pyautogui.press('space') 
            pyautogui.press('tab')     

        # INTERVENSI | TERAPIUTIK
        
        if bersihanJalanNapas_VAR.get():
            pyautogui.press('tab')   
            pyautogui.press('space') 
            for _ in range(11):
                pyautogui.press('tab')   
        if diare_VAR.get():
            for _ in range(3):
                pyautogui.press('tab')
            pyautogui.press('space')   
            for _ in range(2):
                pyautogui.press('tab')
            pyautogui.press('space')   
        if hipertermia_VAR.get():
            pyautogui.press('tab')
            pyautogui.press('space') 
            for _ in range(5):
                pyautogui.press('tab')   
        if hipervolemia_VAR.get():
            for _ in range(2):
                pyautogui.press('tab')  
            pyautogui.press('space') 
            pyautogui.press('tab')    
        if ketidakstabilanGD_VAR.get():
            for _ in range(5):
                pyautogui.press('tab')
            pyautogui.press('space') 
            for _ in range(2):
                pyautogui.press('tab')
            pyautogui.press('space') 
            for _ in range(2):
                pyautogui.press('tab') 
        if nausea_VAR.get():
            pyautogui.press('tab') 
            pyautogui.press('space') 
            for _ in range(6):
                pyautogui.press('tab')  
            pyautogui.press('space') 
            for _ in range(2):
                pyautogui.press('tab')  
            pyautogui.press('space')  
            for _ in range(2):
                pyautogui.press('tab')  
        if nyeriAkut_VAR.get():
            for _ in range(2):
                pyautogui.press('tab') 
            pyautogui.press('space') 
            pyautogui.press('tab') 
            pyautogui.press('space')  
            for _ in range(4):
                pyautogui.press('tab')    
        if penurunanCurahJantung_VAR.get():
            pyautogui.press('tab')
            pyautogui.press('space')  
            for _ in range(3):
                pyautogui.press('tab') 
        if penurunanKapasitasAdaptif_VAR.get():
            pyautogui.press('tab')
            pyautogui.press('space')
            for _ in range(11):
                pyautogui.press('tab')  
        if polaNapas_VAR.get(): 
            pyautogui.press('tab')   
            pyautogui.press('space')   
            for _ in range(9):
                pyautogui.press('tab')   
        if resikoInfeksi_VAR.get(): 
            pyautogui.press('tab')   
            pyautogui.press('space') 
            for _ in range(2): 
                pyautogui.press('tab')   
        if resikoJatuh_VAR.get():     
            for _ in range(2):
                pyautogui.press('tab') 
            pyautogui.press('space')  
            pyautogui.press('tab')   
            pyautogui.press('space')  
            for _ in range(2):
                pyautogui.press('tab')
    
        # INTERVENSI | EDUKASI
        
        if bersihanJalanNapas_VAR.get(): 
            for _ in range(7):
                pyautogui.press('tab')   
        if diare_VAR.get():
            for _ in range(3):
                pyautogui.press('tab')  
        if hipertermia_VAR.get():
            pyautogui.press('tab') 
        if hipervolemia_VAR.get():
            for _ in range(4):
                pyautogui.press('tab')   
        if ketidakstabilanGD_VAR.get():
            for _ in range(10):
                pyautogui.press('tab') 
        if nausea_VAR.get(): 
            for _ in range(7):
                pyautogui.press('tab')  
        if nyeriAkut_VAR.get():
            for _ in range(6):
                pyautogui.press('tab')   
        if penurunanKapasitasAdaptif_VAR.get(): 
            for _ in range(2):
                pyautogui.press('tab')  
        if polaNapas_VAR.get():   
            for _ in range(3):
                pyautogui.press('tab')   
        if resikoInfeksi_VAR.get():  
            for _ in range(6): 
                pyautogui.press('tab')   
        if resikoJatuh_VAR.get():       
            for _ in range(5):
                pyautogui.press('tab') 
        
        # INTERVENSI | KOLABORASI
        
        if bersihanJalanNapas_VAR.get():
            pyautogui.press('tab')   
            pyautogui.press('space')   
        if diare_VAR.get():
            for _ in range(3):
                pyautogui.press('tab')
            pyautogui.press('space')   
        if hipertermia_VAR.get():
            pyautogui.press('tab')
            pyautogui.press('space')  
        if hipervolemia_VAR.get():
            pyautogui.press('tab')  
            pyautogui.press('space') 
            pyautogui.press('tab')    
            pyautogui.press('tab')    
        if ketidakstabilanGD_VAR.get():
            pyautogui.press('tab')
            pyautogui.press('space') 
            for _ in range(3):
                pyautogui.press('tab') 
        if nausea_VAR.get():
            pyautogui.press('tab') 
            pyautogui.press('space')  
        if nyeriAkut_VAR.get():
            pyautogui.press('tab') 
            pyautogui.press('space') 
            pyautogui.press('tab')  
        if penurunanCurahJantung_VAR.get(): 
            for _ in range(4):
                pyautogui.press('tab') 
        if penurunanKapasitasAdaptif_VAR.get():
            pyautogui.press('tab')
            pyautogui.press('space')
            for _ in range(2):
                pyautogui.press('tab')  
        if polaNapas_VAR.get(): 
            pyautogui.press('tab')   
            pyautogui.press('space')    
        if resikoInfeksi_VAR.get(): 
            pyautogui.press('tab')

        # IMPLEMENTASI - OBSERVASI
        
        if bersihanJalanNapas_VAR.get():
            pyautogui.press('tab')   
            pyautogui.press('space') 
            for _ in range(3):
                pyautogui.press('tab') 
            pyautogui.press('space') 
            for _ in range(7):
                pyautogui.press('tab') 
            pyautogui.press('space') 
            pyautogui.press('tab')  
        if diare_VAR.get():
            for _ in range(5):
                pyautogui.press('tab')
            pyautogui.press('space')  
            pyautogui.press('tab')   
            pyautogui.press('space')  
            for _ in range(2):
                pyautogui.press('tab')
            pyautogui.press('space')    
            pyautogui.press('tab')   
        if hipertermia_VAR.get():
            for _ in range(2):
                pyautogui.press('tab')
            pyautogui.press('space') 
            for _ in range(3):
                pyautogui.press('tab')    
        if hipervolemia_VAR.get():
            for _ in range(3):
                pyautogui.press('tab')  
            pyautogui.press('space')  
            pyautogui.press('tab')  
            pyautogui.press('space')    
            for _ in range(4):
                pyautogui.press('tab')   
        if ketidakstabilanGD_VAR.get():
            for _ in range(2):
                pyautogui.press('tab')
            pyautogui.press('space')  
            for _ in range(3):
                pyautogui.press('tab')
            pyautogui.press('space')  
            pyautogui.press('tab')
            pyautogui.press('space')   
            for _ in range(2):
                pyautogui.press('tab')  
        if nausea_VAR.get():
            for _ in range(6):
                pyautogui.press('tab') 
            pyautogui.press('space') 
            for _ in range(4):
                pyautogui.press('tab')  
            pyautogui.press('space') 
            for _ in range(3):
                pyautogui.press('tab')  
        if nyeriAkut_VAR.get():
            for _ in range(4):
                pyautogui.press('tab') 
            pyautogui.press('space') 
            for _ in range(2):
                pyautogui.press('tab') 
            pyautogui.press('space')  
            for _ in range(6):
                pyautogui.press('tab')   
        if penurunanCurahJantung_VAR.get():
            for _ in range(2):
                pyautogui.press('tab')
            pyautogui.press('space')  
            for _ in range(3):
                pyautogui.press('tab')
        if penurunanKapasitasAdaptif_VAR.get():
            for _ in range(3):
                pyautogui.press('tab')
            pyautogui.press('space')
            for _ in range(3):
                pyautogui.press('tab')
            pyautogui.press('space')
            for _ in range(6):
                pyautogui.press('tab')
            pyautogui.press('space')  
            for _ in range(7):
                pyautogui.press('tab')   
        if polaNapas_VAR.get(): 
            pyautogui.press('tab')   
            pyautogui.press('space')   
            for _ in range(6):
                pyautogui.press('tab')   
            pyautogui.press('space')  
            for _ in range(2):
                pyautogui.press('tab')
        if resikoInfeksi_VAR.get(): 
            pyautogui.press('tab')   
            pyautogui.press('space')    
            pyautogui.press('tab')   
        if resikoJatuh_VAR.get(): 
            pyautogui.press('tab')   
            pyautogui.press('space')     
            for _ in range(2):
                pyautogui.press('tab') 
            pyautogui.press('space') 
            pyautogui.press('tab')     

        # IMPLEMENTASI | TERAPIUTIK
        
        if bersihanJalanNapas_VAR.get():
            pyautogui.press('tab')   
            pyautogui.press('space') 
            for _ in range(11):
                pyautogui.press('tab')   
        if diare_VAR.get():
            for _ in range(3):
                pyautogui.press('tab')
            pyautogui.press('space')   
            for _ in range(2):
                pyautogui.press('tab')
            pyautogui.press('space')   
        if hipertermia_VAR.get():
            pyautogui.press('tab')
            pyautogui.press('space') 
            for _ in range(7):
                pyautogui.press('tab')   
        if hipervolemia_VAR.get():
            for _ in range(2):
                pyautogui.press('tab')  
            pyautogui.press('space') 
            pyautogui.press('tab')    
        if ketidakstabilanGD_VAR.get():
            for _ in range(5):
                pyautogui.press('tab')
            pyautogui.press('space') 
            for _ in range(2):
                pyautogui.press('tab')
            pyautogui.press('space') 
            for _ in range(2):
                pyautogui.press('tab') 
        if nausea_VAR.get():
            pyautogui.press('tab') 
            pyautogui.press('space') 
            for _ in range(6):
                pyautogui.press('tab')  
            pyautogui.press('space') 
            for _ in range(2):
                pyautogui.press('tab')  
            pyautogui.press('space')  
            for _ in range(2):
                pyautogui.press('tab')  
        if nyeriAkut_VAR.get():
            for _ in range(2):
                pyautogui.press('tab') 
            pyautogui.press('space') 
            pyautogui.press('tab') 
            pyautogui.press('space')  
            for _ in range(4):
                pyautogui.press('tab')    
        if penurunanCurahJantung_VAR.get():
            pyautogui.press('tab')
            pyautogui.press('space')  
            for _ in range(3):
                pyautogui.press('tab') 
        if penurunanKapasitasAdaptif_VAR.get():
            pyautogui.press('tab')
            pyautogui.press('space')
            for _ in range(11):
                pyautogui.press('tab')  
        if polaNapas_VAR.get(): 
            for _ in range(4):
                pyautogui.press('tab')   
            pyautogui.press('space')   
            for _ in range(2):
                pyautogui.press('tab')   
        if resikoInfeksi_VAR.get(): 
            pyautogui.press('tab')   
            pyautogui.press('space') 
            for _ in range(2): 
                pyautogui.press('tab')   
            pyautogui.press('space') 
            pyautogui.press('tab')   
        if resikoJatuh_VAR.get():     
            for _ in range(2):
                pyautogui.press('tab') 
            pyautogui.press('space')  
            pyautogui.press('tab')   
            pyautogui.press('space')  
            for _ in range(4):
                pyautogui.press('tab')
    
        # IMPLEMENTASI | EDUKASI
        
        if bersihanJalanNapas_VAR.get(): 
            for _ in range(7):
                pyautogui.press('tab')   
        if diare_VAR.get():
            for _ in range(3):
                pyautogui.press('tab')  
        if hipertermia_VAR.get():
            pyautogui.press('tab') 
        if hipervolemia_VAR.get():
            for _ in range(4):
                pyautogui.press('tab')   
        if ketidakstabilanGD_VAR.get():
            for _ in range(10):
                pyautogui.press('tab') 
        if nausea_VAR.get(): 
            for _ in range(7):
                pyautogui.press('tab')  
        if nyeriAkut_VAR.get():
            for _ in range(6):
                pyautogui.press('tab')   
        if penurunanKapasitasAdaptif_VAR.get(): 
            for _ in range(2):
                pyautogui.press('tab')  
        if polaNapas_VAR.get():   
            for _ in range(3):
                pyautogui.press('tab')   
        if resikoInfeksi_VAR.get():  
            for _ in range(6): 
                pyautogui.press('tab')   
        if resikoJatuh_VAR.get():       
            for _ in range(5):
                pyautogui.press('tab') 
        
        # IMPLEMENTASI | KOLABORASI
        
        if bersihanJalanNapas_VAR.get():
            pyautogui.press('tab')   
            pyautogui.press('space')   
        if diare_VAR.get():
            for _ in range(3):
                pyautogui.press('tab')
            pyautogui.press('space')   
        if hipertermia_VAR.get():
            pyautogui.press('tab')
            pyautogui.press('space')  
        if hipervolemia_VAR.get():
            pyautogui.press('tab')  
            pyautogui.press('space') 
            pyautogui.press('tab')    
            pyautogui.press('tab')    
        if ketidakstabilanGD_VAR.get():
            pyautogui.press('tab')
            pyautogui.press('space') 
            for _ in range(4):
                pyautogui.press('tab') 
        if nausea_VAR.get():
            pyautogui.press('tab') 
            pyautogui.press('space')  
        if nyeriAkut_VAR.get():
            pyautogui.press('tab') 
            pyautogui.press('space') 
            pyautogui.press('tab')  
        if penurunanCurahJantung_VAR.get(): 
            for _ in range(4):
                pyautogui.press('tab') 
        if penurunanKapasitasAdaptif_VAR.get():
            pyautogui.press('tab')
            pyautogui.press('space')
            for _ in range(2):
                pyautogui.press('tab')  
        if polaNapas_VAR.get(): 
            pyautogui.press('tab')   
            pyautogui.press('space')    
        if resikoInfeksi_VAR.get(): 
            pyautogui.press('tab')  
        
        pyautogui.press('tab') 
        pyautogui.press('enter') 

    def redirect(opt):  
        time.sleep(2)   
        redirectTotal = int(redirectTotal_EN.get())
         
        for i in range(redirectTotal):  
            pyautogui.hotkey('ctrl', 'l')  
            pyautogui.hotkey('ctrl', 'c')  
            url = pyperclip.paste()  

            if opt == 'ttv':
                newURL = re.sub(r"(rawatinap/)[^?]+", r"\1pemeriksaan_ttv", url)  
            if opt == 'cppt': 
                newURL = re.sub(r"(rawatinap/)[^?]+", r"\1cppt", url)  
            if opt == 'diagnose': 
                newURL = re.sub(r"(rawatinap/)[^?]+", r"\1implementasi_keperawatan", url)  
            if opt == 'handover': 
                newURL = re.sub(r"(rawatinap/)[^?]+", r"\1handover_dewasa1", url)  
 
            pyperclip.copy(newURL)  
            pyautogui.hotkey('ctrl', 'v')   
            pyautogui.press('enter') 

            # hindari berpindah tab untuk page terakhir 
            if i != redirectTotal - 1: 
                pyautogui.hotkey('ctrl', 'tab')   

    def handover():
        time.sleep(2)
        for _ in range(3):
            pyautogui.press('tab') 
        pyautogui.press('space') 

        currentDate = datetime.now().strftime("%Y-%m-%d")
        currentHour = datetime.now().hour

        if currentHour > 6 and currentHour < 14:
            pyautogui.press('down')  
        elif currentHour > 13 and currentHour < 21:
            pyautogui.press('down') 
            pyautogui.press('down')  
        else:
            pyautogui.press('down') 
            pyautogui.press('down') 
            pyautogui.press('down')
        pyautogui.press('enter')   
  
        for _ in range(35):
            pyautogui.press('tab')  
        
        handOverTime = ''

        if currentHour > 6 and currentHour < 14: 
            handOverTime = currentDate + ' 14:00:00' 
        elif currentHour > 13 and currentHour < 21: 
            handOverTime = currentDate + ' 21:00:00' 
        else:
            # Shif malam
            if currentHour > 20 and currentHour < 24 :
                # ganti ke tanggal berikutnya jika sebelum jam 24
                today = datetime.today()  
                next_day = today + timedelta(days=1) 
                tomorrow = next_day.strftime("%Y-%m-%d")
 
                handOverTime = tomorrow + ' 07:00:00'  
            else : 
                # jika diatas jam 24, gunakan tanggal yang sama 
                handOverTime = currentDate + ' 07:00:00' 
 
        pyautogui.write(handOverTime) 

        pyautogui.press('tab') 
        pyautogui.press('space') 
 
    def automate(opt): 
        if opt == 'd':  
            akrid() 
        else: 
            akrig() 

        messagebox.showinfo("?", "Lanjutkan diagnosa?") 
        diagnose() 

        messagebox.showinfo("?", "Lanjutkan discard planning?")  
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'l')  
        pyautogui.hotkey('ctrl', 'c')  
        url = pyperclip.paste()   

        if opt == 'd' :
            newURL = re.sub(r'\basperawat_ranap\b', 'discharge_planning', url, flags=re.IGNORECASE)
        else:
            newURL = re.sub(r'\basperawat_ranap_geriatri\b', 'discharge_planning', url, flags=re.IGNORECASE)
  
        pyperclip.copy(newURL)  
        pyautogui.hotkey('ctrl', 'v')   
        pyautogui.press('enter') 

        messagebox.showinfo("?", "Mengisi discharge planning?")
        dp()

        messagebox.showinfo("?", "Lanjut TTV ?")  
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'l')  
        pyautogui.hotkey('ctrl', 'c')  
        url = pyperclip.paste()  
        newURL = re.sub(r'\bdischarge_planning\b', 'pemeriksaan_ttv', url, flags=re.IGNORECASE)  
        pyperclip.copy(newURL)  
        pyautogui.hotkey('ctrl', 'v')   
        pyautogui.press('enter')  

        messagebox.showinfo("?", "Start filling TTV?")  
        ttv()

        messagebox.showinfo("?", "Lanjut CPPT?")  
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'l')  
        pyautogui.hotkey('ctrl', 'c')  
        url = pyperclip.paste()  
        newURL = re.sub(r'\bpemeriksaan_ttv\b', 'cppt', url, flags=re.IGNORECASE) 
        pyperclip.copy(newURL)  
        pyautogui.hotkey('ctrl', 'v')   
        pyautogui.press('enter') 

        messagebox.showinfo("Ready", "Start filling (doctor) CPPT?")  
        cppt('l')
        messagebox.showinfo("Complete", "Start filling (nurse) CPPT?")  
        cppt('p')
        messagebox.showinfo("Complete", "Your document is complete. Good job!")  

    class modEntry(tk.Entry):
        def __init__(self, master=None, placeholder='', color='grey', *args, **kwargs):
            super().__init__(master, *args, **kwargs)
            self.placeholder = placeholder
            self.placeholder_color = color
            self.default_fg_color = self['fg']

            self.bind("<FocusIn>", self._clear_placeholder)
            self.bind("<FocusOut>", self._add_placeholder)

            self._add_placeholder()

        def _clear_placeholder(self, event=None):
            if self['fg'] == self.placeholder_color and self.get() == self.placeholder:
                self.delete(0, tk.END)
                self['fg'] = self.default_fg_color

        def _add_placeholder(self, event=None):
            if not self.get():
                self.insert(0, self.placeholder)
                self['fg'] = self.placeholder_color
  
    class modText(tk.Text):
        def __init__(self, master=None, placeholder='', color='grey', *args, **kwargs):
            super().__init__(master, *args, **kwargs)
            self.placeholder = placeholder
            self.placeholder_color = color
            self.default_fg_color = self['fg'] if 'fg' in kwargs else 'black'

            self._add_placeholder()
            self.bind("<FocusIn>", self._clear_placeholder)
            self.bind("<FocusOut>", self._add_placeholder)

        def _add_placeholder(self, event=None):
            if self.get("1.0", "end-1c") == "":
                self.insert("1.0", self.placeholder)
                self.config(fg=self.placeholder_color)

        def _clear_placeholder(self, event=None):
            if self.get("1.0", "end-1c") == self.placeholder:
                self.delete("1.0", "end")
                self.config(fg=self.default_fg_color)

    # Main apps GUI
 
    app = tk.Tk()
    app.title("males-banget")   
    app.after(3600000, app.destroy)
    app.attributes('-topmost', True)  
       
    ff = 'Calibri'
    fs = '8'
 
    notebook = ttk.Notebook(app)
    notebook.pack(expand=True, fill='both')
 
    tab1 = ttk.Frame(notebook)
    tab2 = ttk.Frame(notebook) 
 
    notebook.add(tab1, text='Patient')
    notebook.add(tab2, text='Report') 
   
    identity_frame = ttk.Frame(tab1)
    identity_frame.grid(row=0, column=0, pady=1, sticky="w")  
    
    pindahan_entry = modEntry(identity_frame, width='5', font=(ff, fs), placeholder='Fr') 
    pindahan_entry.pack(side=tk.LEFT, padx='1')  
    mr_entry = modEntry(identity_frame, width='8', font=(ff, fs), placeholder='MR') 
    mr_entry.pack(side=tk.LEFT, padx='1')   
    nama_entry = modEntry(identity_frame, width='19', font=(ff, fs), placeholder='Nama') 
    nama_entry.pack(side=tk.LEFT, padx='1')  
    usia_entry = modEntry(identity_frame, width='5', font=(ff, fs), placeholder='Age') 
    usia_entry.pack(side=tk.LEFT, padx='1')  
    
    diagnosa_entry = modEntry(tab1, width='40', font=(ff, fs), placeholder='Diagnosa') 
    diagnosa_entry.grid(row=1, column=0, padx=1, pady=1, sticky="w")
 
    keluhan_entry = modEntry(tab1, width='40', font=(ff, fs), placeholder='Keluhan') 
    keluhan_entry.grid(row=2, column=0, padx=1, pady=1, sticky="w") 
 
    rps_entry = modEntry(tab1, width='40', font=(ff, fs), placeholder='RPS') 
    rps_entry.grid(row=3, column=0, padx=1, pady=1, sticky="w") 
 
    rpd_entry = modEntry(tab1, width='40', font=(ff, fs), placeholder='RPD') 
    rpd_entry.grid(row=4, column=0, padx=1, pady=1, sticky="w") 
  
    ttv_frame = ttk.Frame(tab1)
    ttv_frame.grid(row=5, column=0, sticky="w")  

    sistole_entry = modEntry(ttv_frame, width='5', font=(ff, fs), placeholder='Sis') 
    sistole_entry.pack(side=tk.LEFT, padx='1')  
    diastole_entry = modEntry(ttv_frame, width='5', font=(ff, fs), placeholder='Dia') 
    diastole_entry.pack(side=tk.LEFT, padx='1')  
    nadi_entry = modEntry(ttv_frame, width='5', font=(ff, fs), placeholder='Pul') 
    nadi_entry.pack(side=tk.LEFT, padx='1')  
    suhu_entry = modEntry(ttv_frame, width='5', font=(ff, fs), placeholder='Temp') 
    suhu_entry.pack(side=tk.LEFT, padx='1')  
    rr_entry = modEntry(ttv_frame, width='5', font=(ff, fs), placeholder='Resp') 
    rr_entry.pack(side=tk.LEFT, padx='1')  
    spo2_entry = modEntry(ttv_frame, width='5', font=(ff, fs), placeholder='Sat') 
    spo2_entry.pack(side=tk.LEFT, padx='1')
  
    diet_alergi_frame = ttk.Frame(tab1)
    diet_alergi_frame.grid(row=6, column=0, sticky="w")  
    diet_entry = modEntry(diet_alergi_frame, width='5', font=(ff, fs), placeholder='Diet') 
    diet_entry.pack(side=tk.LEFT, padx='1') 
    alergi_entry = modEntry(diet_alergi_frame, width='34', font=(ff, fs), placeholder='Allergy') 
    alergi_entry.pack(side=tk.LEFT, padx='1')  
      
    tindakan_entry = modEntry(tab1, width=40, font=(ff, fs), placeholder='Plan') 
    tindakan_entry.grid(row=7, column=0, padx=1, pady=1, sticky="w") 
 
    dr_EN = modText(tab1, width=40, height=2, font=(ff, fs), placeholder='Doctor')
    dr_EN.grid(row=8, column=0, padx=1, pady=1, sticky="w") 
      
    terapi_entry = modText(tab1, width=40, height=5, font=(ff, fs), placeholder='Therapy')
    terapi_entry.grid(row=9, column=0, padx=1, pady=1, sticky="w")  

    # DIAGNOSA
 
    bersihanJalanNapas_VAR = tk.BooleanVar()  
    bersihanJalanNapas = tk.Checkbutton(tab1, text="Bersihan Jalan Napas", font=(ff, fs), variable=bersihanJalanNapas_VAR)
    bersihanJalanNapas.grid(row=10, column=0, sticky='W')  

    diare_VAR = tk.BooleanVar()  
    diare = tk.Checkbutton(tab1, text="Diare", font=(ff, fs), variable=diare_VAR)
    diare.grid(row=11, column=0, sticky='W')  
  
    hipertermia_VAR = tk.BooleanVar()  
    hipertermia = tk.Checkbutton(tab1, text="Hipertermia", font=(ff, fs), variable=hipertermia_VAR)
    hipertermia.grid(row=12, column=0, sticky='W') 

    hipervolemia_VAR = tk.BooleanVar()  
    hipervolemia = tk.Checkbutton(tab1, text="Hipervolemia", font=(ff, fs), variable=hipervolemia_VAR)
    hipervolemia.grid(row=13, column=0, sticky='W')            

    ketidakstabilanGD_VAR = tk.BooleanVar()   
    ketidakstabilanGD = tk.Checkbutton(tab1, text="Ketidakstabilan GD", font=(ff, fs), variable=ketidakstabilanGD_VAR)
    ketidakstabilanGD.grid(row=14, column=0, sticky='W') 

    nausea_VAR = tk.BooleanVar() 
    nausea = tk.Checkbutton(tab1, text="Nausea", font=(ff, fs), variable=nausea_VAR)
    nausea.grid(row=15, column=0, sticky='W') 

    nyeriAkut_VAR = tk.BooleanVar()
    nyeriAkut = tk.Checkbutton(tab1, text="Nyeri Akut", font=(ff, fs), variable=nyeriAkut_VAR)
    nyeriAkut.grid(row=16, column=0, sticky='W') 

    penurunanCurahJantung_VAR = tk.BooleanVar()
    penurunanCurahJantung = tk.Checkbutton(tab1, text="Penurunan Curah Jantung", font=(ff, fs), variable=penurunanCurahJantung_VAR)
    penurunanCurahJantung.grid(row=17, column=0, sticky='W') 

    penurunanKapasitasAdaptif_VAR = tk.BooleanVar()
    penurunanKapasitasAdaptif = tk.Checkbutton(tab1, text="Penurunan Kapasitas Adaptif", font=(ff, fs), variable=penurunanKapasitasAdaptif_VAR)
    penurunanKapasitasAdaptif.grid(row=18, column=0, sticky='W') 

    polaNapas_VAR = tk.BooleanVar()
    polaNapas = tk.Checkbutton(tab1, text="Pola Napas", font=(ff, fs), variable=polaNapas_VAR)
    polaNapas.grid(row=19, column=0, sticky='W') 

    resikoInfeksi_VAR = tk.BooleanVar()
    resikoInfeksi = tk.Checkbutton(tab1, text="Resiko Infeksi", font=(ff, fs), variable=resikoInfeksi_VAR)
    resikoInfeksi.grid(row=20, column=0, sticky='W') 

    resikoJatuh_VAR = tk.BooleanVar()
    resikoJatuh = tk.Checkbutton(tab1, text="Resiko Jatuh", font=(ff, fs), variable=resikoJatuh_VAR)
    resikoJatuh.grid(row=21, column=0, sticky='W') 
  
    # BUTTON

    rowButton_1_FR = ttk.Frame(tab1)
    rowButton_1_FR.grid(row=22, column=0, padx=1, pady=1, sticky="w")  
     
    scan_BT = tk.Button(rowButton_1_FR, text="scan-i", font=(ff, fs), command=lambda: scan('i'))
    scan_BT.pack(side=tk.LEFT, padx='1')   
    scan_transfer_BT = tk.Button(rowButton_1_FR, text="scan-t", font=(ff, fs), command=lambda: scan('t'))
    scan_transfer_BT.pack(side=tk.LEFT, padx='1')   
    akrid_BT = tk.Button(rowButton_1_FR, text="asd", font=(ff, fs), command=akrid) 
    akrid_BT.pack(side=tk.LEFT, padx='1')   
    akrig_BT = tk.Button(rowButton_1_FR, text="asg", font=(ff, fs), command=akrig) 
    akrig_BT.pack(side=tk.LEFT, padx='1') 

    rowButton_2_FR = ttk.Frame(tab1)
    rowButton_2_FR.grid(row=23, column=0, padx=1, pady=1, sticky="w")  

    dp_BT = tk.Button(rowButton_2_FR, text="discharge", font=(ff, fs), command=dp) 
    dp_BT.pack(side=tk.LEFT, padx='1')   
    terima_transfer_BT = tk.Button(rowButton_2_FR, text="tr-accept", font=(ff, fs), command=terima_transfer) 
    terima_transfer_BT.pack(side=tk.LEFT, padx='1')   
    ttv_BT = tk.Button(rowButton_2_FR, text="ttv", font=(ff, fs), command=ttv) 
    ttv_BT.pack(side=tk.LEFT, padx='1')  

    rowButton_3_FR = ttk.Frame(tab1)
    rowButton_3_FR.grid(row=24, column=0, padx=1, pady=1, sticky="w")  
    
    cppt_copy_BT = tk.Button(rowButton_3_FR, text="cppt-c", font=(ff, fs), command=lambda: cppt('c')) 
    cppt_copy_BT.pack(side=tk.LEFT, padx='1')    
    cppt_lapor_BT = tk.Button(rowButton_3_FR, text="cppt-l", font=(ff, fs), command=lambda: cppt('l')) 
    cppt_lapor_BT.pack(side=tk.LEFT, padx='1')  
    cppt_perawat_BT = tk.Button(rowButton_3_FR, text="cppt-p", font=(ff, fs), command=lambda: cppt('p')) 
    cppt_perawat_BT.pack(side=tk.LEFT, padx='1') 
    handover_BT = tk.Button(rowButton_3_FR, text="handover", font=(ff, fs), command=handover) 
    handover_BT.pack(side=tk.LEFT, padx='1') 

    rowButton_4_FR = ttk.Frame(tab1)
    rowButton_4_FR.grid(row=25, column=0, padx=1, pady=1, sticky="w")  
   
    diagnose_BT = tk.Button(rowButton_4_FR, text="Diagnose", font=(ff, fs), command=diagnose) 
    diagnose_BT.pack(side=tk.LEFT, padx='1')    
    reset_BT = tk.Button(rowButton_4_FR, text="Reset", font=(ff, fs), command=reset) 
    reset_BT.pack(side=tk.LEFT, padx='1')   
    redirectTotal_EN = modEntry(rowButton_4_FR, width=5, font=(ff, fs), placeholder='loop')
    redirectTotal_EN.pack(side=tk.LEFT, padx='1')   

    rowButton_5_FR = ttk.Frame(tab1)
    rowButton_5_FR.grid(row=26, column=0, padx=1, pady=1, sticky="w")  
 
    redirectTTV_BT = tk.Button(rowButton_5_FR, text="r-ttv", font=(ff, fs), command=lambda: redirect('ttv')) 
    redirectTTV_BT.pack(side=tk.LEFT, padx='1')    
    redirectCPPT_BT = tk.Button(rowButton_5_FR, text="r-cppt", font=(ff, fs), command=lambda: redirect('cppt')) 
    redirectCPPT_BT.pack(side=tk.LEFT, padx='1')    
    redirectDiagnose_BT = tk.Button(rowButton_5_FR, text="r-diagnose", font=(ff, fs), command=lambda: redirect('diagnose')) 
    redirectDiagnose_BT.pack(side=tk.LEFT, padx='1')    
    redirectHandOver_BT = tk.Button(rowButton_5_FR, text="r-handover", font=(ff, fs), command=lambda: redirect('handover')) 
    redirectHandOver_BT.pack(side=tk.LEFT, padx='1')   

    rowButton_6_FR = ttk.Frame(tab1)
    rowButton_6_FR.grid(row=27, column=0, padx=1, pady=1, sticky="w")  
 
    auto_dewasa_BT = tk.Button(rowButton_6_FR, text="auto-d", font=(ff, fs), command=lambda: automate('d')) 
    auto_dewasa_BT.pack(side=tk.LEFT, padx='1')    
    auto_geriatri_BT = tk.Button(rowButton_6_FR, text="auto-g", font=(ff, fs), command=lambda: automate('g')) 
    auto_geriatri_BT.pack(side=tk.LEFT, padx='1')    

    # Button for report and rx

    report_FR = ttk.Frame(tab2)
    report_FR.grid(row=0, column=1, padx=5, sticky="ew")   
    report_LB = tk.Label(report_FR, text='Lapor Pasien :', font=(ff, fs)) 
    report_LB.pack(side=tk.LEFT)   
    report_button = tk.Button(report_FR, width="8", text="compose", font=(ff, fs), command=report) 
    report_button.pack(side=tk.RIGHT) 
    report_copy_BT = tk.Button(report_FR, width="8", text="copy", font=(ff, fs), command=copy_report) 
    report_copy_BT.pack(side=tk.RIGHT)  
    report_EN = tk.Text(tab2, width=30, height=15) 
    report_EN.grid(row=1, column=1, padx=5, rowspan=9, sticky="nsew")  
 
    rx_FR = ttk.Frame(tab2)
    rx_FR.grid(row=10, column=1, padx=5, sticky="ew")   
    rx_LB = tk.Label(rx_FR, text='Resep :', font=(ff, fs)) 
    rx_LB.pack(side=tk.LEFT)   
    rx_BT = tk.Button(rx_FR, text="compose", width="8",  font=(ff, fs), command=rx) 
    rx_BT.pack(side=tk.RIGHT) 
    rx_copy_BT = tk.Button(rx_FR, text="copy", width="8",  font=(ff, fs), command=copy_rx) 
    rx_copy_BT.pack(side=tk.RIGHT)  
    rx_EN = tk.Text(tab2, width=30, height=10) 
    rx_EN.grid(row=11, column=1, padx=5, rowspan=10, sticky="nsew")   
  
    app.mainloop()
      
# Login GUI
root = tk.Tk()
root.title('?')
root.after(10000, root.destroy)
  
password_entry = tk.Entry(root, width='10', show="*")
password_entry.grid(row=0, column=0)
password_entry.focus_set()

submit = tk.Button(root, width='5', text='run', command=checkPassword)
submit.grid(row=0, column=1)

root.mainloop()