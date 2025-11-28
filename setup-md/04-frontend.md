# 04. Frontend 구조 설정 (React + TypeScript)

## 📋 목표
- React 프로젝트 구조 설정
- TypeScript 타입 정의
- API 서비스 레이어 구축
- Context API 설정
- 라우팅 설정

---

## 📁 디렉토리 구조

```
frontend/src/
├── components/          # 재사용 컴포넌트
│   ├── common/         # 공통 컴포넌트
│   ├── layout/         # 레이아웃 컴포넌트
│   └── ...
├── pages/              # 페이지 컴포넌트
│   ├── Onboarding.tsx
│   ├── Home.tsx
│   ├── DailyLesson.tsx
│   └── ...
├── context/            # Context API
│   └── AuthContext.tsx
├── services/           # API 서비스
│   ├── api.ts
│   ├── authService.ts
│   └── lessonService.ts
├── hooks/              # Custom Hooks
│   └── useAuth.ts
├── types/              # TypeScript 타입
│   └── index.ts
├── utils/              # 유틸리티 함수
│   └── storage.ts
├── App.tsx
└── index.tsx
```

---

## 🔧 TypeScript 타입 정의

### types/index.ts
```bash
cd frontend/src
mkdir types
cat > types/index.ts << 'EOF'
// User Types
export interface User {
  id: number;
  email: string;
  username: string;
  level: UserLevel;
  created_at: string;
}

export type UserLevel = 'beginner' | 'intermediate' | 'advanced';

export interface RegisterData {
  email: string;
  username: string;
  password: string;
  level?: UserLevel;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

// Lesson Types
export interface Lesson {
  id: number;
  title: string;
  content: string;
  category: LessonCategory;
  level: UserLevel;
  order: number;
  estimated_time: number;
}

export type LessonCategory =
  | 'economics_basics'
  | 'financial_market'
  | 'investment'
  | 'economic_news'
  | 'economic_indicators'
  | 'financial_statements';

// Progress Types
export interface Progress {
  id: number;
  user_id: number;
  lesson_id: number;
  progress: number;
  completed: boolean;
  completed_at?: string;
}

export interface ProgressUpdate {
  progress: number;
  completed?: boolean;
}

// Stats Types
export interface ProgressStats {
  total_lessons: number;
  completed_lessons: number;
  completion_rate: number;
  current_streak: number;
  longest_streak: number;
}
EOF
```

---

## 🌐 API 서비스 레이어

### services/api.ts
```bash
mkdir services
cat > services/api.ts << 'EOF'
import axios, { AxiosInstance, AxiosError } from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Axios 인스턴스 생성
const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 요청 인터셉터: 토큰 자동 추가
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 응답 인터셉터: 에러 처리
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      // 토큰 만료 시 로그아웃
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
EOF
```

---

### services/authService.ts
```bash
cat > services/authService.ts << 'EOF'
import api from './api';
import { User, RegisterData, LoginData, AuthResponse } from '../types';

export const authService = {
  // 회원가입
  register: async (data: RegisterData): Promise<User> => {
    const response = await api.post<User>('/auth/register', data);
    return response.data;
  },

  // 로그인
  login: async (data: LoginData): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>('/auth/login', data);
    return response.data;
  },

  // 현재 사용자 정보
  getMe: async (): Promise<User> => {
    const response = await api.get<User>('/auth/me');
    return response.data;
  },

  // 레벨 변경
  updateLevel: async (level: string): Promise<void> => {
    await api.put('/auth/level', { level });
  },

  // 로그아웃
  logout: () => {
    localStorage.removeItem('token');
  },
};
EOF
```

---

### services/lessonService.ts
```bash
cat > services/lessonService.ts << 'EOF'
import api from './api';
import { Lesson } from '../types';

export const lessonService = {
  // 강의 목록
  getLessons: async (category?: string, level?: string): Promise<Lesson[]> => {
    const params = new URLSearchParams();
    if (category) params.append('category', category);
    if (level) params.append('level', level);
    
    const response = await api.get<Lesson[]>(`/lessons?${params.toString()}`);
    return response.data;
  },

  // 강의 상세
  getLesson: async (lessonId: number): Promise<Lesson> => {
    const response = await api.get<Lesson>(`/lessons/${lessonId}`);
    return response.data;
  },

  // 카테고리별 강의
  getLessonsByCategory: async (category: string): Promise<Lesson[]> => {
    const response = await api.get<Lesson[]>(`/lessons/category/${category}`);
    return response.data;
  },

  // 오늘의 데일리 강의
  getDailyLesson: async (): Promise<Lesson> => {
    const response = await api.get<Lesson>('/lessons/daily/today');
    return response.data;
  },
};
EOF
```

