# 05. 온보딩 화면 개발

## 📋 목표
- 환영 화면 구현
- 수준 선택 화면 구현
- 회원가입/로그인 화면 구현
- 온보딩 플로우 완성

---

## 🎨 화면 구성

1. **환영 화면** - 앱 소개
2. **수준 선택** - 초급/중급/고급
3. **회원가입** - 이메일, 비밀번호, 이름
4. **로그인** - 이메일, 비밀번호

---

## 📱 환영 화면 (Welcome)

### pages/Onboarding.tsx
```bash
cd frontend/src/pages
cat > Onboarding.tsx << 'EOF'
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '../components/common/Button';

const Onboarding: React.FC = () => {
  const navigate = useNavigate();
  const [step, setStep] = useState<'welcome' | 'level'>('welcome');
  const [selectedLevel, setSelectedLevel] = useState<string>('intermediate');

  const handleStart = () => {
    setStep('level');
  };

  const handleLevelSelect = (level: string) => {
    setSelectedLevel(level);
  };

  const handleComplete = () => {
    // 레벨 정보를 저장하고 회원가입으로 이동
    localStorage.setItem('selected_level', selectedLevel);
    navigate('/register');
  };

  if (step === 'welcome') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-600 to-blue-500 flex items-center justify-center p-4">
        <div className="max-w-md w-full bg-white rounded-3xl shadow-2xl p-8">
          {/* Logo */}
          <div className="text-center mb-8">
            <div className="text-6xl mb-4">💰</div>
            <h1 className="text-4xl font-bold text-gray-800 mb-2">EconoLearn</h1>
            <p className="text-gray-600">경제, 쉽고 재미있게!</p>
          </div>

          {/* Features */}
          <div className="space-y-4 mb-8">
            <div className="bg-blue-50 p-4 rounded-lg">
              <p className="text-blue-800">✓ 데일리 학습으로 꾸준히</p>
            </div>
            <div className="bg-blue-50 p-4 rounded-lg">
              <p className="text-blue-800">✓ 원하는 주제 자유롭게</p>
            </div>
            <div className="bg-blue-50 p-4 rounded-lg">
              <p className="text-blue-800">✓ 실시간 경제 뉴스 분석</p>
            </div>
          </div>

          {/* Button */}
          <Button onClick={handleStart} fullWidth>
            시작하기
          </Button>
        </div>
      </div>
    );
  }

  // Level Selection
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 to-blue-500 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-3xl shadow-2xl p-8">
        <h2 className="text-3xl font-bold text-center text-gray-800 mb-4">
          현재 경제 지식 수준은?
        </h2>
        <p className="text-center text-gray-600 mb-8">
          걱정마세요, 나중에 언제든 변경 가능해요!
        </p>

        <div className="space-y-4 mb-8">
          {/* Beginner */}
          <div
            onClick={() => handleLevelSelect('beginner')}
            className={`p-6 border-2 rounded-xl cursor-pointer transition-all ${
              selectedLevel === 'beginner'
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-200 hover:border-blue-300'
            }`}
          >
            <div className="flex items-start">
              <div className="text-3xl mr-4">🌱</div>
              <div className="flex-1">
                <h3 className="font-bold text-lg text-gray-800 mb-1">
                  초급 - 경제가 처음이에요
                </h3>
                <p className="text-sm text-gray-600">
                  경제 용어가 생소하고 기본 개념부터 차근차근 배우고 싶어요
                </p>
              </div>
            </div>
          </div>

          {/* Intermediate */}
          <div
            onClick={() => handleLevelSelect('intermediate')}
            className={`p-6 border-2 rounded-xl cursor-pointer transition-all ${
              selectedLevel === 'intermediate'
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-200 hover:border-blue-300'
            }`}
          >
            <div className="flex items-start">
              <div className="text-3xl mr-4">🌿</div>
              <div className="flex-1">
                <h3 className="font-bold text-lg text-gray-800 mb-1">
                  중급 - 기본은 알아요
                </h3>
                <p className="text-sm text-gray-600">
                  뉴스에서 나오는 경제 용어는 알지만, 깊이 있는 이해와 실전 적용을 배우고 싶어요
                </p>
              </div>
            </div>
          </div>

          {/* Advanced */}
          <div
            onClick={() => handleLevelSelect('advanced')}
            className={`p-6 border-2 rounded-xl cursor-pointer transition-all ${
              selectedLevel === 'advanced'
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-200 hover:border-blue-300'
            }`}
          >
            <div className="flex items-start">
              <div className="text-3xl mr-4">🌳</div>
              <div className="flex-1">
                <h3 className="font-bold text-lg text-gray-800 mb-1">
                  고급 - 심화 학습 원해요
                </h3>
                <p className="text-sm text-gray-600">
                  경제 이론을 알고 있어서 실전 투자, 정책 분석 등 고급 내용을 배우고 싶어요
                </p>
              </div>
            </div>
          </div>
        </div>

        <Button onClick={handleComplete} fullWidth>
          완료
        </Button>
      </div>
    </div>
  );
};

export default Onboarding;
EOF
```

---

## 📝 회원가입 화면

