# Scanner

휴대폰 카메라로 문서를 스캔하는 Android 앱입니다. 웹 앱(HTML 한 파일)을 [Capacitor](https://capacitorjs.com)로 감싸 APK로 빌드합니다.

## 기능

- 앱 안 카메라 촬영(문서 테두리 실시간 표시), 갤러리·파일에서 여러 장 가져오기
- 자동 자르기 + 원근 보정, 굽은·접힌 페이지 펴기, 기울기 보정, 수동 자르기(모서리 4개 + 돋보기)
- 빛 반사 자동 제거, 효과(원본·컬러·회색조·흑백)와 "하얗게" 정도 조절
- 여러 장 선택 후 삭제(되돌리기), 드래그로 순서 변경(선택한 페이지는 묶음으로 이동)
- PDF(A4 / 원본 크기) 또는 JPG(ZIP / 한 장씩)로 내보내기 → Android 공유 창
- 설정: 자동 보정 항목별 켜기/끄기, 시스템·라이트·다크 테마
- 스캔한 페이지는 기기(IndexedDB)에 저장되어 앱을 다시 열어도 남아 있음

## 폴더 구조

| 경로 | 내용 |
| --- | --- |
| `src/index.html` | 앱 본체(화면 + 이미지 처리). 여기만 고치면 됩니다 |
| `build-web.py` | `src/index.html` → `www/index.html` (문서 틀 추가, CDN 대신 `www/vendor` 사용) |
| `www/` | Capacitor가 앱에 넣는 웹 파일 |
| `make-icons.py` | 앱 아이콘·스플래시 생성 |
| `android/` | Capacitor가 만든 Android 프로젝트 |

## 빌드

필요한 것: Node.js 20+, JDK 21, Android SDK(platform 36, build-tools 36)

```bash
npm install
python3 build-web.py
npx cap sync android
cd android && ./gradlew assembleDebug
```

APK 위치: `android/app/build/outputs/apk/debug/app-debug.apk`

Play 스토어용은 서명 키를 만든 뒤 `./gradlew assembleRelease`(또는 `bundleRelease`)로 빌드합니다.