---

### services/progressService.ts
```bash
cat > services/progressService.ts << 'EOF'
import api from './api';
import { Progress, ProgressUpdate, ProgressStats } from '../types';

export const progressService = {
  // 전체 진도 조회
  getAllProgress: async (): Promise<Progress[]> => {
    const response = await api.get<Progress[]>('/progress');
    return response.data;
  },

  // 강의별 진도 조회
  getLessonProgress: async (lessonId: number): Promise<Progress> => {
    const response = await api.get<Progress>(`/progress/lesson/${lessonId}`);
    return response.data;
  },

  // 진도 업데이트
  updateProgress: async (lessonId: number, data: ProgressUpdate): Promise<Progress> => {
    const response = await api.put<Progress>(`/progress/lesson/${lessonId}`, data);
    return response.data;
  },

  // 통계 조회
  getStats: async (): Promise<ProgressStats> => {
    const response = await api.get<ProgressStats>('/progress/stats');
    return response.data;
  },
};
EOF
```

---

## 🔐 Auth Context 설정

### context/AuthContext.tsx
```bash
mkdir context
cat > context/AuthContext.tsx << 'EOF'
import React, { createContext, useState, useEffect, ReactNode } from 'react';
import { User } from '../types';
import { authService } from '../services/authService';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, username: string, password: string, level?: string) => Promise<void>;
  logout: () => void;
  updateUserLevel: (level: string) => Promise<void>;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  // 초기 로드: 토큰이 있으면 사용자 정보 가져오기
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      fetchUser();
    } else {
      setLoading(false);
    }
  }, []);

  const fetchUser = async () => {
    try {
      const userData = await authService.getMe();
      setUser(userData);
    } catch (error) {
      console.error('Failed to fetch user:', error);
      localStorage.removeItem('token');
    } finally {
      setLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    const response = await authService.login({ email, password });
    localStorage.setItem('token', response.access_token);
    await fetchUser();
  };

  const register = async (email: string, username: string, password: string, level?: string) => {
    await authService.register({ email, username, password, level });
    // 회원가입 후 자동 로그인
    await login(email, password);
  };

  const logout = () => {
    authService.logout();
    setUser(null);
  };

  const updateUserLevel = async (level: string) => {
    await authService.updateLevel(level);
    if (user) {
      setUser({ ...user, level: level as any });
    }
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, updateUserLevel }}>
      {children}
    </AuthContext.Provider>
  );
};
EOF
```

---

## 🪝 Custom Hooks

### hooks/useAuth.ts
```bash
mkdir hooks
cat > hooks/useAuth.ts << 'EOF'
import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
EOF
```

---

## 🛠 유틸리티 함수

### utils/storage.ts
```bash
mkdir utils
cat > utils/storage.ts << 'EOF'
// LocalStorage 유틸리티
export const storage = {
  getToken: (): string | null => {
    return localStorage.getItem('token');
  },

  setToken: (token: string): void => {
    localStorage.setItem('token', token);
  },

  removeToken: (): void => {
    localStorage.removeItem('token');
  },

  getOnboardingComplete: (): boolean => {
    return localStorage.getItem('onboarding_complete') === 'true';
  },

  setOnboardingComplete: (complete: boolean): void => {
    localStorage.setItem('onboarding_complete', String(complete));
  },
};
EOF
```

---

## 🗺️ 라우팅 설정

### App.tsx
```bash
cd ..
cat > App.tsx << 'EOF'
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { useAuth } from './hooks/useAuth';

// Pages (나중에 생성할 예정)
import Onboarding from './pages/Onboarding';
import Login from './pages/Login';
import Register from './pages/Register';
import Home from './pages/Home';
import DailyLesson from './pages/DailyLesson';
import FreeLesson from './pages/FreeLesson';
import Settings from './pages/Settings';

// Protected Route 컴포넌트
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return <div className="flex items-center justify-center h-screen">Loading...</div>;
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
};

// Public Route 컴포넌트
const PublicRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return <div className="flex items-center justify-center h-screen">Loading...</div>;
  }

  if (user) {
    return <Navigate to="/home" replace />;
  }

  return <>{children}</>;
};

function AppRoutes() {
  return (
    <Routes>
      {/* Public Routes */}
      <Route
        path="/onboarding"
        element={
          <PublicRoute>
            <Onboarding />
          </PublicRoute>
        }
      />
      <Route
        path="/login"
        element={
          <PublicRoute>
            <Login />
          </PublicRoute>
        }
      />
      <Route
        path="/register"
        element={
          <PublicRoute>
            <Register />
          </PublicRoute>
        }
      />

      {/* Protected Routes */}
      <Route
        path="/home"
        element={
          <ProtectedRoute>
            <Home />
          </ProtectedRoute>
        }
      />
      <Route
        path="/lesson/daily/:lessonId"
        element={
          <ProtectedRoute>
            <DailyLesson />
          </ProtectedRoute>
        }
      />
      <Route
        path="/lesson/free/:lessonId"
        element={
          <ProtectedRoute>
            <FreeLesson />
          </ProtectedRoute>
        }
      />
      <Route
        path="/settings"
        element={
          <ProtectedRoute>
            <Settings />
          </ProtectedRoute>
        }
      />

      {/* Default Route */}
      <Route path="/" element={<Navigate to="/home" replace />} />
      <Route path="*" element={<Navigate to="/home" replace />} />
    </Routes>
  );
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <AppRoutes />
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
EOF
```

