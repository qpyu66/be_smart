# 10. 배포 가이드

## 📋 목표
- Frontend 배포 (Vercel)
- Backend 배포 (Railway)
- Database 배포 (Railway PostgreSQL)
- 환경 변수 설정

---

## 🚀 배포 개요

### 배포 구조
```
Frontend (Vercel)
    ↓ API 요청
Backend (Railway)
    ↓ DB 연결
Database (Railway PostgreSQL)
```

---

## 🗄️ 1. Database 배포 (Railway PostgreSQL)

### 1.1 Railway 회원가입
```
1. https://railway.app 접속
2. GitHub 계정으로 가입
3. New Project 클릭
```

### 1.2 PostgreSQL 생성
```
1. "Deploy PostgreSQL" 선택
2. 프로젝트 이름: econolearn-db
3. Deploy 클릭
```

### 1.3 데이터베이스 정보 확인
```
1. PostgreSQL 서비스 클릭
2. "Connect" 탭에서 연결 정보 확인
3. DATABASE_URL 복사 (예: postgresql://...)
```

### 1.4 테이블 생성
```bash
# Railway CLI 설치 (선택사항)
npm install -g @railway/cli

# 또는 로컬에서 연결
export DATABASE_URL="postgresql://..."
python backend/init_db.py
python backend/seed_data.py
```

---

## 🐍 2. Backend 배포 (Railway)

### 2.1 준비 작업

#### requirements.txt 확인
```bash
cd backend
cat requirements.txt

# 필수 패키지 확인
# fastapi
# uvicorn[standard]
# sqlalchemy
# psycopg2-binary
# python-jose[cryptography]
# passlib[bcrypt]
# python-multipart
# pydantic[email]
# python-dotenv
```

#### runtime.txt 생성
```bash
cat > runtime.txt << 'EOF'
python-3.11.0
EOF
```

#### Procfile 생성
```bash
cat > Procfile << 'EOF'
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
EOF
```

---

### 2.2 Railway에 배포

#### Git 저장소 준비
```bash
cd ..  # 프로젝트 루트로
git add .
git commit -m "Prepare for deployment"
git push origin main
```

#### Railway 배포
```
1. Railway 대시보드에서 "New Project"
2. "Deploy from GitHub repo" 선택
3. econolearn 저장소 선택
4. Root directory: backend
5. Deploy 클릭
```

### 2.3 환경 변수 설정
```
Railway 프로젝트 > Variables 탭

DATABASE_URL=postgresql://...  (Railway PostgreSQL 연결 문자열)
SECRET_KEY=your-very-secure-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 2.4 배포 URL 확인
```
Settings > Domains > Generate Domain
예: https://econolearn-backend.up.railway.app
```

---

## ⚛️ 3. Frontend 배포 (Vercel)

### 3.1 준비 작업

#### 환경 변수 파일 생성
```bash
cd frontend
cat > .env.production << 'EOF'
REACT_APP_API_URL=https://econolearn-backend.up.railway.app/api
EOF
```

#### package.json 확인
```json
{
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  }
}
```

---

### 3.2 Vercel에 배포

#### Vercel CLI 설치 (선택사항)
```bash
npm install -g vercel
```

#### 배포 방법 1: Vercel 웹사이트
```
1. https://vercel.com 접속
2. GitHub 계정으로 가입
3. "New Project" 클릭
4. econolearn 저장소 선택
5. Root Directory: frontend
6. Framework Preset: Create React App
7. Environment Variables 추가:
   REACT_APP_API_URL=https://econolearn-backend.up.railway.app/api
8. Deploy 클릭
```

#### 배포 방법 2: Vercel CLI
```bash
cd frontend
vercel

# 질문에 답변
# Set up and deploy? Yes
# Which scope? (개인 계정 선택)
# Link to existing project? No
# What's your project's name? econolearn
# In which directory is your code located? ./
# Auto-detected: Create React App
# Override settings? No

# Production 배포
vercel --prod
```

---

### 3.3 배포 URL 확인
```
예: https://econolearn.vercel.app
```

---

## 🔧 4. CORS 설정 업데이트

### Backend CORS 설정
```bash
cd backend/app
# main.py 수정

cat > main.py << 'EOF'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="EconoLearn API")

