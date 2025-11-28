# 07. 데일리 학습 기능 개발

## 📋 목표
- 강의 상세 페이지 구현
- 콘텐츠 렌더링 (Markdown)
- 진도 추적 기능
- 다음/이전 강의 네비게이션
- 북마크 기능

---

## 📱 강의 상세 화면 구조

```
┌─────────────────────┐
│  뒤로가기 | 제목     │
├─────────────────────┤
│  강의 정보           │
│  (카테고리, 시간)    │
├─────────────────────┤
│  강의 콘텐츠         │
│  (Markdown)         │
├─────────────────────┤
│  [북마크] [다음]    │
└─────────────────────┘
```

---

## 📝 DailyLesson 컴포넌트

### pages/DailyLesson.tsx
```bash
cd frontend/src/pages
cat > DailyLesson.tsx << 'EOF'
import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { lessonService } from '../services/lessonService';
import { progressService } from '../services/progressService';
import { Lesson, Progress } from '../types';
import LessonHeader from '../components/lesson/LessonHeader';
import LessonContent from '../components/lesson/LessonContent';
import LessonFooter from '../components/lesson/LessonFooter';
import ReactMarkdown from 'react-markdown';

const DailyLesson: React.FC = () => {
  const { lessonId } = useParams<{ lessonId: string }>();
  const navigate = useNavigate();
  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [progress, setProgress] = useState<Progress | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (lessonId) {
      fetchLesson(parseInt(lessonId));
    }
  }, [lessonId]);

  const fetchLesson = async (id: number) => {
    try {
      const [lessonData, progressData] = await Promise.all([
        lessonService.getLesson(id),
        progressService.getLessonProgress(id),
      ]);
      setLesson(lessonData);
      setProgress(progressData);
    } catch (error) {
      console.error('Failed to fetch lesson:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleComplete = async () => {
    if (!lessonId) return;

    try {
      await progressService.updateProgress(parseInt(lessonId), {
        progress: 1.0,
        completed: true,
      });
      
      // 다음 강의로 이동
      navigate('/home');
    } catch (error) {
      console.error('Failed to update progress:', error);
    }
  };

  const handleBookmark = () => {
    // TODO: 북마크 기능 구현
    alert('북마크 기능은 추후 구현됩니다');
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="text-4xl mb-4">⏳</div>
          <p className="text-gray-600">강의를 불러오는 중...</p>
        </div>
      </div>
    );
  }

  if (!lesson) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="text-4xl mb-4">😕</div>
          <p className="text-gray-600">강의를 찾을 수 없습니다</p>
          <button
            onClick={() => navigate('/home')}
            className="mt-4 text-blue-500 hover:underline"
          >
            홈으로 돌아가기
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <LessonHeader
        lesson={lesson}
        onBack={() => navigate('/home')}
      />

      <div className="max-w-3xl mx-auto px-4 py-6">
        <LessonContent lesson={lesson} />
        
        <LessonFooter
          onBookmark={handleBookmark}
          onComplete={handleComplete}
          progress={progress?.progress || 0}
        />
      </div>
    </div>
  );
};

export default DailyLesson;
EOF
```

---

## 🎨 컴포넌트 생성

### 1. Lesson Header

```bash
mkdir -p ../components/lesson
cat > ../components/lesson/LessonHeader.tsx << 'EOF'
import React from 'react';
import { Lesson } from '../../types';

interface LessonHeaderProps {
  lesson: Lesson;
  onBack: () => void;
}

const LessonHeader: React.FC<LessonHeaderProps> = ({ lesson, onBack }) => {
  const getCategoryName = (category: string) => {
    const names: { [key: string]: string } = {
      economics_basics: '경제 기초',
      financial_market: '금융시장',
      investment: '투자/재테크',
      economic_news: '경제 뉴스',
      economic_indicators: '경제 지표',
      financial_statements: '재무제표',
    };
    return names[category] || category;
  };

  return (
    <header className="bg-gradient-to-r from-purple-600 to-blue-500 text-white">
      <div className="max-w-3xl mx-auto px-4 py-6">
        {/* Back Button */}
        <button
          onClick={onBack}
          className="flex items-center text-white/90 hover:text-white mb-4 transition-colors"
        >
          <span className="text-2xl mr-2">←</span>
          <span>뒤로가기</span>
        </button>

        {/* Lesson Info */}
        <div>
          <h1 className="text-2xl md:text-3xl font-bold mb-3">{lesson.title}</h1>
          <div className="flex items-center space-x-4 text-sm opacity-90">
            <span>📚 {getCategoryName(lesson.category)}</span>
            <span>⏱️ {lesson.estimated_time}분</span>
            <span>📝 {lesson.order}강</span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default LessonHeader;
EOF
```

