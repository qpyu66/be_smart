# 03. Backend API 개발 (FastAPI)

## 📋 목표
- 인증 시스템 구축 (JWT)
- Lessons API 개발
- Progress API 개발
- CRUD 작업 구현

---

## 🔐 인증 시스템 구축

### 1. Pydantic 스키마 생성

#### schemas/__init__.py
```bash
cd backend/app/schemas
cat > __init__.py << 'EOF'
from .user import UserCreate, UserLogin, UserResponse, Token
from .lesson import LessonResponse, LessonCreate
from .progress import ProgressResponse, ProgressUpdate

__all__ = [
    "UserCreate", "UserLogin", "UserResponse", "Token",
    "LessonResponse", "LessonCreate",
    "ProgressResponse", "ProgressUpdate"
]
EOF
```

---

#### schemas/user.py
```bash
cat > user.py << 'EOF'
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str
    level: Optional[str] = "intermediate"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    level: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
EOF
```

---

#### schemas/lesson.py
```bash
cat > lesson.py << 'EOF'
from pydantic import BaseModel
from typing import Optional

class LessonBase(BaseModel):
    title: str
    content: str
    category: str
    level: str
    order: int
    estimated_time: Optional[int] = 15

class LessonCreate(LessonBase):
    pass

class LessonResponse(LessonBase):
    id: int
    
    class Config:
        from_attributes = True
EOF
```

---

#### schemas/progress.py
```bash
cat > progress.py << 'EOF'
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProgressBase(BaseModel):
    lesson_id: int
    progress: float
    completed: bool

class ProgressUpdate(BaseModel):
    progress: float
    completed: Optional[bool] = False

class ProgressResponse(ProgressBase):
    id: int
    user_id: int
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True
EOF
```

---

### 2. 인증 유틸리티 생성

#### services/auth.py
```bash
cd ../services
cat > auth.py << 'EOF'
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

from ..database import get_db
from ..models.user import User
from ..schemas.user import TokenData

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """비밀번호 확인"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """비밀번호 해싱"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """JWT 토큰 생성"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """현재 로그인한 사용자 가져오기"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user
EOF
```

---

### 3. API 엔드포인트 개발

#### api/auth.py
```bash
cd ../api
cat > auth.py << 'EOF'
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from ..database import get_db
from ..models.user import User
from ..models.daily_streak import DailyStreak
from ..schemas.user import UserCreate, UserLogin, UserResponse, Token
from ..services.auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_current_user
)

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """회원가입"""
    # 이메일 중복 확인
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # 사용자 생성
    hashed_password = get_password_hash(user.password)
    new_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        level=user.level
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # 스트릭 초기화
    streak = DailyStreak(user_id=new_user.id)
    db.add(streak)
    db.commit()
    
    return new_user

@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """로그인"""
    user = db.query(User).filter(User.email == user_credentials.email).first()
    
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # JWT 토큰 생성
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """현재 사용자 정보"""
    return current_user

@router.put("/level")
def update_level(level: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """사용자 레벨 변경"""
    if level not in ["beginner", "intermediate", "advanced"]:
        raise HTTPException(status_code=400, detail="Invalid level")
    
    current_user.level = level
    db.commit()
    return {"message": "Level updated successfully", "level": level}
EOF
```

---

