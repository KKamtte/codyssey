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
