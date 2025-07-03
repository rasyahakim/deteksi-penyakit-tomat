import streamlit as st
from datetime import datetime
from pathlib import Path
from PIL import Image
import settings
import helper
from collections import Counter
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Deteksi Penyakit Tomat",
    page_icon="🍅",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "detection_history" not in st.session_state:
    st.session_state.detection_history = []

st.sidebar.title("🍅 Deteksi Penyakit Tomat")
page = st.sidebar.radio("Select Menu", ["🏠Beranda", "🔍 Deteksi", "📜Riwayat"])


CONFIDENCE = 0.25
model_path = Path(settings.DETECTION_MODEL)
try:
    model = helper.load_model(model_path)
except Exception as ex:
    st.error(f"Gagal load model: {model_path}")
    st.error(ex)

penjelasan_kelas = {
    "Anthracnose": "Penyakit jamur yang menyebabkan bintik gelap melingkar.",
    "Bacterial_Spot": "Penyakit bakteri yang menyebabkan bercak cokelat pada daun dan buah.",
    "Blossom end rot": "Penyakit fisiologis ditandai dengan area gelap di ujung bawah tomat.",
    "Healthy Tomato": "Tomat sehat tanpa gejala penyakit.",
    "Spotted wilt Virus": "Penyakit virus yang menyebabkan belang pada daun dan buah."
}

def label_warna(conf):
    if conf < 0.5:
        return "🔴"
    elif conf < 0.8:
        return "🟡"
    else:
        return "🟢"