---

## 📝 임시 페이지 생성

### pages 디렉토리 생성 및 임시 파일
```bash
mkdir pages
cd pages

# 각 페이지 임시 파일 생성
for page in Onboarding Login Register Home DailyLesson FreeLesson Settings; do
cat > ${page}.tsx << EOF
import React from 'react';

const ${page}: React.FC = () => {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <h1 className="text-3xl font-bold">${page} Page</h1>
    </div>
  );
};

export default ${page};
EOF
done

cd ..
```

---

## 🎨 공통 컴포넌트

### components/common/Button.tsx
```bash
mkdir -p components/common
cat > components/common/Button.tsx << 'EOF'
import React from 'react';

interface ButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  type?: 'button' | 'submit' | 'reset';
  variant?: 'primary' | 'secondary';
  fullWidth?: boolean;
  disabled?: boolean;
}

const Button: React.FC<ButtonProps> = ({
  children,
  onClick,
  type = 'button',
  variant = 'primary',
  fullWidth = false,
  disabled = false,
}) => {
  const baseClass = 'px-6 py-3 rounded-lg font-semibold transition-all';
  const variantClass =
    variant === 'primary'
      ? 'bg-blue-500 text-white hover:bg-blue-600'
      : 'bg-white text-blue-500 border-2 border-blue-500 hover:bg-blue-50';
  const widthClass = fullWidth ? 'w-full' : '';
  const disabledClass = disabled ? 'opacity-50 cursor-not-allowed' : '';

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`${baseClass} ${variantClass} ${widthClass} ${disabledClass}`}
    >
      {children}
    </button>
  );
};

export default Button;
EOF
```

---

### components/common/Input.tsx
```bash
cat > components/common/Input.tsx << 'EOF'
import React from 'react';

interface InputProps {
  label?: string;
  type?: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  placeholder?: string;
  required?: boolean;
  error?: string;
}

const Input: React.FC<InputProps> = ({
  label,
  type = 'text',
  value,
  onChange,
  placeholder,
  required = false,
  error,
}) => {
  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-gray-700 mb-2">
          {label}
          {required && <span className="text-red-500 ml-1">*</span>}
        </label>
      )}
      <input
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        required={required}
        className={`w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
          error ? 'border-red-500' : 'border-gray-300'
        }`}
      />
      {error && <p className="mt-1 text-sm text-red-500">{error}</p>}
    </div>
  );
};

export default Input;
EOF
```

---

## 🧪 테스트

### 개발 서버 실행
```bash
cd ../..  # frontend 디렉토리로
npm start
```

### API 연결 테스트
```bash
# .env 파일 생성
cat > .env << 'EOF'
REACT_APP_API_URL=http://localhost:8000/api
EOF
```

---

## ✅ 확인 체크리스트

```bash
# 디렉토리 구조 확인
ls -la src/types
ls -la src/services
ls -la src/context
ls -la src/hooks
ls -la src/utils
ls -la src/components/common
ls -la src/pages

# TypeScript 에러 확인
npm run build
```

---

## 🐛 트러블슈팅

### 1. TypeScript 에러
```bash
# @types 패키지 설치
npm install --save-dev @types/react @types/react-dom @types/node
```

### 2. Axios 에러
```bash
npm install axios
npm install --save-dev @types/axios
```

### 3. 라우터 에러
```bash
npm install react-router-dom
npm install --save-dev @types/react-router-dom
```

### 4. Context 에러
```typescript
// AuthContext를 사용하기 전에 AuthProvider로 감싸져 있는지 확인
```

---

## ✅ 다음 단계

Frontend 구조 설정이 완료되었습니다!

**다음 문서**: [05-onboarding.md](./05-onboarding.md)에서 온보딩 화면을 개발합니다.