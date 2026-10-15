// B1-1 포트폴리오 스크립트
// index.html 에서 defer 로 불러오므로 DOM 이 다 만들어진 뒤 실행된다.
// 기능은 단계별로 추가한다: a-3 인터랙션, a-4 다크 모드, a-5 Projects, a-6 Contact 폼

// ---------- 기준값 (README 에 명시) ----------
const SCROLL_TOP_OFFSET = 300; // 이만큼 내려가면 맨 위로 버튼을 보인다
const HEADER_SCROLL_OFFSET = 60; // 이만큼 내려가면 네비게이션 배경을 바꾼다
const REVEAL_THRESHOLD = 0.2; // 섹션이 20% 보이면 나타나는 애니메이션을 시작한다

const header = document.querySelector('.site-header');
const navToggle = document.querySelector('.nav__toggle');
const navMenu = document.querySelector('.nav__menu');
const navLinks = document.querySelectorAll('.nav__link');
const logoLink = document.querySelector('.nav__logo');
const scrollTopButton = document.querySelector('.scroll-top');
const footerYear = document.querySelector('.footer__year');

footerYear.textContent = new Date().getFullYear();

// ---------- 다크 모드 ----------
// 테마는 <html data-theme="dark"> 로 표시하고, 색은 CSS 변수가 바꾼다.
// 선택은 localStorage 'theme' 에 저장해 새로고침 후에도 유지한다 (처음 적용은 theme-init.js).
const THEME_STORAGE_KEY = 'theme';
const themeToggle = document.querySelector('.theme-toggle');

function applyTheme(theme) {
  const isDark = theme === 'dark';
  if (isDark) {
    document.documentElement.dataset.theme = 'dark';
  } else {
    delete document.documentElement.dataset.theme;
  }
  themeToggle.textContent = isDark ? '☀️' : '🌙';
  themeToggle.setAttribute('aria-label', isDark ? '라이트 모드로 전환' : '다크 모드로 전환');
  themeToggle.setAttribute('aria-pressed', String(isDark));
}

function saveTheme(theme) {
  try {
    localStorage.setItem(THEME_STORAGE_KEY, theme);
  } catch (error) {
    // 저장이 막혀도 지금 화면의 테마 전환은 그대로 동작한다
  }
}

themeToggle.addEventListener('click', () => {
  const nextTheme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
  applyTheme(nextTheme);
  saveTheme(nextTheme);
});

applyTheme(document.documentElement.dataset.theme === 'dark' ? 'dark' : 'light'); // 버튼 아이콘을 현재 테마에 맞춘다

// ---------- 햄버거 메뉴 ----------
function setMenuOpen(isOpen) {
  navMenu.classList.toggle('active', isOpen);
  navToggle.setAttribute('aria-expanded', String(isOpen));
  navToggle.setAttribute('aria-label', isOpen ? '메뉴 닫기' : '메뉴 열기');
}

navToggle.addEventListener('click', () => {
  const isOpen = navMenu.classList.toggle('active');
  setMenuOpen(isOpen);
});

// ---------- 부드러운 스크롤 ----------
// 앵커 기본 이동(뚝 끊기는 점프)을 막고 scrollIntoView 로 부드럽게 이동한다.
// 움직임 줄이기 설정을 켠 사용자에게는 바로 이동한다.
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

function scrollToTarget(event) {
  const targetId = event.currentTarget.getAttribute('href');
  const target = document.querySelector(targetId);
  if (!target) return;

  event.preventDefault();
  target.scrollIntoView({ behavior: prefersReducedMotion.matches ? 'auto' : 'smooth' });
  history.pushState(null, '', targetId);
  setMenuOpen(false); // 모바일에서 메뉴를 고른 뒤에는 메뉴를 닫는다
}

[logoLink, ...navLinks].forEach((link) => {
  link.addEventListener('click', scrollToTarget);
});

