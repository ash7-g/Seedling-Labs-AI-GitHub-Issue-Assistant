# AI-Powered GitHub Issue Assistant


---

# 📦 **Installation & Setup**

This project includes both a **FastAPI backend** and a **Streamlit frontend**, and can be run either:

* ⚡ **Using Docker (recommended — under 5 minutes)**
* 🛠️ **Manually (Python venv)**

Below are simple, reliable instructions for both.

------------------------------------------------------------------

# 🐳 **Option 1: Run with Docker (Recommended)**

This is the fastest and most reliable setup.
You **do not** need to install Python or any dependencies.

----------------------------------------------------------------

## **1️⃣ Clone the repository**

```bash

git clone https://github.com/ash7-g/Seedling-Labs-AI-GitHub-Issue-Assistant.git
cd Seedling-Labs-AI-GitHub-Issue-Assistant

```
---
## **2️⃣ Configure environment variables**

The backend reads API keys from:

```bash

backend/.env

```

# 🤖 **Get your OpenAI API Key (for GPT models)**

Create an API key from your OpenAI account:

👉 [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)

Steps:

1. Log in to OpenAI
2. Go to **API Keys**
3. Click **Create new secret key**
4. Copy the key

Add it to the backend `.env` file:

```
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4.1     # or gpt-4.1-mini, gpt-4.1-preview
```

If your backend uses a different default model, update accordingly.


# 🐙  Get your GitHub Token (to avoid rate limits)

GitHub’s API limits unauthenticated requests.
Create a lightweight token here:

👉 [https://github.com/settings/tokens](https://github.com/settings/tokens)

Steps:

1. Click **Generate new token (classic)**
2. Select only **public_repo**
3. Copy the token

Add it to `.env`:

```
GITHUB_TOKEN=your_github_pat_here
```

```bash

OPENAI_API_KEY=your_openai_key_here
GITHUB_TOKEN=your_github_pat_here   # optional, prevents GitHub rate-limit
OPENAI_MODEL=gpt-4.1

```

**✔ Docker Compose automatically loads this file into the backend container.**
**✔ No extra steps needed.**

---

## **3️⃣ Build and start the entire app**

```bash

docker compose up --build

```

This launches:

| Service              | Port     | Description                           |
| -------------------- | -------- | ------------------------------------- |
| Backend (FastAPI)    | **8000** | Handles GitHub fetching + AI analysis |
| Frontend (Streamlit) | **8501** | User interface                        |

---

## **4️⃣ Open the app**

Open your browser:

🔗 **Frontend:**
[http://localhost:8501](http://localhost:8501)

🔗 **Backend API docs:**
[http://localhost:8000/docs](http://localhost:8000/docs)

---

## **5️⃣ Stop containers**

```bash
docker compose down
```

---

## **6️⃣ (Optional) Remove cache/images**

```bash
docker system prune -af
```

-----------------------------------------------------------------------


## 🐍 Option 2: Manual Installation (Python)

Use this method if you prefer running backend + frontend separately.

-----------------------------------------------------------------------

## 🛠 Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate    # Windows
# or source venv/bin/activate on Mac/Linux

pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Backend runs at:

➡️ [http://localhost:8000](http://localhost:8000)
➡️ [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🖥 Frontend Setup

Open a second terminal:

```bash
cd frontend
python -m venv venv
venv\Scripts\activate     # Windows
# or source venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

Frontend runs at:

➡️ [http://localhost:8501](http://localhost:8501)

---

## 🔐 Environment Variables

Create a `.env` file inside the **backend** directory:

```
OPENAI_API_KEY=your_openai_key_here
GITHUB_TOKEN=your_github_pat_here   # optional but recommended
OPENAI_MODEL=gpt-4.1
```

These are automatically loaded by the backend.

⚠️ The frontend does NOT require any env variables.

---

## 🧪 Testing Installation

Try analyzing a public GitHub issue:

* Repo: `https://github.com/facebook/react`
* Issue: `1`

If everything works, you will see:

* Summary
* AI insights
* JSON output
* Metadata
* Download buttons

---

## ❗ Troubleshooting

| Issue             | Fix                                  |
| ----------------- | ------------------------------------ |
| Module not found  | Ensure `venv` is activated           |
| Backend 403       | Add a GitHub token to `.env`         |
| White UI          | Missing `.streamlit/config.toml`     |
| KeyError: history | Move session init to top of `app.py` |

---









