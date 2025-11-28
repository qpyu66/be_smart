# 09. 설정 페이지 개발

## 📋 목표
- 설정 페이지 구현
- 학습 수준 변경 기능
- 프로필 관리
- 로그아웃 기능

---

## ⚙️ Settings 페이지

### pages/Settings.tsx
```bash
cd frontend/src/pages
cat > Settings.tsx << 'EOF'
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

const Settings: React.FC = () => {
  const navigate = useNavigate();
  const { user, logout, updateUserLevel } = useAuth();
  const [selectedLevel, setSelectedLevel] = useState(user?.level || 'intermediate');
  const [showLevelModal, setShowLevelModal] = useState(false);
  const [updating, setUpdating] = useState(false);

  const handleLevelUpdate = async () => {
    setUpdating(true);
    try {
      await updateUserLevel(selectedLevel);
      setShowLevelModal(false);
      alert('학습 수준이 변경되었습니다!');
    } catch (error) {
      console.error('Failed to update level:', error);
      alert('수준 변경에 실패했습니다');
    } finally {
      setUpdating(false);
    }
  };

  const handleLogout = () => {
    if (window.confirm('로그아웃 하시겠습니까?')) {
      logout();
      navigate('/login');
    }
  };

  const getLevelText = (level: string) => {
    const levels: { [key: string]: string } = {
      beginner: '초급',
      intermediate: '중급',
      advanced: '고급',
    };
    return levels[level] || level;
  };

  const getLevelEmoji = (level: string) => {
    const emojis: { [key: string]: string } = {
      beginner: '🌱',
      intermediate: '🌿',
      advanced: '🌳',
    };
    return emojis[level] || '🌿';
  };

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      {/* Header */}
      <header className="bg-gradient-to-r from-purple-600 to-blue-500 text-white">
        <div className="max-w-4xl mx-auto px-4 py-6">
          <button
            onClick={() => navigate('/home')}
            className="flex items-center text-white/90 hover:text-white mb-4"
          >
            <span className="text-2xl mr-2">←</span>
            <span>뒤로가기</span>
          </button>
          <h1 className="text-3xl font-bold">⚙️ 설정</h1>
        </div>
      </header>

      <div className="max-w-4xl mx-auto px-4 py-6">
        {/* Profile Section */}
        <section className="bg-white rounded-2xl shadow-sm p-6 mb-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4">프로필</h2>
          <div className="flex items-center space-x-4">
            <div className="w-20 h-20 bg-gradient-to-br from-purple-500 to-blue-500 rounded-full flex items-center justify-center text-white text-3xl font-bold">
              {getLevelEmoji(user?.level || 'intermediate')}
            </div>
            <div>
              <h3 className="text-lg font-bold text-gray-800">{user?.username}</h3>
              <p className="text-gray-600">{user?.email}</p>
              <p className="text-sm text-gray-500 mt-1">
                가입일: {new Date(user?.created_at || '').toLocaleDateString('ko-KR')}
              </p>
            </div>
          </div>
        </section>

        {/* Learning Settings */}
        <section className="bg-white rounded-2xl shadow-sm p-6 mb-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4">학습 설정</h2>
          <div className="space-y-4">
            {/* Level Setting */}
            <div
              onClick={() => setShowLevelModal(true)}
              className="flex items-center justify-between p-4 bg-blue-50 border-2 border-blue-200 rounded-xl cursor-pointer hover:bg-blue-100 transition-colors"
            >
              <div className="flex items-center space-x-3">
                <span className="text-2xl">{getLevelEmoji(user?.level || 'intermediate')}</span>
                <div>
                  <h3 className="font-bold text-gray-800">학습 수준</h3>
                  <p className="text-sm text-gray-600">
                    현재: {getLevelText(user?.level || 'intermediate')}
                  </p>
                </div>
              </div>
              <span className="text-blue-500">→</span>
            </div>

            {/* Notification (미구현) */}
            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-xl opacity-50">
              <div className="flex items-center space-x-3">
                <span className="text-2xl">🔔</span>
                <div>
                  <h3 className="font-bold text-gray-800">알림 설정</h3>
                  <p className="text-sm text-gray-600">학습 리마인더 관리</p>
                </div>
              </div>
              <span className="text-gray-400">곧 출시</span>
            </div>

            {/* Theme (미구현) */}
            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-xl opacity-50">
              <div className="flex items-center space-x-3">
                <span className="text-2xl">🎨</span>
                <div>
                  <h3 className="font-bold text-gray-800">테마</h3>
                  <p className="text-sm text-gray-600">라이트/다크 모드</p>
                </div>
              </div>
              <span className="text-gray-400">곧 출시</span>
            </div>
          </div>
        </section>

        {/* About */}
        <section className="bg-white rounded-2xl shadow-sm p-6 mb-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4">정보</h2>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-4 hover:bg-gray-50 rounded-lg">
              <span className="text-gray-700">버전</span>
              <span className="text-gray-600">1.0.0</span>
            </div>
            <div className="flex items-center justify-between p-4 hover:bg-gray-50 rounded-lg cursor-pointer">
              <span className="text-gray-700">이용약관</span>
              <span className="text-gray-400">→</span>
            </div>
            <div className="flex items-center justify-between p-4 hover:bg-gray-50 rounded-lg cursor-pointer">
              <span className="text-gray-700">개인정보처리방침</span>
              <span className="text-gray-400">→</span>
            </div>
          </div>
        </section>

        {/* Logout Button */}
        <button
          onClick={handleLogout}
          className="w-full p-4 bg-red-50 text-red-600 font-semibold rounded-xl hover:bg-red-100 transition-colors"
        >
          로그아웃
        </button>
      </div>

      {/* Level Modal */}
      {showLevelModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-2xl p-6 max-w-md w-full">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">학습 수준 변경</h2>
            <p className="text-gray-600 mb-6">
              현재 수준을 변경하면 맞춤형 강의 추천이 조정됩니다
            </p>

            <div className="space-y-3 mb-6">
              <div
                onClick={() => setSelectedLevel('beginner')}
                className={`p-4 border-2 rounded-xl cursor-pointer transition-all ${
                  selectedLevel === 'beginner'
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-blue-300'
                }`}
              >
                <div className="flex items-center">
                  <span className="text-2xl mr-3">🌱</span>
                  <div>
                    <h3 className="font-bold text-gray-800">초급</h3>
                    <p className="text-sm text-gray-600">경제가 처음이에요</p>
                  </div>
                </div>
              </div>

              <div
                onClick={() => setSelectedLevel('intermediate')}
                className={`p-4 border-2 rounded-xl cursor-pointer transition-all ${
                  selectedLevel === 'intermediate'
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-blue-300'
                }`}
              >
                <div className="flex items-center">
                  <span className="text-2xl mr-3">🌿</span>
                  <div>
                    <h3 className="font-bold text-gray-800">중급</h3>
                    <p className="text-sm text-gray-600">기본은 알아요</p>
                  </div>
                </div>
              </div>

              <div
                onClick={() => setSelectedLevel('advanced')}
                className={`p-4 border-2 rounded-xl cursor-pointer transition-all ${
                  selectedLevel === 'advanced'
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-blue-300'
                }`}
              >
                <div className="flex items-center">
                  <span className="text-2xl mr-3">🌳</span>
                  <div>
                    <h3 className="font-bold text-gray-800">고급</h3>
                    <p className="text-sm text-gray-600">심화 학습 원해요</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="flex space-x-3">
              <button
                onClick={() => setShowLevelModal(false)}
                className="flex-1 px-6 py-3 border-2 border-gray-300 text-gray-700 rounded-lg font-semibold hover:bg-gray-50"
                disabled={updating}
              >
                취소
              </button>
              <button
                onClick={handleLevelUpdate}
                className="flex-1 px-6 py-3 bg-blue-500 text-white rounded-lg font-semibold hover:bg-blue-600 disabled:opacity-50"
                disabled={updating}
              >
                {updating ? '변경 중...' : '변경하기'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Settings;
EOF
```

