import re
import string
import random
from difflib import SequenceMatcher

class ProfitPal:
    def __init__(self):
        # Keywords untuk setiap intent
        self.intents = {
            'greeting': ['halo', 'hai', 'hi', 'selamat', 'assalamualaikum', 'pagi', 'siang', 'malam'],
            'about_bot': ['siapa', 'nama', 'kamu', 'bot', 'anda'],
            'start_investment': ['mulai', 'awal', 'pemula', 'belajar', 'start', 'cara'],
            'investment_types': ['jenis', 'macam', 'pilihan', 'tipe', 'kategori', 'apa'],
            'mutual_funds': ['reksadana', 'reksa', 'dana', 'mutual', 'fund'],
            'stocks': ['saham', 'stock', 'bursa', 'trading', 'beli', 'jual'],
            'gold': ['emas', 'gold', 'logam', 'mulia'],
            'minimum_capital': ['modal', 'uang', 'minimum', 'berapa', 'butuh'],
            'platforms': ['aplikasi', 'platform', 'dimana', 'app', 'tempat'],
            'risk': ['risiko', 'rugi', 'bahaya', 'aman', 'risk', 'berbahaya'],
            'profit': ['untung', 'profit', 'return', 'gain', 'hasil', 'keuntungan'],
            'timing': ['kapan', 'waktu', 'lama', 'jangka', 'tenor'],
            'thanks': ['terima', 'kasih', 'makasih', 'thanks'],
            'goodbye': ['selesai', 'keluar', 'bye', 'sampai', 'jumpa', 'exit'],
            'help': ['help', 'bantuan', 'contoh', 'panduan', 'petunjuk']
        }
        
        # Responses untuk setiap intent
        self.responses = {
            'greeting': [
                "Hai! Saya ProfitPal, sahabat investasi terpercaya Anda. Ada yang ingin ditanyakan?",
                "Selamat datang di ProfitPal! Saya akan membantu Anda meraih profit melalui investasi cerdas. Silakan bertanya!",
                "Halo! Mari kita mulai perjalanan profit Anda bersama ProfitPal. Ada yang mau dipelajari hari ini?"
            ],
            'about_bot': [
                "Saya ProfitPal, sahabat investasi yang membantu pemula meraih profit dengan investasi cerdas!",
                "Saya adalah ProfitPal, chatbot konsultan investasi terpercaya. Tujuan saya membantu Anda memulai investasi yang menguntungkan!"
            ],
            'start_investment': [
                "Untuk pemula, mulai dengan reksadana pasar uang atau emas digital. Modal bisa dari 10ribu saja!",
                "Langkah awal: 1) Tentukan tujuan investasi 2) Pilih jenis investasi sesuai profil risiko 3) Mulai dengan modal kecil",
                "Investasi pemula terbaik: Reksadana pasar uang (risiko rendah) atau emas (hedge inflasi). Mulai sekarang!",
                "Jangan takut mulai! Warren Buffett bilang: 'Seseorang duduk di bawah pohon hari ini karena menanamnya kemarin.'"
            ],
            'investment_types': [
                "Ada reksadana, saham, emas, obligasi, deposito, P2P lending. Mana yang mau dipelajari lebih lanjut?",
                "Jenis investasi: 1) Reksadana (pemula) 2) Saham (advanced) 3) Emas (konservatif) 4) Obligasi (stabil)"
            ],
            'mutual_funds': [
                "Reksadana cocok untuk pemula. Risiko lebih rendah karena dikelola manajer investasi profesional.",
                "Reksadana: uang Anda dikelola profesional, diversifikasi otomatis, modal mulai 10ribu. Cocok untuk pemula!"
            ],
            'stocks': [
                "Saham return tinggi tapi risiko tinggi. Pelajari analisis fundamental dulu sebelum beli saham.",
                "Investasi saham butuh riset mendalam. Mulai dari blue chip, pahami laporan keuangan perusahaan."
            ],
            'gold': [
                "Emas bagus untuk hedge inflasi. Bisa beli emas digital mulai dari 0.01 gram di aplikasi.",
                "Emas stabil dan tahan inflasi. Sekarang bisa investasi emas digital tanpa ribet simpan fisik."
            ],
            'minimum_capital': [
                "Modal investasi bisa mulai dari 10ribu! Reksadana dan emas digital paling terjangkau untuk pemula.",
                "Gak perlu modal besar. Reksadana mulai 10rb, emas digital 1rb, saham 100rb. Yang penting konsisten!"
            ],
            'platforms': [
                "Platform terpercaya: Bibit, Bareksa (reksadana), Stockbit, IPOT (saham), Pegadaian Digital (emas).",
                "Aplikasi investasi: Bibit, Ajaib, Bareksa untuk reksadana. Stockbit, Mirae Asset untuk saham."
            ],
            'risk': [
                "Semua investasi ada risiko. Yang penting diversifikasi dan jangan invest uang yang dibutuhkan sehari-hari.",
                "Prinsip investasi: high risk high return. Kelola risiko dengan diversifikasi dan jangan pakai uang darurat."
            ],
            'profit': [
                "Return investasi bervariasi: Deposito 3-6%, Reksadana 8-15%, Saham bisa 15%+ per tahun.",
                "Keuntungan investasi: Reksadana pasar uang 4-7%, campuran 8-12%, saham 10-20% annually."
            ],
            'timing': [
                "Investasi jangka panjang (5+ tahun) lebih menguntungkan karena efek compound interest.",
                "Waktu terbaik investasi: SEKARANG! Time in market beats timing the market. Mulai sekarang, konsisten.",
                "Einstein bilang compound interest adalah keajaiban dunia ke-8. Mulai investasi sedini mungkin!",
                "Rumus sukses investasi: Mulai Muda + Konsisten + Sabar = Kaya Raya di masa depan!"
            ],
            'thanks': [
                "Sama-sama! ProfitPal senang bisa membantu. Ingat: mulai investasi sekarang, konsisten, dan raih profit impian!",
                "Senang bisa membantu! Jangan lupa mulai investasi dari sekarang bersama ProfitPal, sekecil apapun modalnya."
            ],
            'goodbye': [
                "Terima kasih sudah konsultasi dengan ProfitPal! Semangat meraih profit melalui investasi cerdas!",
                "Sampai jumpa! Ingat: investasi terbaik adalah edukasi diri. Terus belajar bersama ProfitPal dan sukses selalu!"
            ],
            'help': [
                "📋 Contoh pertanyaan untuk ProfitPal:\n• 'cara mulai investasi'\n• 'berapa modal minimum'\n• 'aplikasi investasi yang bagus'\n• 'apa itu reksadana'\n• 'investasi emas gimana'\n• 'risiko investasi saham'",
                "🔍 ProfitPal bisa menjawab tentang:\n✅ Jenis-jenis investasi\n✅ Modal minimum\n✅ Platform/aplikasi investasi\n✅ Tips untuk pemula\n✅ Manajemen risiko\n✅ Waktu yang tepat investasi"
            ],
            'default': [
                "Maaf, ProfitPal belum memahami pertanyaan itu. Bisa tanya tentang jenis investasi, cara mulai, atau platform investasi?",
                "ProfitPal belum paham pertanyaan Anda. Coba tanya tentang: reksadana, saham, emas, modal minimum, atau aplikasi investasi.",
                "Hmm, saya butuh bantuan untuk memahami itu. Coba tanya: 'cara mulai investasi' atau 'aplikasi investasi yang bagus'?",
                "Belum paham nih! Ketik 'help' untuk melihat contoh pertanyaan yang bisa ditanyakan ke ProfitPal."
            ]
        }
    
    def preprocess_text(self, text):
        """Preprocessing: lowercase, remove punctuation, tokenize"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Tokenize (split into words)
        tokens = text.split()
        
        return tokens
    
    def calculate_similarity(self, text1, text2):
        """Calculate similarity between two texts"""
        return SequenceMatcher(None, text1, text2).ratio()
    
    def detect_intent(self, user_input):
        """Detect user intent based on keywords"""
        tokens = self.preprocess_text(user_input)
        
        intent_scores = {}
        
        # Check each intent
        for intent, keywords in self.intents.items():
            score = 0
            
            # Check if any keyword matches
            for token in tokens:
                for keyword in keywords:
                    # Exact match gets higher score
                    if token == keyword:
                        score += 1
                    # Partial match with similarity
                    elif self.calculate_similarity(token, keyword) > 0.8:
                        score += 0.5
            
            intent_scores[intent] = score
        
        # Return intent with highest score
        if max(intent_scores.values()) > 0:
            return max(intent_scores, key=intent_scores.get)
        else:
            return 'default'
    
    def get_response(self, intent):
        """Get response based on detected intent with emoji enhancement"""
        # Emoji collection for different intents
        emoji_map = {
            'greeting': ["👋", "😊", "🤝", "✨", "🌟"],
            'about_bot': ["🤖", "💼", "🎯", "✨", "🤝"],
            'start_investment': ["🚀", "💡", "📈", "🎯", "💰"],
            'investment_types': ["📊", "💎", "🔍", "💡", "📈"],
            'mutual_funds': ["📊", "🏦", "💼", "✅", "🎯"],
            'stocks': ["📈", "⚡", "🎢", "💹", "🔍"],
            'gold': ["🥇", "💎", "✨", "🏆", "💰"],
            'minimum_capital': ["💰", "🪙", "💡", "✅", "🎯"],
            'platforms': ["📱", "💻", "🏦", "✅", "🔗"],
            'risk': ["⚖️", "🛡️", "⚠️", "💡", "🎯"],
            'profit': ["💰", "📈", "🎯", "💎", "🏆"],
            'timing': ["⏰", "📅", "🎯", "💡", "🚀"],
            'thanks': ["😊", "🤝", "❤️", "🙏", "✨"],
            'goodbye': ["👋", "🌟", "🚀", "💫", "🤝"],
            'help': ["📋", "💡", "🔍", "📚", "❓"],
            'default': ["🤔", "💭", "❓", "💡", "🔍"]
        }
        
        # Get random emoji for the intent
        emojis = emoji_map.get(intent, ["💡"])
        selected_emoji = random.choice(emojis)
        
        # Get random response
        response = random.choice(self.responses[intent])
        
        return f"{selected_emoji} {response}"
    
    def chat(self, user_input):
        """Main chat function with enhanced error handling"""
        try:
            # Validate input
            if not user_input or user_input.strip() == "":
                return "🤔 Sepertinya Anda belum mengetik apa-apa. Silakan tanya tentang investasi!"
            
            # Check for very long input
            if len(user_input) > 500:
                return "😅 Pertanyaan terlalu panjang! Coba persingkat pertanyaan Anda tentang investasi."
            
            # Detect intent and get response
            intent = self.detect_intent(user_input)
            response = self.get_response(intent)
            
            # Log interaction (simple counter)
            if not hasattr(self, 'interaction_count'):
                self.interaction_count = 0
            self.interaction_count += 1
            
            return response
            
        except Exception as e:
            return f"🔧 Maaf, terjadi kesalahan teknis. ProfitPal sedang maintenance. Coba lagi ya!"
    
    def get_chat_statistics(self):
        """Get basic chat statistics"""
        return getattr(self, 'interaction_count', 0)

# Demo function for presentation
def run_demo():
    """Demo mode untuk presentasi otomatis"""
    bot = ProfitPal()
    
    print("🎬 DEMO MODE - ProfitPal Automatic Demo")
    print("=" * 55)
    
    demo_conversations = [
        ("halo profitpal", "Greeting - Menyapa bot"),
        ("siapa kamu", "About Bot - Mengenal ProfitPal"),
        ("saya mau mulai investasi", "Start Investment - Panduan pemula"),
        ("berapa modal minimum", "Minimum Capital - Info modal"),
        ("aplikasi apa yang bagus", "Platform - Rekomendasi apps"),
        ("apa itu reksadana", "Mutual Funds - Edukasi produk"),
        ("investasi saham gimana", "Stocks - Info saham"),
        ("bahaya tidak investasi", "Risk - Manajemen risiko"),
        ("terima kasih ya", "Thanks - Apresiasi"),
        ("sampai jumpa", "Goodbye - Penutup")
    ]
    
    for i, (user_input, description) in enumerate(demo_conversations, 1):
        print(f"\n[Demo {i}/10] {description}")
        print(f"User: {user_input}")
        response = bot.chat(user_input)
        print(f"ProfitPal: {response}")
        
        # Pause untuk readability
        import time
        time.sleep(1.5)
    
    print(f"\n🎉 Demo selesai! ProfitPal berhasil menjawab {len(demo_conversations)} pertanyaan dengan sempurna!")

def show_statistics():
    """Tampilkan statistik ProfitPal"""
    bot = ProfitPal()
    
    total_intents = len(bot.intents)
    total_keywords = sum(len(keywords) for keywords in bot.intents.values())
    total_responses = sum(len(responses) for responses in bot.responses.values())
    
    print("📊 PROFITPAL STATISTICS")
    print("=" * 30)
    print(f"🎯 Total Intent Categories: {total_intents}")
    print(f"🔑 Total Keywords: {total_keywords}")
    print(f"💬 Total Unique Responses: {total_responses}")
    print(f"🧠 NLP Features: Preprocessing, Tokenization, Similarity Matching")
    print(f"✨ Special Features: Emoji Enhancement, Fallback Handling, Error Management")
    print(f"🚀 Version: 1.0 | Built with Python & Love")
    print("=" * 30)

# Enhanced main program
def main():
    print("=" * 55)
    print("🤝 PROFITPAL - Your Trusted Investment Buddy")
    print("=" * 55)
    print("Smart investing made simple, profits made possible!")
    print("Developed by: [Your Name] | NLP-Based Chatbot")
    print("\n📋 Menu Options:")
    print("1. Chat dengan ProfitPal")
    print("2. Demo Mode (Presentasi)")
    print("3. Lihat Statistik")
    print("4. Keluar")
    
    while True:
        choice = input("\nPilih menu (1-4): ").strip()
        
        if choice == "1":
            # Normal chat mode
            bot = ProfitPal()
            print("\n🤝 Mode Chat Aktif - Mulai berbicara dengan ProfitPal!")
            print("Ketik 'menu' untuk kembali ke menu utama.\n")
            
            while True:
                user_input = input("Anda: ")
                
                if user_input.lower() in ['keluar', 'exit', 'quit', 'bye']:
                    print("ProfitPal: 👋 Terima kasih sudah chat dengan ProfitPal! Semangat meraih profit melalui investasi! 🚀💰")
                    break
                elif user_input.lower() == 'menu':
                    print("🔄 Kembali ke menu utama...\n")
                    break
                
                response = bot.chat(user_input)
                print(f"ProfitPal: {response}\n")
        
        elif choice == "2":
            # Demo mode
            print("\n" + "="*55)
            run_demo()
            input("\nTekan Enter untuk kembali ke menu...")
        
        elif choice == "3":
            # Statistics
            print("\n" + "="*55)
            show_statistics()
            input("\nTekan Enter untuk kembali ke menu...")
        
        elif choice == "4":
            print("\n🚀 Terima kasih telah menggunakan ProfitPal!")
            print("💡 Remember: The best time to invest was yesterday, the second best time is now!")
            break
        
        else:
            print("❌ Pilihan tidak valid. Silakan pilih 1-4.")

if __name__ == "__main__":
    main()