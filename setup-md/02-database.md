# 02. 데이터베이스 스키마 설계

## 📋 목표
- 데이터베이스 테이블 구조 설계
- SQLAlchemy 모델 생성
- 데이터베이스 초기화
- 샘플 데이터 삽입

---

## 🗄️ 데이터베이스 설계

### ERD (Entity Relationship Diagram)

```
┌─────────────────┐
│     users       │
├─────────────────┤
│ id (PK)         │
│ email           │
│ hashed_password │
│ username        │
│ level           │
│ created_at      │
└────────┬────────┘
         │
         │ 1:N
         │
┌────────┴────────┐
│  user_progress  │
├─────────────────┤
│ id (PK)         │
│ user_id (FK)    │
│ lesson_id (FK)  │
│ completed       │
│ progress        │
│ completed_at    │
└────────┬────────┘
         │
         │ N:1
         │
┌────────┴────────┐
│    lessons      │
├─────────────────┤
│ id (PK)         │
│ category        │
│ title           │
│ content         │
│ level           │
│ order           │
│ estimated_time  │
└─────────────────┘

┌─────────────────┐
│  daily_streak   │
├─────────────────┤
│ id (PK)         │
│ user_id (FK)    │
│ current_streak  │
│ longest_streak  │
│ last_study_date │
└─────────────────┘

┌─────────────────┐
│   bookmarks     │
├─────────────────┤
│ id (PK)         │
│ user_id (FK)    │
│ lesson_id (FK)  │
│ created_at      │
└─────────────────┘
```

---

## 🐍 SQLAlchemy 모델 생성

### 1. database.py 작성

```bash
cd backend/app
cat > database.py << 'EOF'
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
EOF
```

---

### 2. models 생성

#### models/__init__.py
```bash
cd models
cat > __init__.py << 'EOF'
from .user import User
from .lesson import Lesson
from .user_progress import UserProgress
from .daily_streak import DailyStreak
from .bookmark import Bookmark

__all__ = ["User", "Lesson", "UserProgress", "DailyStreak", "Bookmark"]
EOF
```

---

#### models/user.py
```bash
cat > user.py << 'EOF'
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..database import Base

class LevelEnum(str, enum.Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    level = Column(Enum(LevelEnum), default=LevelEnum.intermediate)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    progress = relationship("UserProgress", back_populates="user", cascade="all, delete-orphan")
    streak = relationship("DailyStreak", back_populates="user", uselist=False, cascade="all, delete-orphan")
    bookmarks = relationship("Bookmark", back_populates="user", cascade="all, delete-orphan")
EOF
```

---

#### models/lesson.py
```bash
cat > lesson.py << 'EOF'
from sqlalchemy import Column, Integer, String, Text, Enum
from sqlalchemy.orm import relationship
import enum
from ..database import Base

class CategoryEnum(str, enum.Enum):
    economics_basics = "economics_basics"
    financial_market = "financial_market"
    investment = "investment"
    economic_news = "economic_news"
    economic_indicators = "economic_indicators"
    financial_statements = "financial_statements"

class LevelEnum(str, enum.Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(Enum(CategoryEnum), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    level = Column(Enum(LevelEnum), nullable=False)
    order = Column(Integer, nullable=False)
    estimated_time = Column(Integer, default=15)  # minutes
    
    # Relationships
    progress = relationship("UserProgress", back_populates="lesson")
    bookmarks = relationship("Bookmark", back_populates="lesson")
EOF
```

---

#### models/user_progress.py
```bash
cat > user_progress.py << 'EOF'
from sqlalchemy import Column, Integer, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    completed = Column(Boolean, default=False)
    progress = Column(Float, default=0.0)  # 0.0 to 1.0
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="progress")
    lesson = relationship("Lesson", back_populates="progress")
EOF
```

---

#### models/daily_streak.py
```bash
cat > daily_streak.py << 'EOF'
from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date
from ..database import Base

class DailyStreak(Base):
    __tablename__ = "daily_streak"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_study_date = Column(Date, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="streak")
EOF
```

---

#### models/bookmark.py
```bash
cat > bookmark.py << 'EOF'
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Bookmark(Base):
    __tablename__ = "bookmarks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="bookmarks")
    lesson = relationship("Lesson", back_populates="bookmarks")
EOF
```

