// B1-1 포트폴리오 스크립트
// index.html 에서 defer 로 불러오므로 DOM 이 다 만들어진 뒤 실행된다.
// 기능은 단계별로 추가한다: a-3 인터랙션, a-4 다크 모드, a-5 Projects, a-6 Contact 폼

const footerYear = document.querySelector('.footer__year');
footerYear.textContent = new Date().getFullYear();