def simpan_riwayat(img, result_img, boxes):
    labels = []
    for box in boxes:
        cls = int(box.cls[0])
        nama_kelas = model.names[cls]
        labels.append(nama_kelas)
    st.session_state.detection_history.append({
        "original_image": img.copy(),
        "result_image": result_img,
        "labels": labels,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

if page == "🏠Beranda":
    st.title("Selamat Datang di Aplikasi Deteksi Penyakit Pada Permukaan Buah Tomat 🍅")
    col1, col2 = st.columns(2)

    with col1:
        st.image("images/tomatsegar.jpg", use_container_width=True)
        
    with col2:
        st.image("images/tomatsakit.jpg", use_container_width=True)


    st.write("""
        Aplikasi ini dirancang untuk mendeteksi penyakit pada permukaan buah tomat menggunakan model deep learning YOLOv11. 
        Deteksi penyakit pada tomat merupakan tantangan karena beberapa faktor. 
        Pertama, gejala visual seperti bercak atau perubahan warna sering kali serupa antar jenis penyakit, sehingga sulit dibedakan secara akurat hanya dengan pengamatan mata. 
        Kedua, kondisi pencahayaan dan latar belakang gambar yang bervariasi dapat memengaruhi akurasi deteksi. 
        Ketiga, variasi bentuk dan ukuran buah tomat pada setiap tahap pertumbuhan juga menambah kompleksitas dalam proses identifikasi.
        Selain itu, penggunaan teknologi deteksi seperti YOLOv11 membutuhkan dataset yang besar dan representatif agar mampu mengenali berbagai jenis penyakit secara konsisten. 
        Tantangan lainnya adalah mengintegrasikan model ke dalam aplikasi web yang mudah digunakan oleh petani maupun pengguna umum tanpa latar belakang teknis. Oleh karena itu, pengembangan aplikasi ini tidak hanya mengandalkan kecanggihan model deteksi, tetapi juga mempertimbangkan aspek antarmuka pengguna, performa sistem, serta kemudahan akses untuk mendukung penerapan teknologi ini di bidang pertanian secara nyata.
    """)
    st.title("Jenis Penyakit pada Permukaan Buah Tomat")
    st.write(""" 
        Tanaman tomat rentan terhadap berbagai jenis penyakit yang menyerang permukaan buah, 
        yang dapat menurunkan kualitas dan nilai jual hasil panen. 
        Setiap jenis penyakit seperti bercak daun, busuk buah, dan jamur abu memiliki gejala khas yang penting dikenali. 
        Memahami karakteristik visual dari masing-masing penyakit sangat penting 
        untuk pengambilan keputusan dalam proses penanganan, pengendalian, hingga pemanenan buah tomat yang sehat.
    """)
    # Using columns layout for images and descriptions
    col3, col4 = st.columns([1, 2])
        
    with col3:
        st.image("images/tomanthracnose.jpg", caption="Anthracnose", use_container_width=True)
    with col4:
        st.write("""
        ### Anthracnose
        Anthracnose adalah penyakit pada tomat yang disebabkan oleh jamur *Colletotrichum* spp. 
        Ciri utamanya adalah munculnya bercak bulat kecil berwarna gelap pada permukaan buah, 
        yang kemudian membesar dan menjadi cekung di bagian tengahnya. 
        Permukaan bercak sering kali tampak berair atau lembek, terutama pada buah yang sudah matang. 
        Penyakit ini berkembang pesat di kondisi lembap dan basah, serta dapat menyebabkan kerusakan serius 
        pada hasil panen jika tidak ditangani dengan baik.
        """)

    col5, col6 = st.columns([1, 2])
        
    with col5:
        st.image("images/bacterialspot.jpeg", caption="Bacterial Spot", use_container_width=True)
    with col6:
        st.write("""
        ### Bacterial Spot
        Bacterial Spot adalah penyakit yang disebabkan oleh bakteri *Xanthomonas campestris* pv. *vesicatoria*. 
        Penyakit ini ditandai dengan munculnya bercak kecil berwarna cokelat tua atau hitam di permukaan buah, 
        sering kali dikelilingi oleh lingkaran kuning. 
        Bercak dapat berkembang menjadi luka yang agak cekung dan menyebabkan permukaan buah tampak kasar atau pecah. 
        Infeksi ini umum terjadi pada kondisi panas dan lembap, dan dapat menyebar dengan cepat melalui percikan air hujan atau alat pertanian yang terkontaminasi.
        """)
    
    col7, col8 = st.columns([1, 2])
        
    with col7:
        st.image("images/blosomendrot.jpeg", caption="Blossom End Rot", use_container_width=True)
    with col8:
        st.write("""
        ### Blossom End Rot
        Blossom End Rot adalah gangguan fisiologis pada tomat yang ditandai dengan bercak gelap dan cekung di bagian bawah buah (ujung bunga). 
        Awalnya muncul sebagai noda kecil berair, kemudian membesar dan menjadi berwarna cokelat hingga hitam. 
        Permukaan yang terkena terasa kering dan keras. Penyebab utamanya adalah kekurangan kalsium pada buah, 
        sering kali diperparah oleh fluktuasi kelembapan tanah atau ketidakseimbangan nutrisi. 
        Meski bukan penyakit menular, kondisi ini dapat mengurangi kualitas dan daya jual tomat secara signifikan.
        """)
    
    col9, col10 = st.columns([1, 2])
        
    with col9:
        st.image("images/virustomat.jpg", caption="Spotted Wilt Virus", use_container_width=True)
    with col10:
        st.write("""
        ### Spotted Wilt Virus (TSWV)
        Spotted Wilt Virus (TSWV) adalah penyakit yang disebabkan oleh virus dan ditularkan oleh serangga thrips. 
        Gejalanya meliputi bercak nekrotik (kehitaman) melingkar di permukaan buah, yang sering disertai perubahan warna menjadi kekuningan hingga kecokelatan.
        Buah yang terinfeksi bisa mengalami deformasi bentuk dan berhenti berkembang, serta kualitasnya menurun drastis. 
        Selain pada buah, virus ini juga dapat menyebabkan daun menggulung, kerdil, dan munculnya garis-garis ungu pada batang. 
        Penyakit ini sangat merugikan dan sulit dikendalikan jika penyebarannya sudah luas.
        """)


elif page == "🔍 Deteksi":
    st.title("Deteksi Penyakit Pada Permukaan Buah Tomat")
    mode = st.sidebar.radio("Pilih metode input gambar:", ["Upload Gambar", "Kamera Langsung"])

    if mode == "Upload Gambar":
        uploaded_file = st.file_uploader("Pilih gambar...", type=["jpg", "jpeg", "png", "bmp", "webp"])
        if uploaded_file:
            image = Image.open(uploaded_file)
            results = model.predict(image, conf=CONFIDENCE)
            boxes = results[0].boxes
            result_img = results[0].plot()[:, :, ::-1]

            col1, col2 = st.columns(2)
            with col1:
                st.image(image, caption="Gambar Asli", use_container_width=True)
            with col2:
                st.image(result_img, caption="Hasil Deteksi", use_container_width=True)

            st.markdown("### 🧪 Hasil Deteksi")
            label_sudah_ditampilkan = set()
            for box in boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                nama_kelas = model.names[cls]
                if nama_kelas not in label_sudah_ditampilkan:
                    label_sudah_ditampilkan.add(nama_kelas)
                    warna = label_warna(conf)
                    st.markdown(f"**{warna} {nama_kelas}** ({conf*100:.2f}%)")
                    st.success(penjelasan_kelas.get(nama_kelas, "Tidak ada penjelasan."))

            simpan_riwayat(image, result_img, boxes)

    elif mode == "Kamera Langsung":
        image_file = st.camera_input("Ambil foto dengan kamera")
        if image_file:
            image = Image.open(image_file)
            results = model.predict(image, conf=CONFIDENCE)
            boxes = results[0].boxes
            result_img = results[0].plot()[:, :, ::-1]

            col1, col2 = st.columns(2)
            with col1:
                st.image(image, caption="Gambar Kamera", use_container_width=True)
            with col2:
                st.image(result_img, caption="Hasil Deteksi", use_container_width=True)

            st.markdown("### 🧪 Hasil Deteksi")
            label_sudah_ditampilkan = set()
            for box in boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                nama_kelas = model.names[cls]
                if nama_kelas not in label_sudah_ditampilkan:
                    label_sudah_ditampilkan.add(nama_kelas)
                    warna = label_warna(conf)
                    st.markdown(f"**{warna} {nama_kelas}** ({conf*100:.2f}%)")
                    st.success(penjelasan_kelas.get(nama_kelas, "Tidak ada penjelasan."))

            simpan_riwayat(image, result_img, boxes)

elif page == "📜Riwayat":
    st.title("📑 Riwayat Deteksi")

    if st.session_state.detection_history:
        # Ambil semua label dari history
        all_labels = []
        for record in st.session_state.detection_history:
            all_labels.extend(record.get("labels", []))

        if all_labels:
            st.markdown(
                "<h4 style='text-align: center;'>📊 Ringkasan Deteksi (Pie Chart)</h4>",
                unsafe_allow_html=True
            )

            counter = Counter(all_labels)
            labels = list(counter.keys())
            sizes = list(counter.values())

            # Gunakan kolom agar pie chart berada di tengah
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                fig, ax = plt.subplots(figsize=(2.5, 2.5), dpi=150)
                ax.pie(
                    sizes,
                    labels=labels,
                    autopct='%1.1f%%',
                    startangle=90,
                    textprops={'fontsize': 6}
                )
                ax.axis("equal")
                st.pyplot(fig, use_container_width=False)
        else:
            st.info("Belum ada label yang terbaca dari hasil deteksi.")

        # Tampilkan detail riwayat
        for i, record in enumerate(st.session_state.detection_history, 1):
            st.markdown(f"### Deteksi ke-{i} - {record['timestamp']}")
            col1, col2 = st.columns(2)
            with col1:
                st.image(record["original_image"], caption="Gambar Asli", use_container_width=True)
            with col2:
                st.image(record["result_image"], caption="Hasil Deteksi", use_container_width=True)
            with st.expander("Detail Deteksi"):
                for label in record.get("labels", []):
                    st.write(f"✅ {label}")

        if st.button("🗑️ Hapus Semua Riwayat", type="primary"):
            st.session_state.detection_history.clear()
            st.success("Riwayat berhasil dihapus.")
            st.rerun()
    else:
        st.info("Belum ada riwayat deteksi pada sesi ini.")