#### api/lessons.py
```bash
cat > lessons.py << 'EOF'
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.lesson import Lesson
from ..models.user import User
from ..schemas.lesson import LessonResponse
from ..services.auth import get_current_user

router = APIRouter(prefix="/lessons", tags=["Lessons"])

@router.get("/", response_model=List[LessonResponse])
def get_lessons(
    category: str = None,
    level: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """강의 목록 조회"""
    query = db.query(Lesson)
    
    if category:
        query = query.filter(Lesson.category == category)
    if level:
        query = query.filter(Lesson.level == level)
    else:
        # 사용자 레벨에 맞는 강의 필터링
        query = query.filter(Lesson.level == current_user.level)
    
    lessons = query.order_by(Lesson.order).all()
    return lessons

@router.get("/{lesson_id}", response_model=LessonResponse)
def get_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """강의 상세 조회"""
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson

@router.get("/category/{category}", response_model=List[LessonResponse])
def get_lessons_by_category(
    category: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """카테고리별 강의 조회"""
    lessons = db.query(Lesson).filter(
        Lesson.category == category
    ).order_by(Lesson.order).all()
    return lessons

@router.get("/daily/today", response_model=LessonResponse)
def get_daily_lesson(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """오늘의 데일리 강의"""
    # 사용자의 다음 학습할 강의 찾기
    from ..models.user_progress import UserProgress
    
    # 완료하지 않은 첫 번째 강의 찾기
    completed_lessons = db.query(UserProgress.lesson_id).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.completed == True
    ).all()
    completed_ids = [lesson.lesson_id for lesson in completed_lessons]
    
    next_lesson = db.query(Lesson).filter(
        Lesson.level == current_user.level,
        ~Lesson.id.in_(completed_ids)
    ).order_by(Lesson.order).first()
    
    if not next_lesson:
        # 모든 강의를 완료한 경우 첫 번째 강의 반환
        next_lesson = db.query(Lesson).filter(
            Lesson.level == current_user.level
        ).order_by(Lesson.order).first()
    
    return next_lesson
EOF
```

---

#### api/progress.py
```bash
cat > progress.py << 'EOF'
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, date

from ..database import get_db
from ..models.user_progress import UserProgress
from ..models.daily_streak import DailyStreak
from ..models.user import User
from ..schemas.progress import ProgressResponse, ProgressUpdate
from ..services.auth import get_current_user

router = APIRouter(prefix="/progress", tags=["Progress"])

@router.get("/", response_model=List[ProgressResponse])
def get_user_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """사용자의 모든 진도 조회"""
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id
    ).all()
    return progress

@router.get("/lesson/{lesson_id}", response_model=ProgressResponse)
def get_lesson_progress(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """특정 강의의 진도 조회"""
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.lesson_id == lesson_id
    ).first()
    
    if not progress:
        # 진도가 없으면 새로 생성
        progress = UserProgress(
            user_id=current_user.id,
            lesson_id=lesson_id,
            progress=0.0,
            completed=False
        )
        db.add(progress)
        db.commit()
        db.refresh(progress)
    
    return progress

@router.put("/lesson/{lesson_id}", response_model=ProgressResponse)
def update_lesson_progress(
    lesson_id: int,
    progress_data: ProgressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """강의 진도 업데이트"""
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.lesson_id == lesson_id
    ).first()
    
    if not progress:
        progress = UserProgress(
            user_id=current_user.id,
            lesson_id=lesson_id
        )
        db.add(progress)
    
    progress.progress = progress_data.progress
    progress.completed = progress_data.completed
    
    if progress_data.completed and not progress.completed_at:
        progress.completed_at = datetime.utcnow()
        
        # 스트릭 업데이트
        update_daily_streak(current_user.id, db)
    
    db.commit()
    db.refresh(progress)
    return progress

@router.get("/stats")
def get_progress_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """진도 통계"""
    total_lessons = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id
    ).count()
    
    completed_lessons = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.completed == True
    ).count()
    
    streak = db.query(DailyStreak).filter(
        DailyStreak.user_id == current_user.id
    ).first()
    
    return {
        "total_lessons": total_lessons,
        "completed_lessons": completed_lessons,
        "completion_rate": completed_lessons / total_lessons if total_lessons > 0 else 0,
        "current_streak": streak.current_streak if streak else 0,
        "longest_streak": streak.longest_streak if streak else 0
    }

def update_daily_streak(user_id: int, db: Session):
    """데일리 스트릭 업데이트"""
    streak = db.query(DailyStreak).filter(DailyStreak.user_id == user_id).first()
    
    if not streak:
        streak = DailyStreak(user_id=user_id)
        db.add(streak)
    
    today = date.today()
    
    if streak.last_study_date:
        days_diff = (today - streak.last_study_date).days
        
        if days_diff == 0:
            # 오늘 이미 공부함
            pass
        elif days_diff == 1:
            # 연속 학습
            streak.current_streak += 1
            if streak.current_streak > streak.longest_streak:
                streak.longest_streak = streak.current_streak
        else:
            # 연속 끊김
            streak.current_streak = 1
    else:
        # 첫 학습
        streak.current_streak = 1
        streak.longest_streak = 1
    
    streak.last_study_date = today
    db.commit()
EOF
```