---

### 2. Lesson Content (Markdown 렌더링)

먼저 react-markdown 설치:
```bash
cd ../..  # frontend 디렉토리로
npm install react-markdown
npm install remark-gfm  # GitHub Flavored Markdown
```

컴포넌트 생성:
```bash
cd src/components/lesson
cat > LessonContent.tsx << 'EOF'
import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Lesson } from '../../types';

interface LessonContentProps {
  lesson: Lesson;
}

const LessonContent: React.FC<LessonContentProps> = ({ lesson }) => {
  return (
    <div className="bg-white rounded-2xl shadow-sm p-8 mb-6">
      <article className="prose prose-lg max-w-none">
        <ReactMarkdown
          remarkPlugins={[remarkGfm]}
          components={{
            h1: ({ node, ...props }) => (
              <h1 className="text-3xl font-bold text-gray-900 mt-8 mb-4" {...props} />
            ),
            h2: ({ node, ...props }) => (
              <h2 className="text-2xl font-bold text-gray-800 mt-6 mb-3" {...props} />
            ),
            h3: ({ node, ...props }) => (
              <h3 className="text-xl font-bold text-gray-800 mt-4 mb-2" {...props} />
            ),
            p: ({ node, ...props }) => (
              <p className="text-gray-700 leading-relaxed mb-4" {...props} />
            ),
            ul: ({ node, ...props }) => (
              <ul className="list-disc list-inside space-y-2 mb-4 text-gray-700" {...props} />
            ),
            ol: ({ node, ...props }) => (
              <ol className="list-decimal list-inside space-y-2 mb-4 text-gray-700" {...props} />
            ),
            li: ({ node, ...props }) => (
              <li className="ml-4" {...props} />
            ),
            strong: ({ node, ...props }) => (
              <strong className="font-bold text-gray-900" {...props} />
            ),
            em: ({ node, ...props }) => (
              <em className="italic text-gray-800" {...props} />
            ),
            blockquote: ({ node, ...props }) => (
              <blockquote
                className="border-l-4 border-yellow-400 bg-yellow-50 pl-4 py-2 my-4 italic text-gray-700"
                {...props}
              />
            ),
            code: ({ node, inline, ...props }: any) =>
              inline ? (
                <code className="bg-gray-100 text-red-600 px-2 py-1 rounded text-sm" {...props} />
              ) : (
                <code
                  className="block bg-gray-100 p-4 rounded-lg overflow-x-auto text-sm mb-4"
                  {...props}
                />
              ),
          }}
        >
          {lesson.content}
        </ReactMarkdown>
      </article>

      {/* 핵심 포인트 박스 */}
      <div className="mt-8 bg-blue-50 border-l-4 border-blue-500 p-6 rounded-r-lg">
        <h4 className="font-bold text-blue-900 mb-2">💡 핵심 요약</h4>
        <p className="text-blue-800 text-sm">
          이 강의를 통해 {lesson.title}에 대한 기본 개념을 이해했습니다.
          실생활에서 어떻게 적용할 수 있을지 생각해보세요!
        </p>
      </div>
    </div>
  );
};

export default LessonContent;
EOF
```

---

### 3. Lesson Footer

```bash
cat > LessonFooter.tsx << 'EOF'
import React from 'react';
import Button from '../common/Button';

interface LessonFooterProps {
  onBookmark: () => void;
  onComplete: () => void;
  progress: number;
}

const LessonFooter: React.FC<LessonFooterProps> = ({ onBookmark, onComplete, progress }) => {
  return (
    <div className="bg-white rounded-2xl shadow-sm p-6 sticky bottom-4">
      {/* Progress Bar */}
      <div className="mb-4">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium text-gray-600">학습 진도</span>
          <span className="text-sm font-bold text-blue-600">{Math.round(progress * 100)}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
          <div
            className="bg-blue-500 h-full transition-all duration-300"
            style={{ width: `${progress * 100}%` }}
          />
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex space-x-3">
        <button
          onClick={onBookmark}
          className="flex-1 px-6 py-3 border-2 border-blue-500 text-blue-500 rounded-lg font-semibold hover:bg-blue-50 transition-colors"
        >
          🔖 북마크
        </button>
        <button
          onClick={onComplete}
          className="flex-[2] px-6 py-3 bg-blue-500 text-white rounded-lg font-semibold hover:bg-blue-600 transition-colors"
        >
          완료하고 다음 →
        </button>
      </div>

      {/* Tips */}
      <div className="mt-4 text-center">
        <p className="text-xs text-gray-500">
          💡 스크롤을 끝까지 내려 강의를 완료하세요
        </p>
      </div>
    </div>
  );
};

export default LessonFooter;
EOF
```