---

## 🧪 테스트

### 1. 설정 페이지 접속
```bash
# 홈 화면에서 설정 아이콘 클릭
# 또는 하단 네비게이션에서 "마이" 클릭
```

### 2. 확인 사항
- [ ] 사용자 프로필 정보가 표시되는가?
- [ ] 학습 수준 변경 모달이 열리는가?
- [ ] 수준 변경이 정상적으로 작동하는가?
- [ ] 로그아웃이 정상적으로 작동하는가?
- [ ] 변경된 수준이 즉시 반영되는가?

---

## 📊 학습 통계 페이지 (추가)

### pages/Stats.tsx
```bash
cat > Stats.tsx << 'EOF'
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { progressService } from '../services/progressService';
import { ProgressStats } from '../types';

const Stats: React.FC = () => {
  const navigate = useNavigate();
  const [stats, setStats] = useState<ProgressStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const data = await progressService.getStats();
      setStats(data);
    } catch (error) {
      console.error('Failed to fetch stats:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-4xl">⏳</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      <header className="bg-gradient-to-r from-purple-600 to-blue-500 text-white">
        <div className="max-w-4xl mx-auto px-4 py-6">
          <button
            onClick={() => navigate('/home')}
            className="flex items-center text-white/90 hover:text-white mb-4"
          >
            <span className="text-2xl mr-2">←</span>
            <span>뒤로가기</span>
          </button>
          <h1 className="text-3xl font-bold">📊 학습 통계</h1>
        </div>
      </header>

      <div className="max-w-4xl mx-auto px-4 py-6 space-y-6">
        {/* Streak */}
        <div className="bg-white rounded-2xl shadow-sm p-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4">🔥 연속 학습</h2>
          <div className="grid grid-cols-2 gap-4">
            <div className="text-center p-6 bg-orange-50 rounded-xl">
              <div className="text-4xl font-bold text-orange-600 mb-2">
                {stats?.current_streak || 0}일
              </div>
              <p className="text-sm text-gray-600">현재 연속</p>
            </div>
            <div className="text-center p-6 bg-purple-50 rounded-xl">
              <div className="text-4xl font-bold text-purple-600 mb-2">
                {stats?.longest_streak || 0}일
              </div>
              <p className="text-sm text-gray-600">최장 연속</p>
            </div>
          </div>
        </div>

        {/* Progress */}
        <div className="bg-white rounded-2xl shadow-sm p-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4">📚 학습 진도</h2>
          <div className="space-y-4">
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-gray-600">완료한 강의</span>
                <span className="font-bold text-blue-600">
                  {stats?.completed_lessons || 0} / {stats?.total_lessons || 0}
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div
                  className="bg-blue-500 h-full rounded-full transition-all"
                  style={{ width: `${(stats?.completion_rate || 0) * 100}%` }}
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4 mt-6">
              <div className="text-center p-4 bg-blue-50 rounded-xl">
                <div className="text-3xl font-bold text-blue-600 mb-1">
                  {stats?.completed_lessons || 0}
                </div>
                <p className="text-sm text-gray-600">완료</p>
              </div>
              <div className="text-center p-4 bg-gray-50 rounded-xl">
                <div className="text-3xl font-bold text-gray-600 mb-1">
                  {(stats?.total_lessons || 0) - (stats?.completed_lessons || 0)}
                </div>
                <p className="text-sm text-gray-600">남은 강의</p>
              </div>
            </div>
          </div>
        </div>

        {/* Achievements (미구현) */}
        <div className="bg-white rounded-2xl shadow-sm p-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4">🏆 성취</h2>
          <div className="text-center py-8 text-gray-500">
            <div className="text-4xl mb-2">🎯</div>
            <p>성취 기능은 곧 추가됩니다</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Stats;
EOF
```