---

### 4. main.py 업데이트

```bash
cd ..
cat > main.py << 'EOF'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import auth, lessons, progress

app = FastAPI(
    title="EconoLearn API",
    description="경제 학습 애플리케이션 API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(auth.router, prefix="/api")
app.include_router(lessons.router, prefix="/api")
app.include_router(progress.router, prefix="/api")

@app.get("/")
def read_root():
    return {
        "message": "EconoLearn API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
EOF
```

---

## 🧪 API 테스트

### 1. 서버 실행
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

### 2. API 문서 확인
브라우저에서 접속:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

### 3. cURL로 테스트

#### 회원가입
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "테스트유저",
    "password": "password123",
    "level": "intermediate"
  }'
```

#### 로그인
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

#### 강의 목록 조회 (인증 필요)
```bash
# 위에서 받은 토큰 사용
TOKEN="your_access_token_here"

curl -X GET "http://localhost:8000/api/lessons/" \
  -H "Authorization: Bearer $TOKEN"
```

#### 오늘의 데일리 강의
```bash
curl -X GET "http://localhost:8000/api/lessons/daily/today" \
  -H "Authorization: Bearer $TOKEN"
```

#### 진도 업데이트
```bash
curl -X PUT "http://localhost:8000/api/progress/lesson/1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "progress": 0.5,
    "completed": false
  }'
```

---

## 📝 API 엔드포인트 요약

### 인증 (Authentication)
| Method | Endpoint | 설명 | 인증 |
|--------|----------|------|------|
| POST | `/api/auth/register` | 회원가입 | ❌ |
| POST | `/api/auth/login` | 로그인 | ❌ |
| GET | `/api/auth/me` | 현재 사용자 정보 | ✅ |
| PUT | `/api/auth/level` | 레벨 변경 | ✅ |

### 강의 (Lessons)
| Method | Endpoint | 설명 | 인증 |
|--------|----------|------|------|
| GET | `/api/lessons/` | 강의 목록 | ✅ |
| GET | `/api/lessons/{id}` | 강의 상세 | ✅ |
| GET | `/api/lessons/category/{category}` | 카테고리별 강의 | ✅ |
| GET | `/api/lessons/daily/today` | 오늘의 강의 | ✅ |

### 진도 (Progress)
| Method | Endpoint | 설명 | 인증 |
|--------|----------|------|------|
| GET | `/api/progress/` | 전체 진도 | ✅ |
| GET | `/api/progress/lesson/{id}` | 강의별 진도 | ✅ |
| PUT | `/api/progress/lesson/{id}` | 진도 업데이트 | ✅ |
| GET | `/api/progress/stats` | 통계 | ✅ |

---

## 🐛 트러블슈팅

### 1. CORS 에러
```python
# main.py에서 allow_origins 확인
allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"]
```

### 2. JWT 토큰 에러
```bash
# .env 파일에서 SECRET_KEY 확인
SECRET_KEY=your-very-secure-secret-key-change-this
```

### 3. 데이터베이스 연결 에러
```bash
# PostgreSQL 실행 확인
brew services list | grep postgresql

# 데이터베이스 존재 확인
psql -l | grep econolearn
```

### 4. 모듈 임포트 에러
```bash
# 패키지 재설치
pip install -r requirements.txt

# __init__.py 파일 확인
ls -la app/api/__init__.py
```

---

## ✅ 다음 단계

Backend API 개발이 완료되었습니다!

**다음 문서**: [04-frontend-structure.md](./04-frontend-structure.md)에서 React 프론트엔드 구조를 만듭니다.