---

## 📊 진도 자동 추적

### 스크롤 기반 진도 업데이트

```bash
# DailyLesson.tsx에 추가
cat >> ../../pages/DailyLesson.tsx << 'EOF'

// 컴포넌트 내부에 추가
useEffect(() => {
  const handleScroll = () => {
    const windowHeight = window.innerHeight;
    const documentHeight = document.documentElement.scrollHeight;
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    
    // 진도율 계산 (0.0 ~ 1.0)
    const scrollProgress = Math.min(
      (scrollTop + windowHeight) / documentHeight,
      1.0
    );

    // 진도가 변경되었을 때만 업데이트 (너무 자주 호출되지 않도록)
    if (progress && Math.abs(scrollProgress - progress.progress) > 0.05) {
      updateProgressDebounced(scrollProgress);
    }
  };

  window.addEventListener('scroll', handleScroll);
  return () => window.removeEventListener('scroll', handleScroll);
}, [progress]);

// 디바운스 함수
const updateProgressDebounced = debounce(async (newProgress: number) => {
  if (!lessonId) return;
  try {
    await progressService.updateProgress(parseInt(lessonId), {
      progress: newProgress,
      completed: newProgress >= 0.95,
    });
  } catch (error) {
    console.error('Failed to update progress:', error);
  }
}, 1000);

// 유틸리티 함수
function debounce(func: Function, wait: number) {
  let timeout: NodeJS.Timeout;
  return function executedFunction(...args: any[]) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}
EOF
```

---

## 🧪 테스트

### 1. 강의 상세 페이지 접속
```bash
# 홈에서 "이어서 학습하기" 클릭
# 또는 직접 접속: http://localhost:3000/lesson/daily/1
```

### 2. 확인 사항
- [ ] 강의 제목과 정보가 표시되는가?
- [ ] Markdown 콘텐츠가 올바르게 렌더링되는가?
- [ ] 진도 바가 표시되는가?
- [ ] 스크롤 시 진도가 업데이트되는가?
- [ ] "완료하고 다음" 버튼이 작동하는가?
- [ ] 뒤로가기 버튼이 작동하는가?

---

## 🎨 스타일링 개선

### 코드 블록 하이라이팅 (선택사항)

```bash
npm install react-syntax-highlighter
npm install @types/react-syntax-highlighter --save-dev
```

LessonContent.tsx 업데이트:
```typescript
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

// ReactMarkdown components에 추가
code: ({ node, inline, className, children, ...props }: any) => {
  const match = /language-(\w+)/.exec(className || '');
  return !inline && match ? (
    <SyntaxHighlighter
      style={vscDarkPlus}
      language={match[1]}
      PreTag="div"
      {...props}
    >
      {String(children).replace(/\n$/, '')}
    </SyntaxHighlighter>
  ) : (
    <code className="bg-gray-100 text-red-600 px-2 py-1 rounded text-sm" {...props}>
      {children}
    </code>
  );
}
```

---

## 📱 반응형 최적화

### 모바일에서 읽기 편한 타이포그래피

```css
/* Tailwind prose 커스텀 */
.prose {
  font-size: 16px;
  line-height: 1.75;
}

@media (min-width: 768px) {
  .prose {
    font-size: 18px;
    line-height: 1.8;
  }
}
```

---

## ✅ 체크리스트

- [ ] 강의 상세 페이지가 정상적으로 표시되는가?
- [ ] Markdown이 올바르게 렌더링되는가?
- [ ] 진도 추적이 작동하는가?
- [ ] 완료 버튼이 작동하는가?
- [ ] 뒤로가기가 작동하는가?
- [ ] 반응형 디자인이 잘 작동하는가?

---

## 🐛 트러블슈팅

### 1. Markdown이 렌더링되지 않음
```bash
# react-markdown 설치 확인
npm list react-markdown

# 재설치
npm install react-markdown remark-gfm
```

### 2. 진도가 업데이트되지 않음
```typescript
// Console에서 확인
console.log('Current progress:', progress);
console.log('Scroll progress:', scrollProgress);
```

### 3. 스타일이 깨짐
```bash
# Tailwind typography 플러그인 설치
npm install @tailwindcss/typography

# tailwind.config.js에 추가
plugins: [require('@tailwindcss/typography')]
```

### 4. 완료 버튼이 작동하지 않음
```typescript
// API 응답 확인
const response = await progressService.updateProgress(lessonId, {
  progress: 1.0,
  completed: true,
});
console.log('Update response:', response);
```

---

## ✅ 다음 단계

데일리 학습 기능 개발이 완료되었습니다!

**다음 문서**: [08-free-learning.md](./08-free-learning.md)에서 자유 학습 기능을 개발합니다.