// 저장된 테마를 화면을 그리기 전에 적용한다.
// main.js 는 defer 라 늦게 실행되므로, 여기서 먼저 처리하지 않으면 다크 모드 사용자에게 흰 화면이 잠깐 보인다.
// 그래서 이 파일만 <head> 에서 defer 없이 불러온다.
// 우선순위: 사용자가 토글로 고른 값(localStorage) > 운영체제 설정(prefers-color-scheme, 보너스)
(() => {
  let savedTheme = null;
  try {
    savedTheme = localStorage.getItem('theme');
  } catch (error) {
    // 저장소 접근이 막힌 환경(일부 사생활 보호 모드)에서는 운영체제 설정만 따른다
  }

  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  if (savedTheme === 'dark' || (savedTheme === null && prefersDark)) {
    document.documentElement.dataset.theme = 'dark';
  }
})();