### pages/Register.tsx
```bash
cat > Register.tsx << 'EOF'
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import Input from '../components/common/Input';
import Button from '../components/common/Button';

const Register: React.FC = () => {
  const navigate = useNavigate();
  const { register } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const [formData, setFormData] = useState({
    email: '',
    username: '',
    password: '',
    confirmPassword: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    setError('');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // 유효성 검사
    if (formData.password !== formData.confirmPassword) {
      setError('비밀번호가 일치하지 않습니다');
      return;
    }

    if (formData.password.length < 8) {
      setError('비밀번호는 8자 이상이어야 합니다');
      return;
    }

    setLoading(true);

    try {
      const selectedLevel = localStorage.getItem('selected_level') || 'intermediate';
      await register(formData.email, formData.username, formData.password, selectedLevel);
      localStorage.removeItem('selected_level');
      navigate('/home');
    } catch (err: any) {
      setError(err.response?.data?.detail || '회원가입에 실패했습니다');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 to-blue-500 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-3xl shadow-2xl p-8">
        <div className="text-center mb-8">
          <div className="text-5xl mb-4">💰</div>
          <h1 className="text-3xl font-bold text-gray-800 mb-2">회원가입</h1>
          <p className="text-gray-600">EconoLearn에 오신 것을 환영합니다</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            label="이메일"
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="example@email.com"
            required
          />

          <Input
            label="이름"
            type="text"
            name="username"
            value={formData.username}
            onChange={handleChange}
            placeholder="홍길동"
            required
          />

          <Input
            label="비밀번호"
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            placeholder="8자 이상"
            required
          />

          <Input
            label="비밀번호 확인"
            type="password"
            name="confirmPassword"
            value={formData.confirmPassword}
            onChange={handleChange}
            placeholder="비밀번호 재입력"
            required
          />

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg text-sm">
              {error}
            </div>
          )}

          <Button type="submit" fullWidth disabled={loading}>
            {loading ? '회원가입 중...' : '회원가입'}
          </Button>
        </form>

        <p className="text-center text-gray-600 mt-6">
          이미 계정이 있으신가요?{' '}
          <Link to="/login" className="text-blue-500 font-semibold hover:underline">
            로그인
          </Link>
        </p>
      </div>
    </div>
  );
};

export default Register;
EOF
```

---

## 🔐 로그인 화면

### pages/Login.tsx
```bash
cat > Login.tsx << 'EOF'
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import Input from '../components/common/Input';
import Button from '../components/common/Button';

const Login: React.FC = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    setError('');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await login(formData.email, formData.password);
      navigate('/home');
    } catch (err: any) {
      setError(err.response?.data?.detail || '로그인에 실패했습니다');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 to-blue-500 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-3xl shadow-2xl p-8">
        <div className="text-center mb-8">
          <div className="text-5xl mb-4">💰</div>
          <h1 className="text-3xl font-bold text-gray-800 mb-2">로그인</h1>
          <p className="text-gray-600">다시 만나서 반가워요!</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            label="이메일"
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="example@email.com"
            required
          />

          <Input
            label="비밀번호"
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            placeholder="비밀번호"
            required
          />

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg text-sm">
              {error}
            </div>
          )}

          <Button type="submit" fullWidth disabled={loading}>
            {loading ? '로그인 중...' : '로그인'}
          </Button>
        </form>

        <div className="mt-6 space-y-2">
          <p className="text-center text-gray-600">
            계정이 없으신가요?{' '}
            <Link to="/onboarding" className="text-blue-500 font-semibold hover:underline">
              회원가입
            </Link>
          </p>
        </div>

        {/* 테스트 계정 안내 */}
        <div className="mt-8 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
          <p className="text-sm text-yellow-800 font-semibold mb-2">🧪 테스트 계정</p>
          <p className="text-xs text-yellow-700">
            이메일: test@econolearn.com<br />
            비밀번호: password123
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
EOF
```

---

## 🧪 테스트

### 1. 개발 서버 실행
```bash
# Frontend
cd frontend
npm start

# Backend (다른 터미널)
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

### 2. 온보딩 플로우 테스트

1. http://localhost:3000/onboarding 접속
2. "시작하기" 클릭
3. 학습 수준 선택
4. "완료" 클릭 → 회원가입 화면으로 이동
5. 회원정보 입력 후 가입
6. 자동 로그인 → 홈으로 이동

### 3. 로그인 테스트

1. http://localhost:3000/login 접속
2. 테스트 계정으로 로그인
   - 이메일: test@econolearn.com
   - 비밀번호: password123
3. 홈으로 이동 확인

---

## 🎨 스타일링 개선 (선택사항)

### Tailwind 커스텀 설정

```bash
# tailwind.config.js에 추가 설정
cat >> ../../tailwind.config.js << 'EOF'

module.exports = {
  // ... 기존 설정
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        },
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
    },
  },
}
EOF
```

---

## ✅ 체크리스트

- [ ] 환영 화면이 정상적으로 표시되는가?
- [ ] 수준 선택이 정상적으로 작동하는가?
- [ ] 회원가입이 정상적으로 완료되는가?
- [ ] 로그인 후 홈으로 리다이렉트되는가?
- [ ] 에러 메시지가 적절히 표시되는가?
- [ ] 반응형 디자인이 잘 작동하는가?

---

## 🐛 트러블슈팅

### 1. 회원가입 실패
```bash
# Backend 로그 확인
# 터미널에서 FastAPI 서버 로그 확인

# 데이터베이스 연결 확인
psql -d econolearn -c "SELECT * FROM users;"
```

### 2. 로그인 후 리다이렉트 안됨
```typescript
// AuthContext.tsx에서 토큰 저장 확인
console.log('Token saved:', localStorage.getItem('token'));
```

### 3. CORS 에러
```python
# backend/app/main.py에서 CORS 설정 확인
allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"]
```

### 4. 스타일이 적용 안됨
```bash
# Tailwind CSS가 포함되었는지 확인
# src/index.css 상단에 있어야 함:
# @tailwind base;
# @tailwind components;
# @tailwind utilities;
```

---

## ✅ 다음 단계

온보딩 화면 개발이 완료되었습니다!

**다음 문서**: [06-home-screen.md](./06-home-screen.md)에서 메인 홈 화면을 개발합니다.