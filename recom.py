import docx
from transformers import pipeline

# Fungsi untuk membaca konten dari file Word
def baca_dokumen_word(file_path):
    doc = docx.Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

# Fungsi untuk memecah teks menjadi bagian yang lebih kecil
def pecah_teks(teks, panjang_maksimal=512):
    kata_kata = teks.split()
    bagian_bagian = []
    bagian_sementara = []
    panjang_sementara = 0
    for kata in kata_kata:
        if panjang_sementara + len(kata) + 1 > panjang_maksimal:
            bagian_bagian.append(' '.join(bagian_sementara))
            bagian_sementara = [kata]
            panjang_sementara = len(kata) + 1
        else:
            bagian_sementara.append(kata)
            panjang_sementara += len(kata) + 1
    if bagian_sementara:
        bagian_bagian.append(' '.join(bagian_sementara))
    return bagian_bagian

# Load model pre-trained dari Hugging Face Transformers
summarizer = pipeline('summarization')
qa_model = pipeline('question-answering')

# Fungsi untuk memberikan rekomendasi berdasarkan laporan
def berikan_rekomendasi(teks_laporan):
    bagian_bagian = pecah_teks(teks_laporan)
    ringkasan_keseluruhan = []
    for bagian in bagian_bagian:
        ringkasan = summarizer(bagian, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
        ringkasan_keseluruhan.append(ringkasan)
    ringkasan_akhir = ' '.join(ringkasan_keseluruhan)

    # Menghasilkan rekomendasi perbaikan berdasarkan ringkasan
    rekomendasi_perbaikan = []
    pertanyaan_pertanyaan = [
        "Apa kerentanan yang ditemukan?",
        "Bagaimana cara memperbaiki kerentanan ini?",
        "Apa langkah-langkah pencegahan untuk masa depan?"
    ]
    for pertanyaan in pertanyaan_pertanyaan:
        jawaban = qa_model(question=pertanyaan, context=ringkasan_akhir)
        rekomendasi_perbaikan.append(f"{pertanyaan}: {jawaban['answer']}")

    rekomendasi = ' '.join(rekomendasi_perbaikan)
    return rekomendasi

# Contoh penggunaan
file_path = 'static analys panglima.docx'
teks_laporan = baca_dokumen_word(file_path)
rekomendasi = berikan_rekomendasi(teks_laporan)

print("Teks Laporan Pentest:")
print(teks_laporan)
print("\nRekomendasi Perbaikan:")
print(rekomendasi)
