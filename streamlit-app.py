import streamlit as st
import random

st.set_page_config(page_title="Generator Grup Angka", layout="centered")
st.title("🎲 Generator Grup Angka Acak")

# Input
group_count = st.number_input("Jumlah Grup", min_value=1, value=4)
custom_sizes_input = st.text_input("Ukuran Grup Kustom (pisah koma, total 100)", "")
separator = st.text_input("Pemisah Angka", value="*")
pembelian = st.number_input("Jumlah Pembelian", min_value=1, value=1)
mode = st.selectbox("Mode", ["Semua", "Ganjil", "Genap", "Pisah Ganjil/Genap"])
apply_bonus = st.checkbox("Gunakan Bonus -5000")

if st.button("Generate"):
    try:
        # Validasi ukuran kustom
        if custom_sizes_input:
            sizes = list(map(int, custom_sizes_input.split(",")))
            if sum(sizes) != 100:
                st.error("Total angka harus 100.")
                st.stop()
            if len(sizes) != group_count:
                st.error("Jumlah grup tidak sesuai dengan ukuran grup kustom.")
                st.stop()
        else:
            base = 100 // group_count
            sizes = [base] * group_count
            for i in range(100 % group_count):
                sizes[i] += 1

        # Generate angka sesuai mode
        numbers = [f"{i:02d}" for i in range(100)]
        if mode == "Ganjil":
            numbers = [n for n in numbers if int(n) % 2 == 1]
        elif mode == "Genap":
            numbers = [n for n in numbers if int(n) % 2 == 0]
        elif mode == "Pisah Ganjil/Genap":
            ganjil = [n for n in numbers if int(n) % 2 == 1]
            genap = [n for n in numbers if int(n) % 2 == 0]
            numbers = random.sample(ganjil, len(ganjil)) + random.sample(genap, len(genap))

        if len(numbers) < 100:
            st.error("Angka tersedia kurang dari 100 untuk mode ini.")
            st.stop()

        random.shuffle(numbers)
        harga_per_angka = 710
        start = 0
        total = 0
        output = ""

        for i, size in enumerate(sizes):
            group = numbers[start:start+size]
            start += size
            harga = len(group) * pembelian * harga_per_angka
            if apply_bonus:
                harga = max(0, harga - 5000)
            output += f"Grup {i+1}: {separator.join(group)}\n"
            output += f"Total Harga Grup {i+1}: Rp{harga:,}{' (BONUS -5000)' if apply_bonus else ''}\n\n"
            total += harga

        output += f"Total Keseluruhan: Rp{total:,}"
        st.text_area("Hasil", output, height=300)
        st.download_button("Download Hasil (.txt)", output, file_name="hasil_generator.txt")

    except Exception as e:
        st.error(f"Error: {str(e)}")
