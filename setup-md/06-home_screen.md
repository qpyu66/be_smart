# 06. 메인 홈 화면 개발

## 📋 목표
- 메인 홈 화면 레이아웃 구현
- 데일리 학습 섹션
- 자유 학습 섹션
- 최근 학습 섹션
- 하단 네비게이션

---

## 🏠 메인 홈 화면 구조

```
┌─────────────────────┐
│  Header (프로필)     │
├─────────────────────┤
│  📅 데일리 학습     │
│  (오늘의 강의)      │
├─────────────────────┤
│  🎯 자유 학습       │
│  (6개 카테고리)     │
├─────────────────────┤
│  📚 최근 학습       │
│  (이어서 하기)      │
├─────────────────────┤
│  하단 네비게이션     │
└─────────────────────┘
```

---

## 📱 Home 컴포넌트

### pages/Home.tsx
```bash
cd frontend/src/pages
cat > Home.tsx << 'EOF'
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { lessonService } from '../services/lessonService';
import { progressService } from '../services/progressService';
import { Lesson, ProgressStats } from '../types';
import Header from '../components/layout/Header';
import DailySection from '../components/home/DailySection';
import FreeLearningSection from '../components/home/FreeLearningSection';
import RecentSection from '../components/home/RecentSection';
import BottomNav from '../components/layout/BottomNav';

const Home: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [dailyLesson, setDailyLesson] = useState<Lesson | null>(null);
  const [stats, setStats] = useState<ProgressStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [lesson, progressStats] = await Promise.all([
        lessonService.getDailyLesson(),
        progressService.getStats(),
      ]);
      setDailyLesson(lesson);
      setStats(progressStats);
    } catch (error) {
      console.error('Failed to fetch data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="text-4xl mb-4">⏳</div>
          <p className="text-gray-600">로딩 중...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      <Header user={user!} />
      
      <div className="max-w-4xl mx-auto px-4 py-6 space-y-6">
        {/* 데일리 학습 */}
        <DailySection 
          lesson={dailyLesson} 
          streak={stats?.current_streak || 0}
          onContinue={() => navigate(`/lesson/daily/${dailyLesson?.id}`)}
        />

        {/* 자유 학습 */}
        <FreeLearningSection />

        {/* 최근 학습 */}
        <RecentSection />
      </div>

      <BottomNav />
    </div>
  );
};

export default Home;
EOF
```

---

## 🎨 컴포넌트 생성

### 1. Header 컴포넌트

```bash
mkdir -p ../components/layout
cat > ../components/layout/Header.tsx << 'EOF'
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { User } from '../../types';

interface HeaderProps {
  user: User;
}

const Header: React.FC<HeaderProps> = ({ user }) => {
  const navigate = useNavigate();

  const getLevelEmoji = (level: string) => {
    switch (level) {
      case 'beginner':
        return '🌱';
      case 'intermediate':
        return '🌿';
      case 'advanced':
        return '🌳';
      default:
        return '🌿';
    }
  };

  const getLevelText = (level: string) => {
    switch (level) {
      case 'beginner':
        return '초급';
      case 'intermediate':
        return '중급';
      case 'advanced':
        return '고급';
      default:
        return '중급';
    }
  };

  return (
    <header className="bg-white shadow-sm">
      <div className="max-w-4xl mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* User Info */}
          <div className="flex items-center space-x-3">
            <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-blue-500 rounded-full flex items-center justify-center text-white text-xl font-bold">
              {getLevelEmoji(user.level)}
            </div>
            <div>
              <h2 className="font-bold text-gray-800">안녕하세요!</h2>
              <p className="text-sm text-gray-600">{getLevelText(user.level)} 학습자</p>
            </div>
          </div>

          {/* Icons */}
          <div className="flex items-center space-x-2">
            <button className="p-2 hover:bg-gray-100 rounded-full transition-colors">
              <span className="text-2xl">🔔</span>
            </button>
            <button
              onClick={() => navigate('/settings')}
              className="p-2 hover:bg-gray-100 rounded-full transition-colors"
            >
              <span className="text-2xl">⚙️</span>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
EOF
```

---

### 2. Daily Section 컴포넌트

