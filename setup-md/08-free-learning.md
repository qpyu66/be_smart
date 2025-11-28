# 08. 자유 학습 기능 개발

## 📋 목표
- 카테고리별 강의 목록 페이지
- 자유 학습 강의 상세 페이지
- 강의 검색 기능
- 난이도별 필터링

---

## 📱 화면 구조

1. **카테고리 목록** - 6개 카테고리
2. **강의 목록** - 선택한 카테고리의 강의들
3. **강의 상세** - 개별 강의 콘텐츠

---

## 📚 카테고리별 강의 목록

### pages/CategoryLessons.tsx
```bash
cd frontend/src/pages
cat > CategoryLessons.tsx << 'EOF'
import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { lessonService } from '../services/lessonService';
import { Lesson } from '../types';
import { useAuth } from '../hooks/useAuth';

const CategoryLessons: React.FC = () => {
  const { category } = useParams<{ category: string }>();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [filteredLessons, setFilteredLessons] = useState<Lesson[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedLevel, setSelectedLevel] = useState<string>('all');

  useEffect(() => {
    if (category) {
      fetchLessons();
    }
  }, [category]);

  useEffect(() => {
    filterLessons();
  }, [lessons, selectedLevel]);

  const fetchLessons = async () => {
    try {
      const data = await lessonService.getLessonsByCategory(category!);
      setLessons(data);
    } catch (error) {
      console.error('Failed to fetch lessons:', error);
    } finally {
      setLoading(false);
    }
  };

  const filterLessons = () => {
    if (selectedLevel === 'all') {
      setFilteredLessons(lessons);
    } else {
      setFilteredLessons(lessons.filter(lesson => lesson.level === selectedLevel));
    }
  };

  const getCategoryInfo = (cat: string) => {
    const info: { [key: string]: { name: string; icon: string; description: string } } = {
      economics_basics: {
        name: '경제 기초',
        icon: '📊',
        description: '경제학의 기본 개념과 원리를 배웁니다'
      },
      financial_market: {
        name: '금융시장',
        icon: '💹',
        description: '주식, 채권 등 금융시장의 작동 원리를 이해합니다'
      },
      investment: {
        name: '투자/재테크',
        icon: '💰',
        description: '현명한 투자와 재테크 전략을 학습합니다'
      },
      economic_news: {
        name: '경제 뉴스',
        icon: '📰',
        description: '경제 뉴스를 읽고 분석하는 방법을 배웁니다'
      },
      economic_indicators: {
        name: '경제 지표',
        icon: '📈',
        description: 'GDP, 인플레이션 등 주요 경제 지표를 이해합니다'
      },
      financial_statements: {
        name: '재무제표',
        icon: '📋',
        description: '기업의 재무제표를 읽고 분석하는 방법을 배웁니다'
      }
    };
    return info[cat] || { name: cat, icon: '📚', description: '' };
  };

  const getLevelText = (level: string) => {
    const levels: { [key: string]: string } = {
      beginner: '초급',
      intermediate: '중급',
      advanced: '고급',
    };
    return levels[level] || level;
  };

  const getLevelColor = (level: string) => {
    const colors: { [key: string]: string } = {
      beginner: 'bg-green-100 text-green-800',
      intermediate: 'bg-blue-100 text-blue-800',
      advanced: 'bg-purple-100 text-purple-800',
    };
    return colors[level] || 'bg-gray-100 text-gray-800';
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

  const categoryInfo = getCategoryInfo(category!);

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      {/* Header */}
      <header className="bg-gradient-to-r from-purple-600 to-blue-500 text-white">
        <div className="max-w-4xl mx-auto px-4 py-6">
          <button
            onClick={() => navigate('/home')}
            className="flex items-center text-white/90 hover:text-white mb-4 transition-colors"
          >
            <span className="text-2xl mr-2">←</span>
            <span>뒤로가기</span>
          </button>

          <div className="flex items-center mb-3">
            <span className="text-5xl mr-4">{categoryInfo.icon}</span>
            <div>
              <h1 className="text-3xl font-bold">{categoryInfo.name}</h1>
              <p className="text-white/90 mt-1">{categoryInfo.description}</p>
            </div>
          </div>

          <div className="mt-4 text-sm opacity-90">
            총 {filteredLessons.length}개 강의
          </div>
        </div>
      </header>

      {/* Filter */}
      <div className="max-w-4xl mx-auto px-4 py-4">
        <div className="bg-white rounded-lg shadow-sm p-4 mb-4">
          <div className="flex items-center space-x-2">
            <span className="text-sm font-medium text-gray-700">난이도:</span>
            <button
              onClick={() => setSelectedLevel('all')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                selectedLevel === 'all'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              전체
            </button>
            <button
              onClick={() => setSelectedLevel('beginner')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                selectedLevel === 'beginner'
                  ? 'bg-green-500 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              초급
            </button>
            <button
              onClick={() => setSelectedLevel('intermediate')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                selectedLevel === 'intermediate'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              중급
            </button>
            <button
              onClick={() => setSelectedLevel('advanced')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                selectedLevel === 'advanced'
                  ? 'bg-purple-500 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              고급
            </button>
          </div>
        </div>

        {/* Lessons List */}
        <div className="space-y-3">
          {filteredLessons.length === 0 ? (
            <div className="bg-white rounded-lg shadow-sm p-8 text-center">
              <div className="text-4xl mb-4">😕</div>
              <p className="text-gray-600">선택한 난이도의 강의가 없습니다</p>
            </div>
          ) : (
            filteredLessons.map((lesson) => (
              <div
                key={lesson.id}
                onClick={() => navigate(`/lesson/free/${lesson.id}`)}
                className="bg-white rounded-lg shadow-sm hover:shadow-md transition-all cursor-pointer p-5 border-2 border-transparent hover:border-blue-500"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-2">
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${getLevelColor(lesson.level)}`}>
                        {getLevelText(lesson.level)}
                      </span>
                      <span className="text-xs text-gray-500">
                        {lesson.order}강
                      </span>
                    </div>
                    <h3 className="text-lg font-bold text-gray-800 mb-2">
                      {lesson.title}
                    </h3>
                    <div className="flex items-center space-x-4 text-sm text-gray-600">
                      <span>⏱️ {lesson.estimated_time}분</span>
                    </div>
                  </div>
                  <div className="text-gray-400 text-2xl">→</div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default CategoryLessons;