---

## 🏗️ 데이터베이스 초기화 스크립트

### init_db.py 생성

```bash
cd ../..  # backend 디렉토리로
cat > init_db.py << 'EOF'
from app.database import engine, Base
from app.models import User, Lesson, UserProgress, DailyStreak, Bookmark

def init_database():
    """데이터베이스 테이블 생성"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")

if __name__ == "__main__":
    init_database()
EOF
```

---

### 데이터베이스 초기화 실행

```bash
# 가상환경 활성화 확인
source venv/bin/activate

# 초기화 실행
python init_db.py
```

---

## 📝 샘플 데이터 생성

### seed_data.py 생성

```bash
cat > seed_data.py << 'EOF'
from app.database import SessionLocal
from app.models import Lesson, User
from app.models.lesson import CategoryEnum, LevelEnum as LessonLevel
from app.models.user import LevelEnum as UserLevel
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_sample_lessons():
    """샘플 강의 데이터 생성"""
    db = SessionLocal()
    
    # 경제 기초 강의
    lessons = [
        # 초급 - 경제 기초
        Lesson(
            category=CategoryEnum.economics_basics,
            title="경제학이란 무엇인가?",
            content="""
# 경제학의 정의

경제학(Economics)은 희소한 자원을 어떻게 효율적으로 배분할 것인가를 연구하는 학문입니다.

## 핵심 개념
- **희소성**: 원하는 것은 많지만 자원은 제한적
- **선택**: 무엇을 생산하고 소비할지 결정
- **기회비용**: 선택으로 인해 포기한 것의 가치

## 예시
커피를 5,000원에 산다면, 그 돈으로 살 수 있었던 다른 것(빵, 음료 등)을 포기하는 것입니다.
            """,
            level=LessonLevel.beginner,
            order=1,
            estimated_time=10
        ),
        Lesson(
            category=CategoryEnum.economics_basics,
            title="수요와 공급의 법칙",
            content="""
# 수요와 공급

시장경제의 가장 기본적인 원리입니다.

## 수요 (Demand)
- 소비자가 구매하고자 하는 상품의 양
- 가격이 오르면 수요량 감소
- 가격이 내리면 수요량 증가

## 공급 (Supply)
- 생산자가 판매하고자 하는 상품의 양
- 가격이 오르면 공급량 증가
- 가격이 내리면 공급량 감소

## 균형가격
수요와 공급이 만나는 지점에서 가격이 결정됩니다.
            """,
            level=LessonLevel.beginner,
            order=2,
            estimated_time=15
        ),
        
        # 중급 - 거시경제
        Lesson(
            category=CategoryEnum.economics_basics,
            title="GDP와 경제성장",
            content="""
# GDP (국내총생산)

GDP는 한 나라에서 일정 기간 동안 생산된 모든 최종 재화와 서비스의 시장가치 합계입니다.

## GDP의 구성
- **소비(C)**: 가계의 소비 지출
- **투자(I)**: 기업의 투자 지출
- **정부지출(G)**: 정부의 지출
- **순수출(NX)**: 수출 - 수입

공식: GDP = C + I + G + NX

## 경제성장률
전년 대비 GDP 증가율로, 경제가 얼마나 성장했는지를 나타냅니다.
            """,
            level=LessonLevel.intermediate,
            order=3,
            estimated_time=20
        ),
        
        # 투자/재테크
        Lesson(
            category=CategoryEnum.investment,
            title="주식 투자 기초",
            content="""
# 주식이란?

주식은 기업의 소유권을 나타내는 증서입니다.

## 주식 투자의 수익
1. **시세차익**: 주가 상승으로 얻는 이익
2. **배당금**: 기업이 이익의 일부를 주주에게 지급

## 기본 용어
- **시가총액**: 주가 × 발행주식수
- **PER**: 주가수익비율 (주가 / 주당순이익)
- **ROE**: 자기자본이익률

## 투자 원칙
- 분산투자: 여러 종목에 투자
- 장기투자: 시간을 두고 투자
- 이해하는 기업에 투자
            """,
            level=LessonLevel.beginner,
            order=1,
            estimated_time=15
        ),
        
        Lesson(
            category=CategoryEnum.investment,
            title="자산배분 전략",
            content="""
# 자산배분이란?

여러 자산에 투자 비중을 나누어 리스크를 관리하는 전략입니다.

## 주요 자산군
- **주식**: 높은 수익, 높은 리스크
- **채권**: 안정적 수익, 낮은 리스크
- **현금**: 유동성 확보
- **부동산**: 인플레이션 헤지

## 60/40 포트폴리오
- 주식 60%, 채권 40%
- 전통적인 균형 포트폴리오

## 리밸런싱
정기적으로 원래 비율로 조정하여 리스크를 관리합니다.
            """,
            level=LessonLevel.intermediate,
            order=2,
            estimated_time=20
        ),
    ]
    
    try:
        db.add_all(lessons)
        db.commit()
        print(f"✅ Created {len(lessons)} sample lessons")
    except Exception as e:
        print(f"❌ Error creating lessons: {e}")
        db.rollback()
    finally:
        db.close()

def create_test_user():
    """테스트 사용자 생성"""
    db = SessionLocal()
    
    # 이미 존재하는지 확인
    existing_user = db.query(User).filter(User.email == "test@econolearn.com").first()
    if existing_user:
        print("✅ Test user already exists")
        db.close()
        return
    
    test_user = User(
        email="test@econolearn.com",
        username="테스트 사용자",
        hashed_password=pwd_context.hash("password123"),
        level=UserLevel.intermediate
    )
    
    try:
        db.add(test_user)
        db.commit()
        print("✅ Created test user (email: test@econolearn.com, password: password123)")
    except Exception as e:
        print(f"❌ Error creating test user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🌱 Seeding database...")
    create_sample_lessons()
    create_test_user()
    print("✅ Database seeding complete!")
EOF
```

