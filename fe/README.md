# Vision Language POC

Simple proof-of-concept that provides a frontend to pick an image and upload it to a local server.

Run (PowerShell):

```powershell
cd "c:\Users\rohan\Coding\vision models\vision-language-poc"
npm install
npm start
# open http://localhost:3000 in a browser
```

What you get:
- A small UI at `/` to choose an image, preview it, and upload.
- Uploaded files are saved to an `uploads/` folder and served at `/uploads/<filename>`.

Next steps you might want:
- Wire this UI to your vision-language model backend to send the image for processing.
- Add size/type validation and authentication if required.