EOF
```

---

## 📖 자유 학습 강의 상세

### pages/FreeLesson.tsx
```bash
cat > FreeLesson.tsx << 'EOF'
import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { lessonService } from '../services/lessonService';
import { progressService } from '../services/progressService';
import { Lesson, Progress } from '../types';
import LessonHeader from '../components/lesson/LessonHeader';
import LessonContent from '../components/lesson/LessonContent';
import Button from '../components/common/Button';

const FreeLesson: React.FC = () => {
  const { lessonId } = useParams<{ lessonId: string }>();
  const navigate = useNavigate();
  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [progress, setProgress] = useState<Progress | null>(null);
  const [allLessons, setAllLessons] = useState<Lesson[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (lessonId) {
      fetchLesson(parseInt(lessonId));
    }
  }, [lessonId]);

  const fetchLesson = async (id: number) => {
    try {
      const lessonData = await lessonService.getLesson(id);
      const progressData = await progressService.getLessonProgress(id);
      const categoryLessons = await lessonService.getLessonsByCategory(lessonData.category);

      setLesson(lessonData);
      setProgress(progressData);
      setAllLessons(categoryLessons);
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

      // 다음 강의 찾기
      const currentIndex = allLessons.findIndex(l => l.id === parseInt(lessonId));
      if (currentIndex < allLessons.length - 1) {
        const nextLesson = allLessons[currentIndex + 1];
        navigate(`/lesson/free/${nextLesson.id}`);
      } else {
        navigate(`/category/${lesson?.category}`);
      }
    } catch (error) {
      console.error('Failed to update progress:', error);
    }
  };

  const goToNextLesson = () => {
    const currentIndex = allLessons.findIndex(l => l.id === parseInt(lessonId!));
    if (currentIndex < allLessons.length - 1) {
      const nextLesson = allLessons[currentIndex + 1];
      navigate(`/lesson/free/${nextLesson.id}`);
    }
  };

  const goToPrevLesson = () => {
    const currentIndex = allLessons.findIndex(l => l.id === parseInt(lessonId!));
    if (currentIndex > 0) {
      const prevLesson = allLessons[currentIndex - 1];
      navigate(`/lesson/free/${prevLesson.id}`);
    }
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
        </div>
      </div>
    );
  }

  const currentIndex = allLessons.findIndex(l => l.id === parseInt(lessonId!));
  const hasNext = currentIndex < allLessons.length - 1;
  const hasPrev = currentIndex > 0;

  return (
    <div className="min-h-screen bg-gray-50">
      <LessonHeader
        lesson={lesson}
        onBack={() => navigate(`/category/${lesson.category}`)}
      />

      <div className="max-w-3xl mx-auto px-4 py-6">
        <LessonContent lesson={lesson} />

        {/* Navigation */}
        <div className="bg-white rounded-2xl shadow-sm p-6 mt-6">
          {/* Progress */}
          <div className="mb-6">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-gray-600">학습 진도</span>
              <span className="text-sm font-bold text-blue-600">
                {Math.round((progress?.progress || 0) * 100)}%
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-blue-500 h-full rounded-full transition-all"
                style={{ width: `${(progress?.progress || 0) * 100}%` }}
              />
            </div>
          </div>

          {/* Buttons */}
          <div className="flex space-x-3">
            {hasPrev && (
              <button
                onClick={goToPrevLesson}
                className="flex-1 px-6 py-3 border-2 border-blue-500 text-blue-500 rounded-lg font-semibold hover:bg-blue-50 transition-colors"
              >
                ← 이전 강의
              </button>
            )}
            {hasNext ? (
              <button
                onClick={handleComplete}
                className="flex-1 px-6 py-3 bg-blue-500 text-white rounded-lg font-semibold hover:bg-blue-600 transition-colors"
              >
                다음 강의 →
              </button>
            ) : (
              <button
                onClick={handleComplete}
                className="flex-1 px-6 py-3 bg-green-500 text-white rounded-lg font-semibold hover:bg-green-600 transition-colors"
              >
                ✓ 강의 완료
              </button>
            )}
          </div>

          {/* Lesson Navigation */}
          <div className="mt-6 pt-6 border-t border-gray-200">
            <h4 className="text-sm font-semibold text-gray-700 mb-3">
              이 카테고리의 다른 강의
            </h4>
            <div className="space-y-2">
              {allLessons.slice(0, 3).map((l) => (
                <button
                  key={l.id}
                  onClick={() => navigate(`/lesson/free/${l.id}`)}
                  className={`w-full text-left p-3 rounded-lg transition-colors ${
                    l.id === parseInt(lessonId!)
                      ? 'bg-blue-50 border-2 border-blue-500'
                      : 'bg-gray-50 hover:bg-gray-100'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-gray-800">
                      {l.order}. {l.title}
                    </span>
                    {l.id === parseInt(lessonId!) && (
                      <span className="text-xs text-blue-600 font-semibold">현재</span>
                    )}
                  </div>
                </button>
              ))}
              {allLessons.length > 3 && (
                <button
                  onClick={() => navigate(`/category/${lesson.category}`)}
                  className="w-full text-center p-2 text-sm text-blue-500 hover:bg-blue-50 rounded-lg transition-colors"
                >
                  전체 강의 보기 ({allLessons.length}개) →
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FreeLesson;
EOF
```

---

## 🔄 App.tsx 라우트 추가

```bash
cd ..
# App.tsx에 라우트 추가
cat >> App.tsx << 'EOF'

// Import 추가
import CategoryLessons from './pages/CategoryLessons';

// Routes에 추가 (ProtectedRoute 내부)
<Route
  path="/category/:category"
  element={
    <ProtectedRoute>
      <CategoryLessons />
    </ProtectedRoute>
  }
/>
EOF
```

---

## 🧪 테스트

### 1. 카테고리 목록에서 접속
```bash
# 홈 화면에서 카테고리 카드 클릭
# 예: http://localhost:3000/category/investment
```

### 2. 확인 사항
- [ ] 카테고리 정보가 표시되는가?
- [ ] 강의 목록이 표시되는가?
- [ ] 난이도 필터가 작동하는가?
- [ ] 강의 클릭 시 상세 페이지로 이동하는가?
- [ ] 이전/다음 강의 네비게이션이 작동하는가?
- [ ] 진도가 저장되는가?

---

## ✅ 체크리스트

- [ ] 카테고리별 강의 목록이 표시되는가?
- [ ] 난이도 필터가 작동하는가?
- [ ] 강의 상세 페이지가 작동하는가?
- [ ] 이전/다음 강의 이동이 작동하는가?
- [ ] 진도 추적이 작동하는가?
- [ ] 반응형 디자인이 잘 작동하는가?

---

## 🐛 트러블슈팅

### 1. 강의 목록이 표시되지 않음
```typescript
// Console 확인
console.log('Fetched lessons:', lessons);
console.log('Category:', category);
```

### 2. 필터가 작동하지 않음
```typescript
// 필터링 로직 확인
console.log('Selected level:', selectedLevel);
console.log('Filtered lessons:', filteredLessons);
```

### 3. 다음 강의로 이동 안됨
```typescript
// 현재 인덱스 확인
console.log('Current index:', currentIndex);
console.log('All lessons:', allLessons);
```

---

## ✅ 다음 단계

자유 학습 기능 개발이 완료되었습니다!

**다음 문서**: [09-settings.md](./09-settings.md)에서 설정 페이지를 개발합니다.