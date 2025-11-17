# cura-link — backend

This repository contains the backend for the cura-link project (FastAPI-based).

## Quick overview

- Language: Python 3.10+
- Framework: FastAPI
- Entry point: `run.py` (or `uvicorn app.main:app --reload`)

## Quick start

1. Create and activate a virtual environment:

```bash
python -m venv .venv
# Windows
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:

Create a `.env` file in the root directory with the following variables:

```env
DATABASE_URL=your_database_url
JWT_SECRET=your_jwt_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
RESEARCHER_ROLE=2
HUGGINGFACE_API_KEY=your_huggingface_api_key  # Optional: Required for PDF metadata extraction
```

**Note:** To get a Hugging Face API key:
1. Sign up at [huggingface.co](https://huggingface.co)
2. Go to your profile settings → Access Tokens
3. Create a new token with read permissions
4. Add it to your `.env` file

4. Run the app:

```bash
python run.py
# or for development:
uvicorn app.main:app --reload
```

## Project file tree

```text
cura-link/backend/
├── app/                          # Application package
│   ├── __init__.py
│   ├── main.py
│   ├── template/
│   │   └── index.html
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       ├── trials.py
│   │       ├── forums.py
│   │       ├── onboarding.py
│   │       ├── favourites.py
│   │       ├── experts.py
│   │       ├── publications.py
│   │       └── forum/
│   │           ├── categories.py
│   │           └── reply.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── deps.py
│   │   └── security.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── init_db.py
│   │   └── check_db.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── patient_profile.py
│   │   ├── researcher_profile.py
│   │   ├── forums.py
│   │   ├── forums_reply.py
│   │   ├── forums_category.py
│   │   ├── favourite.py
│   │   ├── expert.py
│   │   ├── publication.py
│   │   └── trial.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user_schema.py
│   │   ├── onboarding_schema.py
│   │   ├── publication_schema.py
│   │   ├── trial_schema.py
│   │   ├── forums.py
│   │   ├── forums_reply.py
│   │   └── expert_schema.py
│   └── services/
│       └── __init__.py
├── run.py                        # Run / entrypoint script
├── requirements.txt              # Python dependencies
└── vercel.json                   # Vercel configuration (if deployed)
```

## Notes

- The app is configured to exclude git, virtualenv, and cache files from the README tree for readability.
- If you want a version that includes hidden files or an ASCII `tree` output, tell me and I will add it.

## Contact

For questions about the backend, open an issue or contact the maintainer.