---

## 🔄 App.tsx 업데이트

```typescript
// Stats 페이지 import 추가
import Stats from './pages/Stats';

// Route 추가
<Route
  path="/stats"
  element={
    <ProtectedRoute>
      <Stats />
    </ProtectedRoute>
  }
/>
```

---

## ✅ 체크리스트

- [ ] 설정 페이지가 정상적으로 표시되는가?
- [ ] 프로필 정보가 표시되는가?
- [ ] 학습 수준 변경이 작동하는가?
- [ ] 로그아웃이 작동하는가?
- [ ] 통계 페이지가 작동하는가?
- [ ] 반응형 디자인이 잘 작동하는가?

---

## 🐛 트러블슈팅

### 1. 수준 변경이 적용되지 않음
```typescript
// AuthContext에서 updateUserLevel 확인
console.log('Updating level to:', level);
```

### 2. 통계가 표시되지 않음
```typescript
// Backend API 응답 확인
const stats = await progressService.getStats();
console.log('Stats:', stats);
```

### 3. 로그아웃 후 리다이렉트 안됨
```typescript
// AuthContext logout 함수 확인
localStorage.removeItem('token');
```

---

## ✅ 다음 단계

설정 페이지 개발이 완료되었습니다!

**다음 문서**: [10-deployment.md](./10-deployment.md)에서 배포 방법을 알아봅니다.