가상환경에서 Flask 애플리케이션을 실행하려면 다음 단계를 따르세요:

1. **가상환경 생성**:
   ```sh
   python3 -m venv venv
   ```

2. **가상환경 활성화**:
   ```sh
   source venv/bin/activate
   ```

3. **가상환경 비활성화**:
   ```sh
   deactivate
   ```

4. **필요한 패키지 설치**:
   [`requirements.txt`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2FA59833%2FDocuments%2FWorkspace%2Fyoutube-transcriber%2Frequirements.txt%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "/Users/A59833/Documents/Workspace/youtube-transcriber/requirements.txt") 파일이 있는 경우:
   ```sh
   pip install -r requirements.txt
   ```
   [`requirements.txt`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2FA59833%2FDocuments%2FWorkspace%2Fyoutube-transcriber%2Frequirements.txt%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "/Users/A59833/Documents/Workspace/youtube-transcriber/requirements.txt") 파일이 없는 경우, 필요한 패키지를 직접 설치:
   ```sh
   pip install flask flask-cors youtube-transcript-api
   ```

5. **애플리케이션 실행**:
   ```sh
   python app.py
   ```

이제 Flask 애플리케이션이 가상환경에서 실행됩니다.