// ---------- 스크롤에 따라 바뀌는 것: 네비 배경, 맨 위로 버튼 ----------
function handleScroll() {
  const y = window.scrollY;
  header.classList.toggle('is-scrolled', y >= HEADER_SCROLL_OFFSET);
  scrollTopButton.classList.toggle('is-visible', y >= SCROLL_TOP_OFFSET);
}

window.addEventListener('scroll', handleScroll, { passive: true });
handleScroll(); // 새로고침으로 중간 위치에서 시작할 때도 바로 맞춘다

scrollTopButton.addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: prefersReducedMotion.matches ? 'auto' : 'smooth' });
});

// ---------- 스크롤 애니메이션 (Intersection Observer) ----------
// Hero 는 처음부터 보이므로 제외하고, 나머지 섹션이 화면에 들어오면 한 번만 나타나게 한다.
const revealTargets = document.querySelectorAll('main .section');

if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-visible');
      observer.unobserve(entry.target);
    });
  }, { threshold: REVEAL_THRESHOLD });

  revealTargets.forEach((section) => {
    section.classList.add('reveal');
    observer.observe(section);
  });
}

// ---------- Projects: GitHub API ----------
// 상태(projectsState)를 바꾸고 renderProjects() 로 화면을 다시 그린다.
// 상태: loading(불러오는 중) → success(카드) / empty(보여줄 것 없음) / error(실패 + 다시 시도)
const GITHUB_USER = 'KKamtte';
const REPOS_URL = `https://api.github.com/users/${GITHUB_USER}/repos?per_page=100&sort=updated`;
// 결과물로 볼 수 있는 저장소만 고른다 (wiki/plans/b1-1.md 결정 사항 5)
const FEATURED_REPOS = ['library-search', 'spring-playground', 'nest_study'];

const projectsStatus = document.querySelector('.projects__status');
const projectsGrid = document.querySelector('.projects__grid');

const projectsState = {
  status: 'loading',
  repos: [],
  errorMessage: '',
};

function setProjectsState(nextState) {
  Object.assign(projectsState, nextState);
  renderProjects();
}

