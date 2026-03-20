const fileInput = document.getElementById('fileInput');
const preview = document.getElementById('preview');
const previewContainer = document.getElementById('previewContainer');
const uploadBtn = document.getElementById('uploadBtn');
const status = document.getElementById('status');

let selectedFile = null;

fileInput.addEventListener('change', (e) => {
  const file = e.target.files && e.target.files[0];
  if (!file) {
    preview.style.display = 'none';
    uploadBtn.disabled = true;
    selectedFile = null;
    return;
  }

  selectedFile = file;
  const reader = new FileReader();
  reader.onload = (ev) => {
    preview.src = ev.target.result;
    preview.style.display = 'block';
  };
  reader.readAsDataURL(file);
  uploadBtn.disabled = false;
  status.textContent = '';
});

uploadBtn.addEventListener('click', async () => {
  if (!selectedFile) return;
  uploadBtn.disabled = true;
  status.textContent = 'Uploading...';

  const fd = new FormData();
  fd.append('image', selectedFile);

  try {
    const res = await fetch('/upload', { method: 'POST', body: fd });
    if (!res.ok) throw new Error('Upload failed');
    const data = await res.json();
    status.innerHTML = `Uploaded: <a href="${data.url}" target="_blank">${data.filename}</a>`;

    // Call backend FastAPI analyze endpoint
    status.textContent = 'Analyzing image...';
    const analyzeRes = await fetch('http://localhost:8000/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ filename: data.filename, prompt: 'What are the items that can be picked up by the robot?' })
    });
    if (!analyzeRes.ok) {
      const errData = await analyzeRes.json();
      throw new Error(errData.detail || 'Analysis failed');
    }

    const analyzeData = await analyzeRes.json();
    status.innerHTML = `Uploaded: <a href="${data.url}" target="_blank">${data.filename}</a><br><strong>Vision response:</strong> ${analyzeData.response}`;
  } catch (err) {
    console.error(err);
    status.textContent = 'Upload or analysis failed. See console for details.';
  } finally {
    uploadBtn.disabled = false;
  }
});