---

### 샘플 데이터 삽입 실행

```bash
python seed_data.py
```

---

## ✅ 데이터베이스 확인

### PostgreSQL에서 확인

```bash
psql -d econolearn -U postgres

# 테이블 목록 확인
\dt

# users 테이블 확인
SELECT * FROM users;

# lessons 테이블 확인
SELECT id, title, category, level FROM lessons;

# 종료
\q
```

---

## 📊 데이터베이스 스키마 요약

### 테이블 목록

| 테이블 | 설명 | 주요 컬럼 |
|--------|------|-----------|
| users | 사용자 정보 | email, level, created_at |
| lessons | 강의 콘텐츠 | title, content, category, level |
| user_progress | 학습 진도 | user_id, lesson_id, completed, progress |
| daily_streak | 연속 학습 | user_id, current_streak, last_study_date |
| bookmarks | 북마크 | user_id, lesson_id |

---

## 🔧 유용한 데이터베이스 명령어

### 테이블 삭제 및 재생성
```bash
python << 'EOF'
from app.database import engine, Base
from app.models import User, Lesson, UserProgress, DailyStreak, Bookmark

# 모든 테이블 삭제
Base.metadata.drop_all(bind=engine)
print("✅ All tables dropped")

# 테이블 재생성
Base.metadata.create_all(bind=engine)
print("✅ All tables recreated")
EOF
```

### 특정 테이블 데이터 조회
```python
# Python 인터프리터에서
from app.database import SessionLocal
from app.models import Lesson

db = SessionLocal()
lessons = db.query(Lesson).all()
for lesson in lessons:
    print(f"{lesson.id}: {lesson.title}")
db.close()
```

---

## 🐛 트러블슈팅

### 1. 테이블 생성 오류
```bash
# 모델 임포트 오류 확인
python -c "from app.models import User, Lesson"

# 데이터베이스 연결 확인
python -c "from app.database import engine; print(engine)"
```

### 2. 중복 데이터 오류
```bash
# 기존 데이터 삭제
psql -d econolearn -U postgres -c "TRUNCATE TABLE lessons CASCADE;"
```

### 3. 외래키 제약 조건 오류
```bash
# CASCADE로 테이블 삭제
psql -d econolearn -U postgres -c "DROP TABLE IF EXISTS user_progress CASCADE;"
```

---

## ✅ 다음 단계

데이터베이스 설계가 완료되었습니다!

**다음 문서**: [03-backend-api.md](./03-backend-api.md)에서 FastAPI 엔드포인트를 개발합니다.