// API 에서 온 글자를 innerHTML 에 넣기 전에 HTML 로 해석되지 않게 바꾼다
function escapeHtml(text) {
  return String(text)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

function formatDate(isoString) {
  return new Date(isoString).toLocaleDateString('ko-KR', { year: 'numeric', month: 'short', day: 'numeric' });
}

function createRepoCard({ name, html_url, description, language, stargazers_count, pushed_at }) {
  return `
    <article class="project-card">
      <h3 class="project-card__title">
        <a href="${escapeHtml(html_url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(name)}</a>
      </h3>
      <p class="project-card__desc">${description ? escapeHtml(description) : '설명이 아직 없습니다.'}</p>
      <ul class="project-card__meta">
        ${language ? `<li class="project-card__lang">${escapeHtml(language)}</li>` : ''}
        <li aria-label="스타 ${stargazers_count}개">★ ${stargazers_count}</li>
        <li>최근 수정 <time datetime="${escapeHtml(pushed_at)}">${formatDate(pushed_at)}</time></li>
      </ul>
    </article>
  `;
}

function renderProjects() {
  const { status, repos, errorMessage } = projectsState;
  projectsGrid.innerHTML = '';

  if (status === 'loading') {
    projectsStatus.innerHTML = '<div class="spinner" aria-hidden="true"></div><p>로딩 중...</p>';
    return;
  }

  if (status === 'error') {
    projectsStatus.innerHTML = `
      <p>프로젝트를 불러올 수 없습니다.</p>
      <p class="projects__error-detail">${escapeHtml(errorMessage)}</p>
      <button class="btn btn--secondary projects__retry" type="button">다시 시도</button>
    `;
    projectsStatus.querySelector('.projects__retry').addEventListener('click', loadProjects);
    return;
  }

  if (status === 'empty') {
    projectsStatus.innerHTML = '<p>표시할 프로젝트가 없습니다.</p>';
    return;
  }

  projectsStatus.innerHTML = '';
  projectsGrid.innerHTML = repos.map(createRepoCard).join('');
}

async function loadProjects() {
  setProjectsState({ status: 'loading', repos: [], errorMessage: '' });

  try {
    const response = await fetch(REPOS_URL);

    // 인증 없는 호출은 시간당 60회 제한이 있고, 넘으면 403 이 온다
    if (response.status === 403) {
      throw new Error('GitHub API 요청 한도를 넘었습니다. 잠시 후 다시 시도해 주세요.');
    }
    if (!response.ok) {
      throw new Error(`GitHub API 응답 오류 (${response.status})`);
    }

    const allRepos = await response.json();
    const repos = allRepos
      .filter((repo) => FEATURED_REPOS.includes(repo.name))
      .sort((a, b) => new Date(b.pushed_at) - new Date(a.pushed_at));

    setProjectsState({ status: repos.length > 0 ? 'success' : 'empty', repos });
  } catch (error) {
    // 네트워크가 끊긴 경우 fetch 자체가 TypeError 로 실패한다
    const message = error instanceof TypeError ? '네트워크 연결을 확인해 주세요.' : error.message;
    setProjectsState({ status: 'error', errorMessage: message });
  }
}

loadProjects();

// ---------- Contact 폼 검증 ----------
// 입력값 → 검증 결과(에러 메시지) → 칸 아래 메시지 표시/숨김.
// 처음에는 제출할 때 검사하고, 한 번 에러가 난 칸은 입력할 때마다(input) 다시 검사해 고치는 즉시 메시지가 사라진다.
const contactForm = document.querySelector('.contact__form');
const formSuccess = document.querySelector('.form__success');
// 이메일 형식: 공백 없는 글자@공백 없는 글자.공백 없는 글자 (예: name@example.com)
const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const validators = {
  name: (value) => (value ? '' : '이름을 입력해 주세요.'),
  email: (value) => {
    if (!value) return '이메일을 입력해 주세요.';
    if (!EMAIL_PATTERN.test(value)) return '이메일 형식이 올바르지 않습니다. (예: name@example.com)';
    return '';
  },
  message: (value) => (value ? '' : '메시지를 입력해 주세요.'),
};

function validateField(field) {
  const errorMessage = validators[field.name](field.value.trim());
  const errorElement = document.getElementById(`${field.id}-error`);
  errorElement.textContent = errorMessage;
  field.setAttribute('aria-invalid', String(errorMessage !== ''));
  return errorMessage === '';
}

const formFields = [...contactForm.elements].filter((element) => element.name in validators);

formFields.forEach((field) => {
  field.addEventListener('input', () => {
    formSuccess.textContent = '';
    if (field.getAttribute('aria-invalid') === 'true') {
      validateField(field);
    }
  });
});

contactForm.addEventListener('submit', (event) => {
  event.preventDefault(); // 페이지 새로고침(기본 제출)을 막는다

  // every 를 쓰면 첫 에러에서 멈추므로, map 으로 모든 칸을 검사해 에러를 한 번에 보여준다
  const results = formFields.map(validateField);
  const isValid = results.every(Boolean);

  if (!isValid) {
    formSuccess.textContent = '';
    formFields[results.indexOf(false)].focus(); // 첫 번째 에러 칸으로 이동
    return;
  }

  const name = contactForm.elements.name.value.trim();
  // 실제 전송 기능은 없으므로(보너스 항목), 방문자가 오해하지 않게 그대로 알린다
  formSuccess.textContent = `${name}님, 감사합니다! 입력이 확인되었습니다. 지금은 데모 폼이라 실제로 전송되지는 않으니, 급한 연락은 이메일로 부탁드립니다.`;
  contactForm.reset();
  formFields.forEach((field) => field.removeAttribute('aria-invalid'));
});
