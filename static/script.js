document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', () => {

            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.content').forEach(c => c.classList.add('hidden'));

            tab.classList.add('active');
            document.getElementById(tab.dataset.tab).classList.remove('hidden');
        });
    });

    document.getElementById('audioToTextForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        const audioFile = document.getElementById('audioFile').files[0];

        if (!audioFile) {
            alert('Por favor, selecione um arquivo de áudio!');
            return;
        }

        formData.append('audio', audioFile);

        try {
            const response = await fetch('/api/transcribe/', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const data = await response.json();
                document.getElementById('audioToTextResult').innerText = `Transcrição: ${data.transcription}`;
            } else {
                const error = await response.json();
                alert(`Erro: ${error.error || 'Falha ao processar o arquivo.'}`);
            }
        } catch (err) {
            console.error(err);
            alert('Erro ao enviar o arquivo.');
        }
    });

    document.getElementById('textToAudioForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        const text = document.getElementById('textInput').value;
        const language = document.getElementById('languageSelect').value;

        if (!text.trim()) {
            alert('Por favor, insira o texto!');
            return;
        }

        formData.append('text', text);
        formData.append('language', language);

        try {
            const response = await fetch('/api/text-to-audio/', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const data = await response.json();
                const downloadLink = document.createElement('a');
                downloadLink.href = data.file_url;
                downloadLink.textContent = 'Baixar Áudio';
                document.getElementById('textToAudioResult').appendChild(downloadLink);
            } else {
                const error = await response.json();
                alert(`Erro: ${error.error || 'Falha ao processar o texto.'}`);
            }
        } catch (err) {
            console.error(err);
            alert('Erro ao enviar o texto.');
        }
    });
});
