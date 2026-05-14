const BASE = '';

function getToken(): string {
  if (typeof window === 'undefined') return '';
  return localStorage.getItem('token') || '';
}

export function authHeaders(): Record<string, string> {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function apiFetch(path: string, options: RequestInit = {}) {
  const res = await fetch(`${BASE}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...authHeaders(),
      ...(options.headers || {}),
    },
  });
  if (res.status === 401) {
    localStorage.removeItem('token');
    window.location.href = '/login';
    throw new Error('Unauthorized');
  }
  return res;
}

export function getUser() {
  if (typeof window === 'undefined') return null;
  try {
    return JSON.parse(localStorage.getItem('user') || 'null');
  } catch {
    return null;
  }
}

export function logout() {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  window.location.href = '/login';
}