```bash
mkdir -p ../components/home
cat > ../components/home/DailySection.tsx << 'EOF'
import React from 'react';
import { Lesson } from '../../types';
import Button from '../common/Button';

interface DailySectionProps {
  lesson: Lesson | null;
  streak: number;
  onContinue: () => void;
}

const DailySection: React.FC<DailySectionProps> = ({ lesson, streak, onContinue }) => {
  if (!lesson) {
    return null;
  }

  return (
    <section className="bg-gradient-to-br from-purple-600 to-blue-500 rounded-2xl p-6 text-white shadow-lg">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-bold">📅 오늘의 학습</h2>
        <div className="bg-white/20 backdrop-blur-sm px-4 py-2 rounded-full">
          <span className="font-semibold">🔥 {streak}일 연속</span>
        </div>
      </div>

      <div className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl p-5">
        <h3 className="text-xl font-bold mb-2">{lesson.title}</h3>
        <div className="flex items-center justify-between text-sm opacity-90 mb-4">
          <span>⏱️ {lesson.estimated_time}분</span>
        </div>
        
        <Button
          onClick={onContinue}
          variant="primary"
          fullWidth
        >
          <span className="bg-white text-purple-600 px-6 py-3 rounded-lg font-semibold w-full block">
            이어서 학습하기 →
          </span>
        </Button>
      </div>
    </section>
  );
};

export default DailySection;
EOF
```

---

### 3. Free Learning Section 컴포넌트

```bash
cat > ../components/home/FreeLearningSection.tsx << 'EOF'
import React from 'react';
import { useNavigate } from 'react-router-dom';

interface Category {
  id: string;
  name: string;
  icon: string;
  route: string;
}

const categories: Category[] = [
  { id: 'economics_basics', name: '경제 기초', icon: '📊', route: '/category/economics_basics' },
  { id: 'financial_market', name: '금융시장', icon: '💹', route: '/category/financial_market' },
  { id: 'investment', name: '투자/재테크', icon: '💰', route: '/category/investment' },
  { id: 'economic_news', name: '경제 뉴스', icon: '📰', route: '/category/economic_news' },
  { id: 'economic_indicators', name: '경제 지표', icon: '📈', route: '/category/economic_indicators' },
  { id: 'financial_statements', name: '재무제표', icon: '📋', route: '/category/financial_statements' },
];

const FreeLearningSection: React.FC = () => {
  const navigate = useNavigate();

  return (
    <section>
      <h2 className="text-2xl font-bold text-gray-800 mb-4">🎯 자유 학습</h2>
      <div className="grid grid-cols-3 gap-4">
        {categories.map((category) => (
          <div
            key={category.id}
            onClick={() => navigate(category.route)}
            className="bg-white p-6 rounded-xl shadow-sm hover:shadow-md transition-all cursor-pointer border-2 border-transparent hover:border-blue-500"
          >
            <div className="text-4xl mb-3 text-center">{category.icon}</div>
            <p className="text-center text-sm font-semibold text-gray-800">{category.name}</p>
          </div>
        ))}
      </div>
    </section>
  );
};

export default FreeLearningSection;
EOF
```

---

### 4. Recent Section 컴포넌트

```bash
cat > ../components/home/RecentSection.tsx << 'EOF'
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { progressService } from '../../services/progressService';
import { lessonService } from '../../services/lessonService';
import { Progress, Lesson } from '../../types';

interface RecentLesson {
  progress: Progress;
  lesson: Lesson;
}

const RecentSection: React.FC = () => {
  const navigate = useNavigate();
  const [recentLessons, setRecentLessons] = useState<RecentLesson[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchRecentLessons();
  }, []);

  const fetchRecentLessons = async () => {
    try {
      const allProgress = await progressService.getAllProgress();
      // 최근 학습한 2개만 가져오기 (완료하지 않은 것 우선)
      const sorted = allProgress
        .filter(p => !p.completed && p.progress > 0)
        .sort((a, b) => b.progress - a.progress)
        .slice(0, 2);

      const lessonsWithProgress = await Promise.all(
        sorted.map(async (progress) => {
          const lesson = await lessonService.getLesson(progress.lesson_id);
          return { progress, lesson };
        })
      );

      setRecentLessons(lessonsWithProgress);
    } catch (error) {
      console.error('Failed to fetch recent lessons:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading || recentLessons.length === 0) {
    return null;
  }

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
    <section>
      <h2 className="text-2xl font-bold text-gray-800 mb-4">📚 최근 학습</h2>
      <div className="bg-white rounded-xl shadow-sm p-4 space-y-3">
        {recentLessons.map(({ progress, lesson }) => (
          <div
            key={lesson.id}
            onClick={() => navigate(`/lesson/free/${lesson.id}`)}
            className="flex items-center p-4 hover:bg-gray-50 rounded-lg cursor-pointer transition-colors"
          >
            <div className="w-14 h-14 bg-blue-100 rounded-xl flex items-center justify-center text-2xl mr-4">
              📖
            </div>
            <div className="flex-1">
              <p className="text-xs text-gray-500 mb-1">
                {getCategoryName(lesson.category)}
              </p>
              <h3 className="font-semibold text-gray-800">{lesson.title}</h3>
              <div className="mt-2 bg-gray-200 rounded-full h-2 overflow-hidden">
                <div
                  className="bg-blue-500 h-full transition-all"
                  style={{ width: `${progress.progress * 100}%` }}
                />
              </div>
            </div>
            <div className="text-gray-400 ml-4">→</div>
          </div>
        ))}
      </div>
    </section>
  );
};

export default RecentSection;
EOF
```