# CORS 설정 - 프로덕션 도메인 추가
origins = [
    "http://localhost:3000",
    "https://econolearn.vercel.app",  # Vercel 도메인
    # 추가 도메인...
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ... 나머지 코드
EOF

# Git push
git add .
git commit -m "Update CORS settings"
git push
```

---

## ✅ 5. 배포 확인

### 5.1 Backend 확인
```bash
# Health check
curl https://econolearn-backend.up.railway.app/health

# API 문서
# https://econolearn-backend.up.railway.app/docs
```

### 5.2 Frontend 확인
```
1. https://econolearn.vercel.app 접속
2. 회원가입 테스트
3. 로그인 테스트
4. 강의 조회 테스트
```

### 5.3 Database 확인
```bash
# Railway에서 PostgreSQL Connect 탭
# psql 명령어로 연결
psql $DATABASE_URL

# 테이블 확인
\dt

# 데이터 확인
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM lessons;
```

---

## 🔐 6. 보안 설정

### 6.1 SECRET_KEY 생성
```python
# 안전한 SECRET_KEY 생성
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 6.2 환경 변수 보안
```
❌ 하지 말 것:
- .env 파일을 Git에 커밋
- SECRET_KEY를 코드에 하드코딩

✅ 해야 할 것:
- Railway/Vercel에서만 환경 변수 설정
- .env 파일은 .gitignore에 추가
- 프로덕션과 개발 환경 분리
```

---

## 📊 7. 모니터링 & 로그

### Railway 로그 확인
```
1. Railway 프로젝트 > Deployments
2. 최신 배포 클릭
3. "View Logs" 클릭
```

### Vercel 로그 확인
```
1. Vercel 프로젝트 > Deployments
2. 최신 배포 클릭
3. "View Function Logs" 클릭
```

---

## 🔄 8. CI/CD (자동 배포)

### GitHub Actions 설정 (선택사항)
```bash
mkdir -p .github/workflows
cat > .github/workflows/deploy.yml << 'EOF'
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Railway
        run: echo "Railway auto-deploys on push"

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Vercel
        run: echo "Vercel auto-deploys on push"
EOF
```

---

## 💰 9. 비용 관리

### Railway 무료 티어
```
- $5 무료 크레딧/월
- PostgreSQL: ~$5/월
- Backend: 사용량에 따라 변동
```

### Vercel 무료 티어
```
- 100GB 대역폭/월
- Hobby 프로젝트는 무료
```

---

## 🐛 10. 트러블슈팅

### 문제 1: CORS 에러
```
증상: Frontend에서 API 호출 실패
해결:
1. Backend CORS 설정 확인
2. Frontend 도메인이 허용 목록에 있는지 확인
3. Railway 로그에서 에러 확인
```

### 문제 2: Database 연결 실패
```
증상: 500 Internal Server Error
해결:
1. Railway DATABASE_URL 확인
2. PostgreSQL 서비스가 실행 중인지 확인
3. 연결 문자열 형식 확인
```

### 문제 3: Build 실패
```
증상: Deployment failed
해결:
1. 로그에서 에러 메시지 확인
2. requirements.txt / package.json 확인
3. 로컬에서 build 테스트: npm run build
```

### 문제 4: 환경 변수 미적용
```
증상: API URL이 localhost로 설정됨
해결:
1. Vercel Environment Variables 재확인
2. 재배포 필요 (Environment 변경 후)
3. .env.production 파일 확인
```

---

## 📱 11. 커스텀 도메인 (선택사항)

### Vercel 커스텀 도메인
```
1. 도메인 구매 (예: econolearn.com)
2. Vercel 프로젝트 > Settings > Domains
3. 도메인 추가
4. DNS 레코드 설정 (Vercel 가이드 따르기)
```

### Railway 커스텀 도메인
```
1. Railway 프로젝트 > Settings > Domains
2. Custom Domain 추가
3. DNS CNAME 레코드 설정
```

---

## 📝 12. 배포 체크리스트

### Backend 배포 전
- [ ] requirements.txt 최신 상태
- [ ] Procfile 생성
- [ ] 환경 변수 설정
- [ ] SECRET_KEY 생성
- [ ] CORS 설정 확인

### Frontend 배포 전
- [ ] .env.production 생성
- [ ] API URL 확인
- [ ] Build 테스트 (npm run build)
- [ ] 환경 변수 설정

### 배포 후
- [ ] Health check 확인
- [ ] 회원가입/로그인 테스트
- [ ] API 호출 테스트
- [ ] 로그 확인
- [ ] 에러 모니터링 설정

---

## 🎉 완료!

축하합니다! EconoLearn 앱이 성공적으로 배포되었습니다.

### 배포된 URL
- Frontend: https://econolearn.vercel.app
- Backend API: https://econolearn-backend.up.railway.app
- API Docs: https://econolearn-backend.up.railway.app/docs

---

## 🚀 다음 단계

1. **사용자 피드백 수집**
   - 실제 사용자 테스트
   - 버그 리포트 수집

2. **기능 추가**
   - 경제 뉴스 피드
   - 퀴즈 시스템
   - 알림 기능

3. **성능 최적화**
   - 이미지 최적화
   - API 응답 캐싱
   - Database 인덱싱

4. **모니터링 설정**
   - Sentry (에러 추적)
   - Google Analytics
   - 성능 모니터링

---

## 📚 추가 리소스

- [Railway 문서](https://docs.railway.app)
- [Vercel 문서](https://vercel.com/docs)
- [FastAPI 배포](https://fastapi.tiangolo.com/deployment/)
- [React 배포](https://create-react-app.dev/docs/deployment/)

---

**프로젝트 완료! 🎊**

모든 개발 문서가 완성되었습니다. 각 문서를 순서대로 따라가면서 앱을 개발하고 배포하세요!