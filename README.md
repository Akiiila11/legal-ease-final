# LegalEase single-service deployment

Deploy this folder as one Render Python web service.

- Build command: `pip install -r requirements-render.txt`
- Start command: `streamlit run streamlit_app.py --server.address 0.0.0.0 --server.port $PORT`
- Environment variable: `GOOGLE_API_KEY` with your Gemini API key

This version runs Streamlit, Gemini generation, document creation, and downloads in one service. It does not use `API_BASE`, FastAPI, or a separate backend service.
