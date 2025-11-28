# 01. 개발 환경 설정

## 📋 목표
- Node.js, Python, PostgreSQL 설치
- 프로젝트 디렉토리 구조 생성
- Frontend (React) 프로젝트 초기화
- Backend (FastAPI) 프로젝트 초기화

---

## 🛠 필수 프로그램 설치

### 1. Node.js 설치 (v18 이상)

**Mac:**
```bash
brew install node
```

**Windows:**
- https://nodejs.org 에서 LTS 버전 다운로드

**설치 확인:**
```bash
node --version  # v18.0.0 이상
npm --version   # 9.0.0 이상
```

---

### 2. Python 설치 (v3.11 이상)

**Mac:**
```bash
brew install python@3.11
```

**Windows:**
- https://www.python.org/downloads/ 에서 다운로드

**설치 확인:**
```bash
python3 --version  # 3.11.0 이상
pip3 --version
```

---

### 3. PostgreSQL 설치

**Mac:**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Windows:**
- https://www.postgresql.org/download/ 에서 다운로드

**설치 확인:**
```bash
psql --version  # 15.0 이상
```

---

## 📁 프로젝트 생성

### 1. 루트 디렉토리 생성
```bash
mkdir econolearn
cd econolearn
```

### 2. Git 초기화
```bash
git init
```

### 3. .gitignore 생성
```bash
cat > .gitignore << 'EOF'
# Node
node_modules/
dist/
build/

# Python
__pycache__/
*.py[cod]
*$py.class
venv/
.env

# Database
*.db
*.sqlite

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
EOF
```

---

## ⚛️ Frontend 설정 (React + TypeScript)

### 1. React 프로젝트 생성
```bash
npx create-react-app frontend --template typescript
cd frontend
```

### 2. 필수 패키지 설치
```bash
npm install react-router-dom
npm install axios
npm install @types/react-router-dom --save-dev
```

### 3. Tailwind CSS 설치 (선택)
```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

**tailwind.config.js 수정:**
```bash
cat > tailwind.config.js << 'EOF'
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#3498db',
        secondary: '#667eea',
      },
    },
  },
  plugins: [],
}
EOF
```

**src/index.css 수정:**
```bash
cat > src/index.css << 'EOF'
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
EOF
```

### 4. 디렉토리 구조 생성
```bash
cd src
mkdir components pages hooks context services utils types
cd ..
```

### 5. 개발 서버 실행 테스트
```bash
npm start
```
브라우저에서 http://localhost:3000 접속 확인

**종료**: Ctrl + C

---

## 🐍 Backend 설정 (FastAPI + Python)

### 1. 프로젝트 디렉토리로 돌아가기
```bash
cd ..  # econolearn 디렉토리로
```

### 2. Backend 디렉토리 생성
```bash
mkdir backend
cd backend
```

### 3. Python 가상환경 생성
```bash
python3 -m venv venv

# 가상환경 활성화
# Mac/Linux:
source venv/bin/activate

# Windows:
# venv\Scripts\activate
```

### 4. 필수 패키지 설치
```bash
pip install fastapi
pip install uvicorn[standard]
pip install sqlalchemy
pip install psycopg2-binary
pip install python-jose[cryptography]
pip install passlib[bcrypt]
pip install python-multipart
pip install pydantic[email]
pip install python-dotenv
pip install requests
pip install beautifulsoup4
```

### 5. requirements.txt 생성
```bash
pip freeze > requirements.txt
```

### 6. 디렉토리 구조 생성
```bash
mkdir app
cd app
mkdir api models schemas services
touch __init__.py main.py database.py
cd api
touch __init__.py auth.py lessons.py progress.py
cd ../..
```

### 7. .env 파일 생성
```bash
cat > .env << 'EOF'
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/econolearn

# JWT Secret
SECRET_KEY=your-secret-key-here-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
EOF
```

### 8. 간단한 FastAPI 서버 테스트
```bash
cat > app/main.py << 'EOF'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="EconoLearn API")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "EconoLearn API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
EOF
```

### 9. 개발 서버 실행 테스트
```bash
uvicorn app.main:app --reload
```
브라우저에서 http://localhost:8000 접속 확인
API 문서: http://localhost:8000/docs

**종료**: Ctrl + C

---

## 🗄️ PostgreSQL 데이터베이스 생성

### 1. PostgreSQL 접속
```bash
psql postgres
```

### 2. 데이터베이스 생성
```sql
CREATE DATABASE econolearn;
```

### 3. 사용자 생성 (선택사항)
```sql
CREATE USER econolearn_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE econolearn TO econolearn_user;
```

### 4. 종료
```sql
\q
```

### 5. 연결 테스트
```bash
psql -d econolearn -U postgres
```

---

## ✅ 설정 확인 체크리스트

모든 명령어가 작동하는지 확인:

```bash
# Node.js
node --version

# Python
python3 --version

# PostgreSQL
psql --version

# Frontend 디렉토리 확인
ls frontend/src

# Backend 디렉토리 확인
ls backend/app

# 가상환경 활성화 상태 확인
which python  # venv 경로가 나와야 함
```

---

## 🚀 최종 프로젝트 구조

```
econolearn/
├── frontend/
│   ├── node_modules/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── context/
│   │   ├── services/
│   │   ├── utils/
│   │   ├── types/
│   │   ├── App.tsx
│   │   └── index.tsx
│   ├── package.json
│   └── tailwind.config.js
│
├── backend/
│   ├── venv/
│   ├── app/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── lessons.py
│   │   │   └── progress.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── database.py
│   ├── .env
│   └── requirements.txt
│
└── .gitignore
```

---

## 📝 개발 서버 실행 명령어 요약

### Frontend 실행
```bash
cd frontend
npm start
```

### Backend 실행
```bash
cd backend
source venv/bin/activate  # 가상환경 활성화
uvicorn app.main:app --reload
```

---

## 🐛 트러블슈팅

### 1. PostgreSQL 연결 오류
```bash
# PostgreSQL 서비스 시작
brew services start postgresql@15  # Mac
# 또는
sudo systemctl start postgresql    # Linux
```

### 2. Python 가상환경 활성화 안됨
```bash
# 가상환경 재생성
rm -rf venv
python3 -m venv venv
source venv/bin/activate
```

### 3. npm 설치 오류
```bash
# node_modules 삭제 후 재설치
rm -rf node_modules package-lock.json
npm install
```

### 4. 포트 이미 사용 중
```bash
# 3000 포트 사용 중인 프로세스 종료
lsof -ti:3000 | xargs kill -9

# 8000 포트 사용 중인 프로세스 종료
lsof -ti:8000 | xargs kill -9
```

---

## ✅ 다음 단계

환경 설정이 완료되었습니다!

**다음 문서**: [02-database.md](./02-database.md)에서 데이터베이스 스키마를 설계합니다.