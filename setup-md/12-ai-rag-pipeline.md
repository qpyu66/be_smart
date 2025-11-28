# 12. 데이터 파이프라인 & RAG (AI 기능) 설계

## 📋 개요
이 프로젝트에 **데이터 파이프라인**과 **RAG (Retrieval-Augmented Generation, 검색 증강 생성)** 기술을 도입하여 앱을 고도화하는 방안입니다.

---

## 🔄 1. 데이터 파이프라인 (Automated News Pipeline)

경제 뉴스를 자동으로 수집, 처리, 요약하여 사용자에게 제공하는 ETL(Extract, Transform, Load) 파이프라인입니다.

### 1.1 아키텍처
```mermaid
graph LR
    A[뉴스 소스 (RSS/API)] -->|Extract| B(수집기 Worker)
    B -->|Transform| C{AI 프로세서}
    C -->|요약 & 키워드 추출| D[LLM (GPT/Gemini)]
    D -->|Load| E[(PostgreSQL)]
    E -->|Serve| F[사용자 앱]
```

### 1.2 기술 스택
- **Scheduler**: Celery + Redis 또는 APScheduler (Python)
- **External API**: Naver News API, Google News RSS
- **AI Processing**: OpenAI API 또는 LangChain
- **Database**: PostgreSQL (기존 DB 활용)

### 1.3 구현 단계
1. **수집 (Extract)**: 매일 오전 8시, 주요 경제 언론사의 RSS/API를 통해 최신 뉴스 메타데이터 수집
2. **정제 (Transform 1)**: 본문 스크래핑 및 불필요한 HTML 태그 제거
3. **AI 분석 (Transform 2)**:
   - **요약**: "이 기사를 3줄로 요약해줘"
   - **키워드 추출**: "이 기사의 핵심 경제 용어 5개를 뽑아줘"
   - **난이도 분류**: "이 기사의 경제 지식 요구 수준을 상/중/하로 평가해줘"
4. **저장 (Load)**: `news` 테이블에 원본 링크, 요약본, 추출된 키워드 저장

---

## 🧠 2. RAG 기반 AI 튜터 (AI Tutor)

단순한 챗봇이 아니라, **우리 앱의 학습 콘텐츠(강의 자료)**를 기반으로 정확하게 답변하는 AI 튜터입니다.

### 2.1 왜 RAG인가?
- 일반 LLM은 최신 경제 지식이나 우리 앱의 커리큘럼 순서를 모릅니다.
- RAG를 사용하면 **"검증된 우리 강의 자료"**를 근거로 답변하므로 환각(Hallucination) 현상을 줄이고 교육적 일관성을 유지할 수 있습니다.

### 2.2 아키텍처
```mermaid
graph TD
    subgraph "데이터 준비 (Indexing)"
    A[강의 콘텐츠 (Markdown)] -->|Chunking| B[텍스트 조각]
    B -->|Embedding| C[Vector]
    C -->|Store| D[(Vector DB / pgvector)]
    end

    subgraph "서비스 (Retrieval & Generation)"
    E[사용자 질문] -->|Embedding| F[질문 Vector]
    F <-->|Similarity Search| D
    D -->|관련 강의 내용 반환| G[Context]
    G + E -->|Prompt| H[LLM]
    H -->|Answer| I[답변 생성]
    end
```

### 2.3 기술 스택
- **Vector DB**: `pgvector` (PostgreSQL 확장기능 사용 - 별도 DB 구축 불필요)
- **Framework**: LangChain 또는 LlamaIndex
- **Embedding Model**: OpenAI `text-embedding-3-small`
- **LLM**: GPT-4o-mini 또는 Gemini Flash

### 2.4 구현 시나리오
1. **사용자 질문**: "금리가 오르면 왜 주식이 떨어져?"
2. **검색 (Retrieval)**: DB에서 '금리', '주식', '상관관계' 관련 강의 챕터를 검색
3. **생성 (Generation)**:
   > "사용자가 '금리와 주식'에 대해 물었습니다.
   > 다음은 우리 앱의 '금융시장 기초' 강의 내용입니다: [검색된 내용...]
   > 이 내용을 바탕으로 초보자도 이해하기 쉽게 설명해주세요."
4. **답변**: 우리 강의 내용을 인용하여 친절하게 설명 + "더 자세한 내용은 3강. 금융시장 이해를 참고하세요"라고 추천 링크 제공

---

## 🚀 3. 추천 구현 순서

1. **뉴스 파이프라인 구축 (난이도: 중)**
   - 외부 API 연동 경험 및 백그라운드 작업 처리 학습에 좋음
   - 사용자에게 매일 새로운 콘텐츠를 제공하여 리텐션(재방문) 증가

2. **RAG AI 튜터 구축 (난이도: 상)**
   - 벡터 데이터베이스와 임베딩 개념 학습 필요
   - 앱의 핵심 차별화 포인트가 될 수 있음

---

## 📝 데이터베이스 스키마 추가 (예시)

### News 테이블
```sql
CREATE TABLE news (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    original_link VARCHAR(500),
    summary TEXT,
    difficulty VARCHAR(20), -- 'beginner', 'intermediate', 'advanced'
    published_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Vector Store (pgvector)
```sql
-- pgvector 확장 설치 필요
CREATE EXTENSION vector;

CREATE TABLE lesson_embeddings (
    id SERIAL PRIMARY KEY,
    lesson_id INTEGER REFERENCES lessons(id),
    content_chunk TEXT,
    embedding vector(1536) -- OpenAI 임베딩 차원 수
);
```
