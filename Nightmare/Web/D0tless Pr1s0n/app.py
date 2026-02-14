from flask import Flask, request, render_template, render_template_string

app = Flask(__name__)
app.secret_key = "0xaskar_secret_nightmare"

def check_blacklist(text):

    blacklist = ['.', '_', '|join', '[', ']', 'mro', 'base']
    found_words = []
    for word in blacklist:
        if word in text.lower():
            found_words.append(word)
    return found_words

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name', '')
        job = request.form.get('job', '')
        
        combined_input = (name + job).lower()
        forbidden_found = check_blacklist(combined_input)

        if forbidden_found:
            words_str = ", ".join([f"'{w}'" for w in forbidden_found])
            error_msg = f"0xaskar says: 🛑 Nice try! (Detected: {words_str})"
            return render_template('index.html', error=error_msg)

        card_template = f"""
        <html>
        <head><script src="https://cdn.tailwindcss.com"></script></head>
        <body class="bg-[#0a0a0a] flex items-center justify-center min-h-screen">
            <div class="p-1 rounded-xl bg-gradient-to-r from-green-500 to-emerald-900 shadow-2xl">
                <div class="bg-black p-8 rounded-lg w-80 text-white border border-white/10">
                    <div class="flex justify-between items-start mb-8">
                        <div class="h-10 w-10 border-2 border-green-500 rounded-full flex items-center justify-center font-bold text-green-500 font-mono">0x</div>
                        <div class="text-[10px] text-gray-500 text-right uppercase tracking-widest">Official<br>Employee Card</div>
                    </div>
                    <h2 class="text-2xl font-bold mb-1 tracking-tight text-white font-sans">{name}</h2>
                    <p class="text-green-500 text-sm mb-6 font-mono tracking-tighter">{job}</p>
                    <div class="flex items-center gap-2">
                        <div class="h-1 w-12 bg-green-500"></div>
                        <div class="text-[8px] text-gray-600 uppercase">Authenticated by 0xaskar</div>
                    </div>
                </div>
            </div>
            <div class="fixed bottom-10"><a href="/" class="text-green-500 hover:underline font-mono">← Back to Console</a></div>
        </body>
        </html>
        """
        return render_template_string(card_template)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8989)