---

### 5. Bottom Navigation 컴포넌트

```bash
cat > ../components/layout/BottomNav.tsx << 'EOF'
import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

const BottomNav: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const navItems = [
    { path: '/home', icon: '🏠', label: '홈' },
    { path: '/lessons', icon: '📚', label: '학습' },
    { path: '/news', icon: '📰', label: '뉴스' },
    { path: '/stats', icon: '📊', label: '통계' },
    { path: '/settings', icon: '👤', label: '마이' },
  ];

  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 shadow-lg">
      <div className="max-w-4xl mx-auto px-4">
        <div className="flex justify-around">
          {navItems.map((item) => {
            const isActive = location.pathname === item.path;
            return (
              <button
                key={item.path}
                onClick={() => navigate(item.path)}
                className={`flex flex-col items-center py-3 px-4 transition-colors ${
                  isActive ? 'text-blue-500' : 'text-gray-500'
                }`}
              >
                <span className="text-2xl mb-1">{item.icon}</span>
                <span className="text-xs font-medium">{item.label}</span>
              </button>
            );
          })}
        </div>
      </div>
    </nav>
  );
};

export default BottomNav;
EOF
```

---

## 🧪 테스트

### 1. 홈 화면 접속
```bash
# 로그인 후 자동으로 /home으로 이동
# 또는 직접 접속: http://localhost:3000/home
```

### 2. 확인 사항
- [ ] 헤더에 사용자 정보 표시
- [ ] 데일리 학습 섹션 표시
- [ ] 스트릭 표시
- [ ] 6개 카테고리 카드 표시
- [ ] 최근 학습 섹션 표시 (진행 중인 강의가 있을 때)
- [ ] 하단 네비게이션 표시
- [ ] 각 버튼 클릭 시 해당 페이지로 이동

---

## 📱 반응형 디자인

### 모바일 최적화
```css
/* Tailwind 클래스를 사용하여 반응형 처리 */
- sm: (640px): 모바일 가로
- md: (768px): 태블릿
- lg: (1024px): 데스크톱

예시:
<div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6">
  {/* 모바일: 2열, 태블릿: 3열, 데스크톱: 6열 */}
</div>
```

---

## 🎨 스타일링 개선

### 그라데이션 추가
```typescript
// Daily Section에 애니메이션 추가
className="bg-gradient-to-br from-purple-600 to-blue-500 rounded-2xl p-6 text-white shadow-lg transform hover:scale-[1.02] transition-transform"
```

### 호버 효과
```typescript
// Category 카드에 호버 효과
className="hover:shadow-xl hover:-translate-y-1 transition-all duration-200"
```

---

## ✅ 체크리스트

- [ ] 헤더가 정상적으로 표시되는가?
- [ ] 데일리 학습 섹션이 작동하는가?
- [ ] 자유 학습 카테고리가 모두 표시되는가?
- [ ] 최근 학습이 표시되는가?
- [ ] 하단 네비게이션이 작동하는가?
- [ ] 각 버튼 클릭 시 올바른 페이지로 이동하는가?
- [ ] 반응형 디자인이 잘 작동하는가?

---

## 🐛 트러블슈팅

### 1. 데일리 강의가 표시되지 않음
```typescript
// Backend 로그 확인
// Frontend console 확인
console.log('Daily lesson:', dailyLesson);
```

### 2. 스트릭이 0으로 표시됨
```bash
# 데이터베이스에서 확인
psql -d econolearn -c "SELECT * FROM daily_streak WHERE user_id = 1;"
```

### 3. 카테고리 클릭 시 페이지가 없음
```typescript
// App.tsx에 라우트 추가 필요
<Route path="/category/:category" element={<CategoryLessons />} />
```

### 4. 최근 학습이 표시되지 않음
```typescript
// 진행 중인 강의가 있는지 확인
const progress = await progressService.getAllProgress();
console.log('Progress:', progress);
```

---

## ✅ 다음 단계

메인 홈 화면 개발이 완료되었습니다!

**다음 문서**: [07-daily-learning.md](./07-daily-learning.md)에서 데일리 학습 기능을 개발합니다.