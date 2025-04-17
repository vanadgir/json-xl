# JSON-XL

Web application for converting JSON into downloadable Excel files

- HTML/CSS/JS
- FastAPI
- XlsxWriter

To set up server:

```bash
cd server
make venv # (to create virtual env)
make install # (to install Python dependencies)
make run # (to start FastAPI server)
```

To set up client:

```bash
cd client
make install # (to install npm dependencies)
make run # (to start Vite dev server)
```